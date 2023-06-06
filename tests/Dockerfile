FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER=coupon_recommendation_system
ENV POSTGRES_PASSWORD=Xq8@SHF0S1&sM7v3
ENV POSTGRES_DB=betting_recommendation_system
ENV KAFKA_HOST=kafka
ENV KAFKA_PORT=9092

ENTRYPOINT ["python", "-m", "unittest", "discover", "-s", "tests"]
