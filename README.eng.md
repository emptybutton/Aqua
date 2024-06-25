<h1><img src="https://github.com/emptybutton/Aqua/blob/main/assets/logo.png?raw=true" width="33" height="33"/> Aqua</h1>
Application for tracking your water balance.

## Deployment
To deploy this application locally:
1. clone this repository
2. initialize and run it within `docker`

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose --project-directory ./Aqua run backend ash ./scripts/init-and-start.sh
```

> [!TIP]
> After initialization, for faster startup speed, you can launch using:
> ```bash
> docker compose --project-directory ./Aqua up
> ```

## About the repository
This repository is a monorepository where both the backend and frontend parts of the application are located. <br>
Each such repository contains information about this part of the application, including information on how to install it separately.
