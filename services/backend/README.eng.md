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
docker exec aqua-backend alembic upgrade head
docker exec aqua-mongo1 mognosh -f /scripts/init-cluster.js
```

> [!NOTE]
> After such a launch, for greater speed, you can launch only using:
> ```bash
> docker compose -f Aqua/services/backend/docker-compose.dev.yml up
> ```

## API scheme
<img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/api-view.png?raw=true"/>

## Design
Used approaches:
- Modular monolith
- Clean architecture
- Some DDD patterns

### Modules
The system is divided into subsystems - modules, each of which represents an independent (or almost independent) application with its own external interface in the form of a facade.

#### Internal structure of modules
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-structure-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-structure-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!NOTE]
> In the context of internal layering of modules, when `A -> B` interacts, both `A` and `B` are on the `Periphery` layer for each other, namely, for `A`, `B` will be in the `Infrastructure periphery`, and for `B`, `A` will be in the `Presentation periphery`.

#### Interaction of modules
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-relationship-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/services/backend/assets/module-relationship-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!IMPORTANT]
> The interaction of modules occurs in a logically synchronous method, that is, a separate module must directly call another module without the use of message brokers or other things that provide events.
> 
> There is a special `Shared` module, it itself should not interact with other modules and have a façade, since other modules can interact with it as if it were the very part of the module that uses it. It is advisable to keep it as small as possible in order to prevent too much coupling between other modules, even if you have to write several pieces that (for now) completely repeat each other.
