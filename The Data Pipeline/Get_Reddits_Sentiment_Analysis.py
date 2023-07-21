"""
This script gets reddits titles from the reddit api 
and serve in the first step of the dockerized pipeline.
"""

from  pprint import pprint
from config import CONFIGURE
import requests
from requests.auth import HTTPBasicAuth

###Creating mongodb connection
from pymongo import MongoClient
import pandas as pd

# imports needed to build up 
# the connection to PostgrSQL container
from sqlalchemy import create_engine
from sqlalchemy import text

# Vader import
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()


## PREPARE AUTHENTIFICATION INFORMATION ##
## FOR REQUESTING A TEMPORARY ACCESS TOKEN ##
basic_auth = HTTPBasicAuth(
    username=CONFIGURE['APP_ID'],
    password=CONFIGURE['SECRET']
)

print(basic_auth)

GRANT_INFORMATION = dict(
    grant_type="password",
    username=CONFIGURE['REDDIT_USERNAME'], # REDDIT USERNAME
    password=CONFIGURE['REDDIT_PASSWORD'] # REDDIT PASSWORD
)

headers = {
    'User-Agent': "Chrome"
}

### POST REQUEST FOR ACCESS TOKEN

POST_URL = "https://www.reddit.com/api/v1/access_token"

access_post_response = requests.post(
    url=POST_URL,
    headers=headers,
    data=GRANT_INFORMATION,
    auth=basic_auth
).json()

#print(type(access_post_response),access_post_response)

### ADDING TO HEADERS THE Authorization KEY

headers['Authorization'] = access_post_response.get('token_type') + ' ' + access_post_response.get('access_token')

print(headers)

## Send a get request to download most popular (hot )Python subreddits title using the new headers.

topic = 'Python'
URL = f"https://oauth.reddit.com/r/{topic}/hot"

response = requests.get(
    url=URL,
    headers=headers
).json()

pprint(len(response.get('data').get('children')))
full_response = response.get('data').get('children')

#  mongo_dict = dict()

### POSTGRES STUFF###
# THE 🤚🏼 things needed to connect to PostgreSQL
PG_USER = 'postgres'
PG_PASSWORD = 'XXX'
PG_HOST = 'localhost'
PG_PORT = 5432 
PG_DB = 'postgres'

# Define connection string for PostrgreSQL
conn_str = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

# define a client for PostrgreSQL
pg_client = create_engine(conn_str)

# connect pg_client to PostgreSQL
pg_client_connect = pg_client.connect()

# define create_table query
create_table = """
DROP TABLE IF EXISTS score_reddits;
CREATE TABLE score_reddits (
    title VARCHAR(255),
    score numeric
);
"""
# execute create_table query with pg_client_connect and then commit
pg_client_connect.execute(text(create_table))
# pg_client_connect.commit()
######################

#create connection with mongodb (running a container)
#conn = 'reddit_container' #'mongodb://localhost:27017'
#client = MongoClient(conn)

#CRUD command
## Create, Read, Update, Delete
###Create.Done (Its running on my container already!)
#reddit = client.reddit_DB

# go through the full response and save each title with the corresponding id 

for post in full_response:
    id_ = post.get('data').get('id')
    title = post.get('data').get('title').replace("'", " ")
    #calculate the polarity score
    score= analyzer.polarity_scores(title)['compound']
    insert_query = f"""
    INSERT INTO score_reddits
    VALUES ('{title}', {score});
    """
    pg_client_connect.execute(text(insert_query))
    # pg_client_connect.commit()
    #mongo_dict[id_] = title
    #reddit.reddit_table.insert_one({id_:title})


