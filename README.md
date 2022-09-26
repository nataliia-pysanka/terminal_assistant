# Terminal assistans
Create database which consist of:
* table of students
* table of subjects
* table of professors


## Synopsis

* `alembic==1.8.1`
* `faker==14.2.0`
* `greenlet==1.1.3`
* `mako==1.2.2`
* `markupsafe==2.1.1`
* `psycopg2-binary==2.9.3`
* `python-dateutil==2.8.2`
* `python-dotenv==0.21.0`
* `six==1.16.0`
* `sqlalchemy==1.4.41`

## Installation

### Requirements

Docker-compose (https://docs.docker.com/compose/)

### Deploy

```bash
# Clone this repository using git
git clone git@github.com:nataliia-pysanka/terminal_assistant.git
# Change the directory
cd terminal_assistant
# Create virtual enviroment
make venv
# Activate virtual env
source venv/bin/activate
# Install requirements
make req
# Build and run the container
make up
# Create database
make db
# Run the script
make run
```

### Destroy

```bash
# Delete database
make drop
# Stop docker-container
make stop
# Clear the container
make clear
```
