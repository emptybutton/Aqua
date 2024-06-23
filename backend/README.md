## I am from England
[Give me english text](https://github.com/emptybutton/Aqua/blob/main/backend/README.eng.md).

## Как запустить
Что бы запустить локально:
1. склонируйте этот репозиторий
2. запустите внутри `docker`

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose --project-directory ./Aqua/backend up
```

## API схема
<img src="https://github.com/emptybutton/Aqua/blob/main/backend/assets/api-view.png?raw=true"/>

## Дизайн
Используемые подходы:
- Модульный монолит
- Чистая архитектура
- DDD

### Модули
Система разделена на подсистемы — модули, каждый из которых представляет собой независимое (или почти независимое) приложение со своим внешним интерфейсом в виде фасада.

#### Внутреннее устроиство модулей
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/backend/assets/module-structure-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/backend/assets/module-structure-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!NOTE]
> В контексте внутреннего разделения модулей на слои, при взаимодействии `A -> B`, как `A`, так и `B`, друг для друга находятся на слое фреймворков (Frameworks), а именно для `A`, `B` будет находиться в фреймворках инфраструктуры (Infrastructure frameworks), а для `B`, `A` будет находиться в фреймворках представления (Presentation frameworks).

#### Взаимодействие модулей
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/emptybutton/Aqua/blob/main/backend/assets/module-relationship-map/dark-theme.png?raw=true">
 <img src="https://github.com/emptybutton/Aqua/blob/main/backend/assets/module-relationship-map/light-theme.png?raw=true">
</picture>

<span></sman>

> [!IMPORTANT]
> Взаимодействие модулей происходит логически синхронным методом, т. е. отдельный модуль должен напрямую вызывать другой модуль без использоваия брокеров сообщений или других вещей предоставляющие эвенты.
> 
> Существует специальный модуль `Shared`, сам он не должен взаимодействовать с другими модулями и иметь фасада, так как другие модули могут взаимодействовать с ним так, как будто он является самой частью модуля, который его использует. Желательно держать его как можно меньше, что бы предотвратить большую связность между другими модулями, даже если придется написать несколько штук, которые (пока что) полностью повторяют друг друга.
