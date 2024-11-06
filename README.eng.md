<h1><img src="https://github.com/emptybutton/Aqua/blob/main/assets/logo.png?raw=true" width="32" height="32"/> Aqua</h1>
Application for tracking your water balance.

## Deployment
To deploy this application locally:
1. clone this repository
2. run all services
3. set the `Postgres` table structure
4. initialize `MongoDB` cluster

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose -f Aqua/docker-compose.dev.yml up
docker exec aqua-backend alembic -c src/auth/alembic.ini upgrade head
docker exec aqua-mongo1 mognosh -f /scripts/init-cluster.js
```

> [!NOTE]
> After such a launch, for greater speed, you can launch only using:
> ```bash
> docker compose -f Aqua/docker-compose.dev.yml up
> ```

## About the repository
- this repository is a monorepository where all parts of the system are located
- each repository contains a service that has its own deployment point and the ability to deploy independently
- each service has its own `README` file, which includes information about its individual launch
- all repositories are located in the `services` directory
