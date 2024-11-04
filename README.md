<h1><img src="https://github.com/emptybutton/Aqua/blob/main/assets/logo.png?raw=true" width="32" height="32"/> Aqua</h1>

> [English version](https://github.com/emptybutton/Aqua/blob/main/README.eng.md) of this README file.
___

Приложение для отслеживания вашего водного баланса.


## Как запустить
Что бы запустить локально:
1. склонируйте этот репозиторий
2. запустите все сервисы
3. установите структуру таблиц `Postgres`
4. инициализируйте кластер `MongoDB`

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose -f Aqua/docker-compose.dev.yml up
docker exec aqua-backend alembic upgrade head
docker exec aqua-mongo1 mognosh -f /scripts/init-cluster.js
```

> [!NOTE]
> После такого запуска, для большей скорости, можете запускать только при помощи:
> ```bash
> docker compose -f Aqua/docker-compose.dev.yml up
> ```

## Про репозиторий
- этот репозиторий является монорепозиторием, где находятся все части системы
- каждый репозиторий содержит сервис, имеющий свою точку деплоя и возможность разворачиватся независимо
- у каждого сервиса есть свой `README` файл, включающий информацию об его отдельном запуске
- все репозитории находятся в директории `services`
  
