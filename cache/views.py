from django.shortcuts import render
from adorBotProject.settings import r
import json

def insert_data(user_id,instance_id,data):
    key="{}:{}".format(user_id,instance_id)
    try:
        # if not len(find_key(user_id, instance_id)):
            for d in data:
                r.rpush(key,json.dumps(d))
                r.expire(key,3000)
        # else:
        #     print("already present")
    except Exception as e:
        print(e)


def remove_old_conversation_singular(user_id, instance_id):
    key = "{}:{}".format(user_id, instance_id)
    try:
        r.lpop(key)
    except Exception as e:
        print(e)


def add_new_conversation_singular(user_id,instance_id,data):
    key="{}:{}".format(user_id,instance_id)
    try:
        r.rpush(key,json.dumps(data))
    except Exception as e:
        print(e)


def find_key(user_id, instance_id):
    key="{}:{}".format(user_id,instance_id)
    try:
        is_there = r.lrange(key, 0, -1)
        return is_there
    except Exception as e:
        print(e)


def popAndInsert(user_id, instance_id, data):
    _find_key=find_key(user_id, instance_id)
    if len(_find_key) <= 2:
        insert_data(user_id, instance_id, data)
    else:
        remove_old_conversation_singular(user_id,instance_id)
        insert_data(user_id, instance_id, data)
    return _find_key
