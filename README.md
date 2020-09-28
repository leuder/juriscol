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

## Run model 
Run command to export to json file:
    
    scrapy crawl corteconstitucional -s HTTPCACHE_ENABLED=1  -o data.json