FROM python:latest

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY remote_eval/ /tmp/server/remote_eval
COPY setup.py /tmp/server
RUN pip install /tmp/server

ENV FLASK_APP=remote_eval:app
EXPOSE 5000
CMD /usr/local/bin/flask run --host=0.0.0.0

