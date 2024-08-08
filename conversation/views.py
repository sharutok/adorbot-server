from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .functions import get_by_id, post_by_id, chat_history_by_id

# Create your views here.

@api_view(['GET','POST'])
def DATA_BY_ID(request,id):
    try:
        match request.method:
            case "GET":
                response = get_by_id(request, id)
                print(response)
            case "POST":
                response= post_by_id(request,id)
        return Response({'status':200,"response":response})
    except Exception as e:
        print("Error",e)
        return Response({'status':400})


@api_view(['GET'])
def CHAT_HISTORY_BY_ID(request,id):
    try:
        match request.method:
            case "GET":
                response=chat_history_by_id(request,id)
                return Response({'status':200,"response":response})
    except Exception as e:
        print("Error",e)
        return Response({'status':400})
