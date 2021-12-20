
## Build docker container:

```bash
docker build -t films_app:latest .
```

## Set up environment variables:

> NOTE: you should replace stars with real passwords!!!

```bash
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=****
export PGADMIN_DEFAULT_EMAIL=pgadmin.default@email.com
export PGADMIN_DEFAULT_PASSWORD=****
export DATABASE_NAME=films_site_db
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

## Run `docker-compose`:

```bash
docker-compose up
```

It will start 3 services: 
- films_app on port 8080
- dp (postgresql) on port 5432
- pgadmin on port 8081
