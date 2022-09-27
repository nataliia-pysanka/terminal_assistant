# Terminal assistans (pure Python, SQLAlchemy, Alembic)
Create your personal terminal contact book. You could save:
* name and surname of person
* list of phone numbers
* list of emails
* date of birth
* adress
* group of contact

### How to use:
Terminal assistant works with arguments in command line.
You could call "help" to view all options:
```bash
python3 main.py -h
```
You see next:
```bash
options:
  -h, --help            show this help message and exit
  --action ACTION, -a ACTION
                        Command: create, update, list, remove
  --search SEARCH, -s SEARCH
                        Command: name, date, groups
  --birth [BIRTH], -b [BIRTH]
  --seed SEED, -se SEED
```
To create/update/list/remove records from contact book use one of these arguments with option --action or -a.
```bash
python3 main.py --action create
python3 main.py --action update
python3 main.py --action list
python3 main.py --action remove
```
To search records by name/date/groups use one of these arguments with option --search or -s.
```bash
python3 main.py --search name
python3 main.py --search date
python3 main.py --search groups
```
To find persons who have birthday today use option --birth or -b. Also, you could write other date in format '%d.%m'
```bash
python3 main.py --birth 26.09
```
To seed database use argument --seed or -se. You could input number of contacts. By default, it's 50. 
```bash
python3 main.py --seed 10
```
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
# Make migrations
make migr
# Run the script
python3 main.py -h
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
