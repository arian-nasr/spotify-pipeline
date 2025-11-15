FROM python:3.14.0

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "grab.py"]