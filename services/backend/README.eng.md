# Backend
Monolithic web application for a single [frontend](https://github.com/emptybutton/Aqua/blob/main/services/frontend) of the system

## Deployment
To deploy this application locally:
1. clone this repository
2. run the service
3. set the `Postgres` table structure
4. initialize `MongoDB` cluster

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose -f Aqua/services/backend/docker-compose.dev.yml up
docker exec aqua-backend alembic -c src/auth/alembic.ini upgrade head
docker exec aqua-mongo1 mognosh -f /scripts/init-cluster.js
```

> [!NOTE]
> After such a launch, for greater speed, you can launch only using:
> ```bash
> docker compose -f Aqua/services/backend/docker-compose.dev.yml up
> ```

## API
<img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/api-view.png?raw=true"/>

## Design
Used approaches:
- Modular monolith
- Clean architecture
- Three-layer architecture
- DDD patterns

### General structure
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-relationship-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-relationship-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!NOTE]
> Interaction between modules occurs synchronously through facade calls, not through the network.

### Module structure
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-structure-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-structure-map/light-theme.png?raw=true">
</picture>

> [!IMPORTANT]
> Each module has its own individual structure, but at the moment (11.11.2024) this scheme can generalize the `auth` and `aqua` modules.
