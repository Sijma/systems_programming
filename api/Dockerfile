FROM python:3.9-alpine

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Setup Cron
RUN apt-get update && apt-get -y install cron
RUN chmod +x ./recommendation_scheduler.py
RUN echo "5 0 * * * /usr/local/bin/python3 /app/recommendation_scheduler.py" >> /etc/crontab
CMD cron -f

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]