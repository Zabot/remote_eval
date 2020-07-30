FROM python:latest

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY remote_eval/ /tmp/remote_eval
COPY setup.py /tmp/remote_eval
RUN pip install /tmp/remote_eval

ENV FLASK_APP=remote_eval:app
EXPOSE 5000
CMD /usr/local/bin/flask run --host=0.0.0.0

