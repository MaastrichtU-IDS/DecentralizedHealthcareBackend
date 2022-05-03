
# LUCE Technical Prototype 
## How to launch LUCE (Debug purpose)
### database
LUCE use PostgresQL to keep user information, just run:
`docker compose up`
this command will launch a `postgres_db` container，you can configure it in Django project settings

### Ganache
As ganache-cli has upgrade into a full functional application - [Ganache](https://trufflesuite.com/ganache/), which brings many useful features for debuging. You can configure it as a `HttpProvider`

### Django server
activate your devlopment environment, and start a Django server; generally, go into the root directory of Django project, `luce_django/luce` in this case, and run:
`python manage.py runserver`

You can access each end-point with http request, or use this [app](https://github.com/klifish/DecentralizedHealthcare)