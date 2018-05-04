FROM python:3.6.5-slim
COPY requirements.pip .
RUN pip install -r requirements.pip
COPY *.py ./
CMD python game.py
