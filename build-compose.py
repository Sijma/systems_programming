import json

if __name__ == '__main__':
    # Load the configuration file
    with open('secrets.json') as config_file:
        secret = json.load(config_file)

    # Generate the Docker Compose YAML
    with open('docker-compose.yml', 'w') as compose_file:
        compose_file.write(f'''
    version: '3'
    services:
      postgres:
        image: postgres:latest
        container_name: postgres_c
        healthcheck:
          test: [ "CMD-SHELL", "pg_isready" ]
          interval: 5s
          timeout: 5s
          retries: 5
        restart: always
        networks:
          - db-network
        ports:
          - "5432:5432"
        environment:
          POSTGRES_USER: {secret["main_db"]["user"]}
          POSTGRES_PASSWORD: {secret["main_db"]["password"]}
          POSTGRES_DB: {secret["main_db"]["database"]}
        volumes:
          - ./init.sql:/docker-entrypoint-initdb.d/init.sql
          - ./postgres_data:/var/lib/postgresql/data
    
      postgres_authentication:
        image: postgres:latest
        container_name: postgres_authentication_c
        healthcheck:
          test: [ "CMD-SHELL", "pg_isready" ]
          interval: 5s
          timeout: 5s
          retries: 5
        restart: always
        networks:
          - app-network
        environment:
          POSTGRES_USER: {secret["auth_db"]["user"]}
          POSTGRES_PASSWORD: {secret["auth_db"]["password"]}
          POSTGRES_DB: {secret["auth_db"]["database"]}
        volumes:
          - ./postgres_authentication_data:/var/lib/postgresql/data
    
      data_access_layer:
        build: ./database
        container_name: database_c
        restart: always
        healthcheck:
          test: ["CMD-SHELL", "wget --quiet --tries=1 --spider http://localhost:8000/ || exit 1"]
          interval: 5s
          timeout: 5s
          retries: 5
        networks:
          - db-network
          - dal-network
        depends_on:
          postgres:
            condition: service_healthy
        environment:
          POSTGRES_HOST: postgres
          POSTGRES_PORT: 5432
          POSTGRES_USER: {secret["main_db"]["user"]}
          POSTGRES_PASSWORD: {secret["main_db"]["password"]}
          POSTGRES_DB: {secret["main_db"]["database"]}
    
      kafka:
        image: bitnami/kafka:latest
        container_name: kafka_c
        healthcheck:
          test: ["CMD-SHELL", "kafka-topics.sh --list --bootstrap-server kafka:9092"]
          interval: 10s
          timeout: 5s
          retries: 10
        restart: always
        networks:
          - kafka-network
        environment:
          ALLOW_PLAINTEXT_LISTENER: 'yes'
    
      init-kafka:
        image: confluentinc/cp-kafka:latest
        container_name: init-kafka_c
        networks:
          - kafka-network
        depends_on:
          kafka:
            condition: service_healthy
        entrypoint: [ '/bin/sh', '-c' ]
        command: |
          "
          echo -e 'Creating kafka topics'
          kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic user --replication-factor 1 --partitions 1
          kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic event --replication-factor 1 --partitions 1
          kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic coupon --replication-factor 1 --partitions 1
          kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic statistics --replication-factor 1 --partitions 1
          
          echo -e 'Successfully created the following topics:'
          kafka-topics --bootstrap-server kafka:9092 --list
          "
    
      kafka_consumer:
        image: python:latest
        container_name: kafka_consumer_c
        restart: always
        depends_on:
          data_access_layer:
            condition: service_healthy
          init-kafka:
            condition: service_completed_successfully
        networks:
          - kafka-network
          - dal-network
        volumes:
          - ./kafka_code/requirements.txt:/requirements.txt
          - ./kafka_code/kafka_consumer.py:/kafka_consumer.py
        command: sh -c "pip install -r requirements.txt && python -u kafka_consumer.py"
        environment:
          FASTAPI_HOST: data_access_layer
          FASTAPI_PORT: 8000
          KAFKA_HOST: kafka
          KAFKA_PORT: 9092
          SO_REUSEPORT: 1
    
      user_generator:
        image: python:latest
        container_name: user_generator_c
        restart: always
        depends_on:
          kafka_consumer:
            condition: service_started
        networks:
          - kafka-network
        volumes:
          - ./kafka_code/requirements.txt:/requirements.txt
          - ./kafka_code/user_generator.py:/user_generator.py
        command: sh -c "pip install -r requirements.txt && python -u user_generator.py"
        environment:
          KAFKA_HOST: kafka
          KAFKA_PORT: 9092
    
      event_generator:
        image: python:latest
        container_name: event_generator_c
        restart: always
        depends_on:
          kafka_consumer:
            condition: service_started
        networks:
          - kafka-network
        volumes:
          - ./kafka_code/requirements.txt:/requirements.txt
          - ./kafka_code/event_generator.py:/event_generator.py
        command: sh -c "pip install -r requirements.txt && python -u event_generator.py"
        environment:
          KAFKA_HOST: kafka
          KAFKA_PORT: 9092
    
      coupon_generator:
        image: python:latest
        container_name: coupon_generator_c
        restart: always
        depends_on:
          event_generator:
            condition: service_started
          kafka_consumer:
            condition: service_started
        networks:
          - dal-network
          - kafka-network
        volumes:
          - ./kafka_code/requirements.txt:/requirements.txt
          - ./kafka_code/coupon_generator.py:/coupon_generator.py
        command: sh -c "pip install -r requirements.txt && python -u coupon_generator.py"
        environment:
          FASTAPI_HOST: data_access_layer
          FASTAPI_PORT: 8000
          KAFKA_HOST: kafka
          KAFKA_PORT: 9092
    
      statistics_generator:
        image: python:latest
        container_name: statistics_generator_c
        restart: always
        depends_on:
          event_generator:
            condition: service_started
          kafka_consumer:
            condition: service_started
        networks:
          - kafka-network
          - dal-network
        volumes:
          - ./kafka_code/requirements.txt:/requirements.txt
          - ./kafka_code/statistics_generator.py:/statistics_generator.py
        command: sh -c "pip install -r requirements.txt && python -u statistics_generator.py"
        environment:
          FASTAPI_HOST: data_access_layer
          FASTAPI_PORT: 8000
          KAFKA_HOST: kafka
          KAFKA_PORT: 9092
    
    
    #  tests:
    #      build:
    #        context: ./tests
    #      container_name: tests_c
    #      stdin_open: true
    #      tty: true
    #      depends_on:
    #        database:
    #          condition: service_healthy
    #      volumes:
    #        - .:/app
    #        - ./tests:/app/tests
    
      mailhog:
        image: mailhog/mailhog
        container_name: mailhog_c
        networks:
          - app-network
        ports:
          - "8025:8025"  # Web interface to view emails
        # TODO: Add healthcheck
    
      app:
        build: ./api
        container_name: app_c
        restart: always
        stop_signal: SIGINT
        networks:
          - app-network
          - dal-network
        ports:
          - "5000:5000"
        volumes:
          - ./api:/app
        depends_on:
          data_access_layer:
            condition: service_healthy
    #      tests:
    #        condition: service_completed_successfully
          mailhog:
            condition: service_started
          postgres_authentication:
            condition: service_healthy
        environment:
          FASTAPI_HOST: data_access_layer
          FASTAPI_PORT: 8000
          AUTH_HOST: postgres_authentication
          AUTH_PORT: 5432
          AUTH_USER: {secret["auth_db"]["user"]}
          AUTH_PASSWORD: {secret["auth_db"]["password"]}
          AUTH_DB: {secret["auth_db"]["database"]}
          FLASK_SECRET_KEY: {secret["flask"]["secret_key"]}
          JWT_SECRET_KEY: {secret["flask"]["jwt_secret_key"]}
          MAIL_PASSWORD: {secret["flask"]["mail_password"]}
    
    
      frontend:
        build:
          context: ./frontend
          dockerfile: ./Dockerfile-development
        container_name: frontend_c
        restart: always
        networks:
          - app-network
        depends_on:
          app:
            condition: service_started
        ports:
          - "3000:3000"  # 3000 for dockerfile development, 80 for production
        volumes:
          - ./frontend:/app
          - ./app/node_modules
        stdin_open: true # Development only
        tty: true # Development only
        environment:
          FLASK_HOST: app
          FLASK_PORT: 5000
    
    networks:
      app-network:
      db-network:
      dal-network:
      kafka-network:
    ''')
