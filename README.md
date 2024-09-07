<h1><img src="https://github.com/emptybutton/Aqua/blob/main/assets/logo.png?raw=true" width="32" height="32"/> Aqua</h1>
Приложение для отслеживания вашего водного баланса.

<span></span>

> [English version](https://github.com/emptybutton/Aqua/blob/main/README.eng.md) of this README file.

## Как запустить
Что бы запустить локально:
1. склонируйте этот репозиторий
2. установите структуру БД
3. запустите все сервисы внутри `docker`

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose -f Aqua/services/backend/docker-compose.dev.yml run aqua alembic upgrade head
docker compose -f Aqua/docker-compose.dev.yml up
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
  
