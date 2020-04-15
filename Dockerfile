FROM ubuntu:18.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget gcc build-essential git && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

ENV PORT 8000
ENV APP_HOME /app
WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m deeppavlov install squad_ru_rubert_infer
RUN python -m deeppavlov download squad_ru_rubert_infer
RUN conda install nltk
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader perluniprops
RUN python -m nltk.downloader nonbreaking_prefixes

COPY ./deal_digger ./
RUN python -c "import deal_api.dl_model"
