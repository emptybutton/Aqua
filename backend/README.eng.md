## Deployment
To deploy this application locally:
1. clone this repository
2. initialize and run it within `docker`

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose --project-directory ./Aqua/backend run aqua ash ./scripts/init-and-start.sh
```

> [!TIP]
> After initialization, for faster startup speed, you can launch using:
> ```bash
> docker compose --project-directory ./Aqua/backend up
> ```

## API scheme
<img src="https://github.com/emptybutton/Aqua/blob/main/backend/assets/api-view.png?raw=true"/>

## Design
Used approaches:
- Modular monolith
- Clean architecture
- DDD

### Modules
The system is divided into subsystems - modules, each of which represents an independent (or almost independent) application with its own external interface in the form of a facade.

#### Internal structure of modules
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/backend/assets/module-structure-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/backend/assets/module-structure-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!NOTE]
> In the context of the internal division of modules into layers, when interacting `A -> B`, both `A` and `B` for each other are on the framework layer, namely for `A`, `B` will be in the infrastructure frameworks, and for `B`, `A` will be in the presentation frameworks.

#### Interaction of modules
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/backend/assets/module-relationship-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/backend/assets/module-relationship-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!IMPORTANT]
> The interaction of modules occurs in a logically synchronous method, that is, a separate module must directly call another module without the use of message brokers or other things that provide events.
> 
> There is a special `Shared` module, it itself should not interact with other modules and have a façade, since other modules can interact with it as if it were the very part of the module that uses it. It is advisable to keep it as small as possible in order to prevent too much coupling between other modules, even if you have to write several pieces that (for now) completely repeat each other.
