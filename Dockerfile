FROM python:3.9

USER root
WORKDIR /luce

ENV USE_TZ=False

RUN apt-get update && \
    apt-get install -y wget build-essential software-properties-common libssl-dev  postgresql-client libpq-dev

RUN pip install eth-brownie
RUN python -m pip install Django
RUN pip install django-filter
RUN pip install django-extensions
RUN pip3 install djangorestframework
RUN pip install django-cors-headers
RUN pip install psycopg2
RUN pip install matplotlib
# Install Ethereum
# RUN add-apt-repository -y ppa:ethereum/ethereum && \
#     apt update && \
#     apt install -y ethereum


# Install from requirements.txt to only rebuild when requirements file change
# ADD requirements.txt .

# RUN pip install -r requirements.txt

COPY luce_vm/scripts/entrypoint.sh /entrypoint.sh
RUN chmod 744 /entrypoint.sh

RUN brownie networks add LUCE luce host=http://ganache_db:8545 chainid=72



COPY . .

# RUN pip install -e .

# RUN python -m solcx.install v0.4.25



EXPOSE 8000

ENTRYPOINT [ "/entrypoint.sh" ]