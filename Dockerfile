FROM python:latest

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]