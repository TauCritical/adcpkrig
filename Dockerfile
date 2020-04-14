FROM python:3.8.2-slim-buster

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY . /app

RUN make /app

CMD python /app/sample_train.py 6 20 4 40 4 v_mag

