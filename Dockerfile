FROM python:3.8.2-stretch

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY . /home/appuser

CMD ["python", "./sample_train.py 6 20 4 40 4"]

