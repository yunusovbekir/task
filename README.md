# Vehicle finder app
#### The app currenly is online on https://vehicle-app-task.herokuapp.com


## Installation - on Docker

```bash
# clone repo to your machine
git clone git@github.com:yunusovbekir/task.git
```

## Usage

```bash
# run with docker. after that it will be available on http://localhost:8000
docker-compose up --build

# run tests
docker-compose -f bin/docker/docker-compose.dev.yaml run --rm web sh -c "./manage.py test"

# run linting
docker-compose -f bin/docker/docker-compose.dev.yaml run --rm web sh -c "flake8"
```