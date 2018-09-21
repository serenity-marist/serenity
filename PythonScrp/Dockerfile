FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y \
    python-pip  \
    python-dev \
    build-essential \
&& pip install --upgrade pip

WORKDIR /serenity-api
COPY src/. .
COPY requirements.txt .

EXPOSE 8080
RUN pip install -r requirements.txt
CMD ["python","-u","app.py"]

