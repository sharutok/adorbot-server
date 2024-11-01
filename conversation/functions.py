import os
from .serializers import ConversationSerializer, InstanceSerializer
from django.db import connection
import json
import requests
from cache.views import (
    insert_data,
    remove_old_conversation_singular,
    add_new_conversation_singular,
    find_key,
    popAndInsert,
)


def get_by_id(request, id):
    try:
        sql = """select id, user_id, questions, response from chat_conversation where user_id = '{}' and instance_id='{}'  order by created_at asc ;""".format(id, request.data["instance_id"])
        data = execute_select_sql(sql)
        _data = []
        for x in data[-3:]:
            _data.append(
                [x["questions"], x["response"]]
            )
        popAndInsert(user_id=id,instance_id=request.data["instance_id"],data=_data)
        return {"last_3_conversation":_data,"data": data }
    except Exception as e:
        print(e)
        return None


def post_by_id(request):
    try:
        if request["instance_id"]:
            serializers = ConversationSerializer(data=request)
            if serializers.is_valid():
                obj = serializers.save()
                chat_history=popAndInsert(data=[[ConversationSerializer(obj).data["questions"],ConversationSerializer(obj).data["response"],]],instance_id=request["instance_id"],user_id=ConversationSerializer(obj).data["user_id"])
                return {
                    **ConversationSerializer(obj).data,
                    "chat_history": chat_history,
                }
            else:
                print("error in saving 1", serializers.errors)
                raise Exception("error in saving 1", serializers.errors)
        else:
            instance = InstanceSerializer(
                data={
                    "user_id": request["user_id"],
                    "questions": request["questions"],
                }
            )
            if instance.is_valid():
                obj = instance.save()
                request["instance_id"]=InstanceSerializer(obj).data["instance_id"]
                conversation = ConversationSerializer(data=request)
                if conversation.is_valid():
                    obj = conversation.save()
                    chat_history=popAndInsert(data=[[ConversationSerializer(obj).data["questions"],ConversationSerializer(obj).data["response"]]],instance_id=request["instance_id"],user_id=ConversationSerializer(obj).data["user_id"])
                    return {
                        **ConversationSerializer(obj).data,
                        "chat_history": chat_history,
                        "instance_id":request["instance_id"]
                    }
                else:
                    print("error in saving 2", conversation.errors)
                    raise Exception("error in saving 2", conversation.errors)

    except Exception as e:
        print("error in saving 3", e)
        return None

def chat_history_by_id(request, id):
    try:
        print(id)
        sql = """select instance_id,questions from chat_instance where user_id ='{}' order by created_at asc""".format(
            id
        )
        data = execute_select_sql(sql)

        return data
    except Exception as e:
        print("chat_history_by_id", e)
        return None

def generate_response(questions,chat_history):
    try:
        url = "{}/generate/text".format(os.environ.get("MICROSERVICE_API_BASE_URL"))
        response = requests.request(
            "POST",
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"questions": questions,"chat_history":chat_history}),
        )
        return response.json()
    except Exception as e:
        print("error in generating resposne", e)
        return None

def execute_select_sql(sql):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            rows = [
                dict(zip([col[0] for col in cursor.description], row))
                for row in results
            ]
        return rows
    except Exception as e:
        print("execute_select_sql", e)
        return None


def validate_user(request):
    try:
        email = request.data["email"]
        password = request.data["password"]
        if email and password:
            url = "{}/user-manage/login/check/".format(
                os.environ.get("ADORHUB_API_BASE_URL_DEV")
            )
            response = requests.request(
                "POST",
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "email": email,
                        "password": password,
                        "prefix": "@adorians.com",
                        "remember_me": False,
                        "mode":"bot"
                    }
                ),
            )
            return json.loads(response.text)
        else:
            print("no email or password")
    except Exception as e:
        return{"status":400}
        print(e)


def chat_history(instance_id, user_id):
    try:
        return find_key(instance_id,user_id)
    except Exception as e:
        print("error in chat_history",e)