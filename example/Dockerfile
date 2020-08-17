FROM python:3.7.5

WORKDIR /app/
ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

ADD extract_gpe.py /app/extract_gpe.py
