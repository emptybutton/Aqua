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
docker exec aqua-backend alembic upgrade head
docker exec aqua-mongo1 mognosh -f /scripts/init-cluster.js
```

> [!NOTE]
> После такого запуска, для большей скорости, можете запускать только при помощи:
> ```bash
> docker compose -f Aqua/services/backend/docker-compose.dev.yml up
> ```

## API схема
<img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/api-view.png?raw=true"/>

## Дизайн
Используемые подходы:
- Модульный монолит
- Чистая архитектура
- Некоторые паттерны DDD

### Модули
Система разделена на подсистемы — модули, каждый из которых представляет собой независимое (или почти независимое) приложение со своим внешним интерфейсом в виде фасада.

#### Внутреннее устроиство модулей
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-structure-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-structure-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!NOTE]
> В контексте внутреннего разделения модулей на слои, при взаимодействии `A -> B`, как `A`, так и `B`, друг для друга находятся на слое переферий (`Periphery`), а именно для `A`, `B` будет находиться в переферии инфраструктуры (`Infrastructure periphery`), а для `B`, `A` будет находиться в переферии представления (`Presentation periphery`).

#### Взаимодействие модулей
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-relationship-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-relationship-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!IMPORTANT]
> Взаимодействие модулей происходит логически синхронным методом, т. е. отдельный модуль должен напрямую вызывать другой модуль без использоваия брокеров сообщений или других вещей предоставляющие эвенты.
> 
> Существует специальный модуль `Shared`, сам он не должен взаимодействовать с другими модулями и иметь фасада, так как другие модули могут взаимодействовать с ним так, как будто он является самой частью модуля, который его использует. Желательно держать его как можно меньше, что бы предотвратить большую связность между другими модулями, даже если придется написать несколько штук, которые (пока что) полностью повторяют друг друга.
