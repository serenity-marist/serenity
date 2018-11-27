FROM python:latest

ENV LISTEN_PORT 5000
EXPOSE 5000

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD python routes.py
# CMD python run.py
