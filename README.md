# LUCE Technical Prototype 
[LUCE](https://www.sciencedirect.com/science/article/pii/S2096720922000434) (License accoUntability and CompliancE) is a blockchain-based data sharing platform for monitoring data license accountability and compliance. It is designed to provide full transparency on what happens to the data after being shared with third parties. The contributions of LUCE consist of:
1. a decentralized data sharing solution with accountability and compliance by design 
2.  a dynamic consent model for personalized data sharing preferences and for enabling legal compliance mechanisms

## Architecture
The architecture of LUCE presented as follow:

![LUCE](https://ars.els-cdn.com/content/image/1-s2.0-S2096720922000434-gr1.jpg)

There are four main actors involved:
- data provider, e.g., a researcher willing to share a dataset;
- data requester, e.g., a researcher requesting to reuse a dataset;
- supervisory authority, e.g., a national public authority in charge of monitoring the adherece to data regulations
- data subjects, e.g.,any individual whose data are being collected, held, or processed.

> For detailed introduction of LUCE, please refer to [LUCE paper](https://www.sciencedirect.com/science/article/pii/S2096720922000434)

We also provide a view of implementing LUCE:

![implementation of LUCE](./img/LUCE%20architecture.drawio.svg)

### Django
LUCE utilses Django to hold data sharing business.

### Database
LUCE use PostgresQL to keep user information, you can configure it in Django project settings

### Ganache
LUCE uses [Ganache](https://trufflesuite.com/ganache/) as a blockchain backend. It can be used as a GUI of blockchain or just as a [container](https://hub.docker.com/r/trufflesuite/ganache).




## How to launch LUCE (For developers)
`docker compose up` will launch all containers.

LUCE use PostgresQL to keep user information, 


## How to access LUCE
You can access with [LUCE API](https://documenter.getpostman.com/view/18666298/2s93sZ7aDm), or with [app](https://github.com/klifish/DecentralizedHealthcare)

### For http request user
1. Step 1: register
2. Step 2: login
> Once logged in, you can get a token which is necessary for later operation
3. Step 3: upload data

## Tips
1. if you encounter the issue: 

> ```brownie.exceptions.ContractNotFound: No contract deployed at 0xDa574613C62f6DB9FFE8dCC5a8b079Ba37e29390```,

> please go to `luce_vm/brownie`, remove `build/deployment` folder in the brownie directory, and then run `brownie compile`

2. If you got the response:
```
{
    "error": {
        "code": 400,
        "message": "validation error",
        "status": "ERROR",
        "details": "luce registry was not deployed"
    },
    "data": {}
}
```
please deploy a LUCERegistry contract in `admin/deployRegistry/` endpoint.