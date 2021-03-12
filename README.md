# To-do list app with Flask, Redis & VueJS.

A Todo app allowing user authentication and todos managements secured by JWT and deployable with Docker.

Deploy with `docker-compose -f docker-compose.yml up`, the JWT secret can be set in the `docker_compose.yml` file.


## API: Flask + Redis ![API Tests Status](https://github.com/qlamu/to-do-list_vue-flask-redis/workflows/API/badge.svg)

The API is vanilla Flask app with the dependencies kept as short a possible, it is divided like so:
- **blueprints**: Each blueprint correspond to a family of routes (`/lists`, `/todos`, etc.).
- **static** & **templates**: This is only used to serve Swagger UI (v44) that act as an interactive documentation (route `/doc`).
- **test**: A suite of tests running with `pytest`, covering most of the use cases of the API.
- **utils**: Contains the decorators (to request authentication, auto logs) and the `marshmallow` schemas used to validate the input to some routes.

### Database structure

![Redis Structure Diagram](redis_structure.svg)