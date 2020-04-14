FROM python:3.8.2-apline3.11

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

WORKDIR /app

COPY . /app

CMD ["python", "./sample_train.py 6 20 4 40 4"]

