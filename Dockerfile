FROM python:3.7

ENV PORT 8000
ENV APP_HOME /app
WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN python -m deeppavlov install squad_ru_rubert_infer
RUN python -m deeppavlov download squad_ru_rubert_infer

COPY ./deal_digger ./


CMD exec gunicorn --bind :$PORT --workers 4 --timeout 600 deal_digger:wsgi