import json
import redis
from datetime import datetime, date, timedelta
import sys
import os



def rdb_save_output(output):
    r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    r.set('lab-last-output', json.dumps(output))
    return True


def fetch_last_output():
    r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    op = r.get('lab-last-output')
    if (op):
        return json.loads(op)

    return False
