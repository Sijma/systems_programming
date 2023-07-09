FROM python:3.9-alpine

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /app

COPY ./api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .
COPY schemas.py .

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]