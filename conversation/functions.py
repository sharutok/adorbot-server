from .serializers import ConversationSerializer,InstanceSerializer
from django.db import connection
import json

def get_by_id(request, id):
    try:
        sql = """
        select
        id,
        user_id,
        questions,
        response
        from
            conversation c
        where
            user_id = '{}';
        """.format(id)
        
        data=execute_select_sql(sql)
        
        return data
    except Exception as e:
        print(e)
        return None


def post_by_id(request, id):
    try:
        if request.data['instance_id']:
            serializers = ConversationSerializer(data=request.data)
            if serializers.is_valid():
                obj = serializers.save()
                return ConversationSerializer(obj).data
            else:
                raise Exception("error in saving 1",serializers.errors)
        else:
            instance = InstanceSerializer(
                data={
                    "user_id": request.data["user_id"],
                    "questions": request.data["questions"],
                }
            )
            if instance.is_valid():
                obj=instance.save()
                request.data['instance_id']=InstanceSerializer(obj).data["instance_id"]
                converstion=ConversationSerializer(data=request.data)
                if converstion.is_valid():
                    obj = converstion.save()
                    return ConversationSerializer(obj).data
                else:
                    raise Exception("error in saving 2",converstion.errors)

    except Exception as e:
        print("error in saving 3",e)
        return None


def chat_history_by_id(request, id):
    try:
        sql = """select instance_id ,user_id ,questions from "instance" where user_id ='{}'""".format(id)
        data = execute_select_sql(sql)
        print(data)
        return data
    except Exception as e:
        print("chat_history_by_id",e)
        return None


def execute_select_sql(sql):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            rows = [
                dict(zip([col[0] for col in cursor.description], row)) for row in results
            ]
        return rows
    except Exception as e:
        print("execute_select_sql",e)
        return None
