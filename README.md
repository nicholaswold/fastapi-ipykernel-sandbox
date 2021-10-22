# FastAPI IPyKernel Sandbox

This repository is a light-weight FastAPI project that is meant to provide a
wrapper around IPyKernel interactions. It is inspired by Jupyter Server, an open-source
project designed to provide a REST API for frontend clients to interact with a filesystem
and with compatible Jupyter kernels.

## Installation

This project uses Poetry to manage its dependencies. Poetry will install its dependencies
into an isolated virtual environment if you're not currently in one. If you are using a
virtualenv, it will detect that and treat the environment as its own.

1. Install a Python version manager such as [pyenv](https://github.com/pyenv/pyenv)
1. Ensure that you have Python 3.9.7 installed
1. `pip install poetry`
1. `poetry install`


## Running the Sandbox

The sandbox project has a few commands to help you get up and running. First, you should
run `poetry run migratedb` to create a local SQLite3 database file in the top-level directory.
This will create the database and automatically populate its schema with the currently
defined tables. Anytime you add a new table to the sandbox you will want to run this
command.

If you ever need to clear the existing tables for whatever reason, you can run `poetry run cleardb`.
This command will drop any table defined in the sandbox code if it exists in the DB. You
may need to run this if you are making alterations to existing database tables. Don't worry about
losing any important data!

To actually start the API server, you can run `poetry run sandbox`. That will start the web server,
listening on port 8000.