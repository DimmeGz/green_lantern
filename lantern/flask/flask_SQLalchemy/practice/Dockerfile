FROM python:3.8
LABEL name='docker_homework'
COPY /app /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python wsgi.py