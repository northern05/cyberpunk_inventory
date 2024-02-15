# Setup and run
Repo https://github.com/northern05/cyberpunk_inventory.git

1. Install Docker: https://docs.docker.com/engine/install/ubuntu/
2. Create docker subnet: docker network create dev --subnet=172.31.0.0/16
3. Run sh script from repo "deploy.sh": sh deploy.sh
4. Open http://127.0.0.1:6016/docs# - docs endpoint


## API

### Fast API REST endpoints

**items/views.py** - CRUD endpoints for Items.

**items/schemas.py** - Schemas for CRUD Items.

**items/crud.py** - service to interact with Item. 

### Core

**models** - directory with files to setup connection with database, setup tables and models in it.

## Tests

**test_main.py** - tests for REST API

## Deploy

**.docker** - directory with docker composes for postgresql and app

**.envs** - directory with local variables