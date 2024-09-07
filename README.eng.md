<h1><img src="https://github.com/emptybutton/Aqua/blob/main/assets/logo.png?raw=true" width="32" height="32"/> Aqua</h1>
Application for tracking your water balance.

## Deployment
To deploy this application locally:
1. clone this repository
2. set the DB structure
3. run all services inside `docker`

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose -f Aqua/services/backend/docker-compose.dev.yml run aqua alembic upgrade head
docker compose -f Aqua/docker-compose.dev.yml up
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
