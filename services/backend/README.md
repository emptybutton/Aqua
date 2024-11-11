# Backend
> [English version](https://github.com/emptybutton/Aqua/blob/main/services/backend/README.eng.md) of this README file.
___

Монолитное веб приложение для единственного [фронтенда](https://github.com/emptybutton/Aqua/blob/main/services/frontend) системы.

## Как запустить
Что бы запустить локально:
1. склонируйте этот репозиторий
2. запустите сервис
3. установите структуру таблиц `Postgres`
4. инициализируйте кластер `MongoDB`

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose -f Aqua/services/backend/docker-compose.dev.yml up
docker exec aqua-backend alembic -c src/auth/alembic.ini upgrade head
docker exec aqua-mongo1 mognosh -f /scripts/init-cluster.js
```

> [!NOTE]
> После такого запуска, для большей скорости, можете запускать только при помощи:
> ```bash
> docker compose -f Aqua/services/backend/docker-compose.dev.yml up
> ```

## API
<img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/api-view.png?raw=true"/>

## Архитектура
Используемые подходы:
- Модульный монолит
- Чистая архитектура
- Трехслойная архитектура
- Паттерны DDD

### Общая структура
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-relationship-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-relationship-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!NOTE]
> Взаимодействие модулей происходит синхронным образом через вызовы фасадов, не через сеть.

### Структура модуля
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-structure-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-structure-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!IMPORTANT]
> Каждый модуль имеет свою индивидуальную структуру, но на данный момент (11.11.2024) эта схема может обобщить модули `auth` и `aqua`.
