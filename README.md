# Juriscol 

## Container

### Docker-compose

Run command to create image:

    docker-compose bulid

Run serivices image:

    docker-compose up

## Local

### Virtual env

python -m venv env
source env/bin/activate

### Requirements

Install them from `requirements.txt`:

    pip install -r requirements.txt

Install spacy:
    
    python -m spacy download es_core_news_sm

## Run crawl 
Run in shell command to export to json file:
    
    scrapy crawl corteconstitucional -s HTTPCACHE_ENABLED=1  -o data.json

Run command to export to json file between 2009 and 2019:
    scrapy crawl corteconstitucional -s HTTPCACHE_ENABLED=1 -a anios_init=9 -a anios_limit=19

## Run MONGO
Create file called .env in folder juriscol with next varialbes

    - MONGO_USER=user
    - MONGO_PASS=pass
    - MONGO_HOST=host(ip:port)
    - MONGO_DB=db

The data is store in sentence collection.

Run in shell:

    scrapy crawl corteconstitucional -s HTTPCACHE_ENABLED=1 -a anios_init=9 -a anios_limit=19

The data is not update, the data is append.