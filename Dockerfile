FROM python:2.7

WORKDIR /wsgi

COPY src/ .

# RUN pip freeze > requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 wsgi:app
