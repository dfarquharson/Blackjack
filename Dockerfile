FROM python:3.6.5-slim
RUN mkdir /code
WORKDIR /code
COPY requirements.pip .
RUN pip install -r requirements.pip
COPY *.py ./
CMD python blackjack.py
