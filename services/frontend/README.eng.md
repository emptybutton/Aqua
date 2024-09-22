# Frontend

The only service interacting with the end user of the entire system, running in the browser.
Needed solely as a bridge between the end user and the rest of the system.

Contains only the logic of interaction with the [backend](https://github.com/emptybutton/Aqua/blob/main/services/backend) and visualization of the results obtained in this way.

## Deployment
To deploy locally:
1. clone this repository
2. run the service inside `docker`

```bash
git clone https://github.com/emptybutton/Aqua.git
docker compose -f Aqua/services/frontend/docker-compose.dev.yml up
```

> [!WARNING]
> Since this is a delegating service, remember that in such an independent deployment almost all interactions will fail.
> 
> For successful interactions, it is highly recommended to [deploy the service with the rest of the system](https://github.com/emptybutton/Aqua/blob/main/README.eng.md#deployment).

<details>
  <summary><h2>Gallery</h2></summary>
  <table>
    <tr>
      <th>Login Page</th>
      <th>Registration Page</th>
    </tr>
    <tr>
      <td><img src="https://github.com/emptybutton/Aqua/blob/main/services/frontend/assets/pages/login-page-view.jpg?raw=true" width="240"/></td>
      <td><img src="https://github.com/emptybutton/Aqua/blob/main/services/frontend/assets/pages/registration-page-view.jpg?raw=true" width="240"/></td>
    </tr>
  </table>
</details>

## Stack
- `TS` as the main language for scripts
- `HTML` for prepared pages
- `SASS` as `SCSS` for page styles
- `Nginx` as a server for distributing static content and redirecting

## Design
Approaches used:
- Clean architecture
- Some DDD patterns
- Multidomain

### Domains
Usually only one domain layer is allocated, but the application of this service operates several domains at once.
The domains themselves do not interact with each other.

In total there are the following domains:
- `water-recording` - domain for replenishing users' water balance
- `access` - domain for identification and access to accounts
- `shared` - domain for basic things in the form of `ID`, basic error classes, and a couple of utilities that compensate for the language and operate on other basic things in the domain

This service is mostly inclined to `IO` operations rather than internal calculations due to its nature, so the listed domains are thin and have little or no logic, which is why complex patterns were not taken to organize it, instead entities are represented as simple DS.
