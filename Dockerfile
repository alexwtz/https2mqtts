### 1. Get Linux
FROM ubuntu:22.04

RUN apt update
### 2. Get Java via the package manager
RUN mkdir -p /usr/share/man/man1

RUN apt install openjdk-17-jre-headless -y

### 3. Get Python, PIP
RUN apt install python3 python3-pip -y

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

# 
RUN apt install wget -y
RUN wget https://github.com/hivemq/mqtt-cli/releases/download/v4.25.0/mqtt-cli-4.25.0.deb
RUN dpkg -i mqtt-cli-4.25.0.deb

COPY ./app /code/app
COPY ./log.ini /code/log.ini

EXPOSE 80

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "/code/log.ini"]