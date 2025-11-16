FROM python:3.14.0

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "endpoint.py"]