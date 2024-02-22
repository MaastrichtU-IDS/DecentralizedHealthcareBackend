FROM python:3.9
# FROM --platform=linux/amd64 python:3.9
# 3.10: 6.15.0
# 3.9: 5.31.3

USER root
WORKDIR /app

ENV USE_TZ=False

RUN apt-get update && \
    apt-get install -y wget build-essential software-properties-common libssl-dev postgresql-client libpq-dev

ADD ./requirements.txt .
RUN pip install -r requirements.txt

# Compile the sol contracts with brownie
RUN brownie pm install OpenZeppelin/openzeppelin-contracts@4.8.0
ADD ./brownie ./brownie
RUN cd brownie && \
    brownie compile && \
    brownie networks add LUCE luce host=http://ganache_db:8545 chainid=72
# brownie networks add [environment] [id] host=[host] [KEY=VALUE, ...]

ADD . .
RUN pip install -e .

EXPOSE 8000
ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]
