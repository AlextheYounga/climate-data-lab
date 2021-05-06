import django
from django.apps import apps
import json
import redis
import sys
import os
from dotenv import load_dotenv
load_dotenv()
django.setup()


def rdb_schema():
    """
    This is the standard redis db schema for this app, built on key,value pairs.
    The keys are differentiated by tickers.


    # Climate Data
    'climate-'+date+'-temp'
    """

    key_roots = [
        'climate',
    ]
    
    return key_roots