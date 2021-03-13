# To-do list app with Flask, Redis & VueJS.

A Todo app allowing user authentication and todos managements secured by JWT and deployable with Docker.

Deploy with `docker-compose -f docker-compose.yml up`, the JWT secret can be set in the `docker_compose.yml` file.


## API: Flask + Redis ![API Tests Status](https://github.com/qlamu/to-do-list_vue-flask-redis/workflows/API/badge.svg)

The API is vanilla Flask app with the dependencies kept as short a possible, it is divided like so:
- **blueprints**: Each blueprint correspond to a family of routes (`/lists`, `/todos`, etc.).
- **static** & **templates**: This is only used to serve Swagger UI (v44) that act as an interactive documentation (route `/doc`).
- **test**: A suite of tests running with `pytest`, covering most of the use cases of the API.
- **utils**: Contains the decorators (to request authentication, auto logs) and the `marshmallow` schemas used to validate the input to some routes.

For the Docker deployment the app is served through Gunicorn, a production friendly WSGI.

### Database structure

![Redis Structure Diagram](redis_structure.svg)


## Front: VueJS

The front is a static VueJS app with the following routes:
- **/**: The Home page with all the lists on the left side and a main panel with the todos of the selected list (empty, because no lsit is selected).
- **/:id**: Same thing, except the id corresponds the the currently selected list, and the main panel is then filled with the todos of the list `id`.
- **/login**: The login page
- **/signup**: The register page
- **/logs**: Public logs of everything that happens on the API in near real time.

For the Docker deployment the app is served through Nginx, a config file `nginx.conf` has been added to avoid unnatural 404 errors caused by the usage of History Mode for Vue's router.