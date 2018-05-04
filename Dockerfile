FROM python:3.6.5-alpine3.6
COPY *.py .
COPY requirements.pip .
RUN pip install -r requirements.pip
CMD python game.py
