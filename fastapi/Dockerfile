FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
# FROM ethereum/solc:stable
# FROM python:3.10

WORKDIR /app

# ENV USE_TZ=False \
#     PYTHONUNBUFFERED='1' \
#     APP_MODULE=src.luce.main:app \
#     MAX_WORKERS='16'

## Check here for more details on how the image is built and which env variables are available
# https://github.com/tiangolo/uvicorn-gunicorn-docker/tree/master/docker-images
#   WORKER_CLASS=uvicorn.workers.UvicornWorker \
#   WORKERS_PER_CORE='1' \
#   LOG_LEVEL=info

RUN apt-get update
RUN apt-get install -y software-properties-common wget build-essential libssl-dev postgresql-client libpq-dev python3-dev
RUN pip install --upgrade pip

RUN curl -L https://github.com/ethereum/solidity/releases/download/v0.8.25/solc-static-linux -o /usr/local/bin/solc \
    && chmod +x /usr/local/bin/solc


# RUN apt-get update && \
#     apt-get install -y software-properties-common wget build-essential libssl-dev postgresql-client libpq-dev python3-dev && \
#     pip install --upgrade pip

# RUN add-apt-repository ppa:ethereum/ethereum
# RUN apt-get update
# RUN apt-get install -y solc

COPY requirements.txt .

RUN pip install -r requirements.txt

# # Compile the sol contracts with brownie
RUN brownie pm install OpenZeppelin/openzeppelin-contracts@4.8.0
ADD ./brownie ./brownie
RUN cd brownie && \
    brownie compile && \
    brownie networks add LUCE luce host=http://ganache_db:8545 chainid=72

ADD . .

RUN pip install -e .

# By default this image entrypoint will use gunicorn to start multiple uvicorn workers

ENTRYPOINT [ "uvicorn", "src.luce.main:app" ]
# ENTRYPOINT [ "sleep", "infinity" ]