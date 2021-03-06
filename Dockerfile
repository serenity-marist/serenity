FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y vim
EXPOSE 80
CMD python routes.py
# CMD python run.py
