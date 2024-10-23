from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from .functions import (
    get_by_id,
    post_by_id,
    chat_history_by_id,
    generate_response,
    validate_user,
    chat_history,
)

from cache.views import (find_key)
# Create your views here.


@api_view(['POST'])
def DATA_BY_ID(request, id):
    try:
        response = get_by_id(request, id)
        return Response({'status':200,"response":response})
    except Exception as e:
        print("Error in DATA_BY_ID", e)
        return Response({'status':400})


@api_view(['POST'])
def GENERATE_RESPONSE(request,id):
    try:
        chat_history=find_key(instance_id=request.data["instance_id"],user_id=id)
        response = generate_response(
            questions=request.data["questions"],
            chat_history=chat_history        
            )
        
        response['user_id']=str(id)
        response["response_status"] = False
        response["instance_id"] = request.data["instance_id"]
        response["other_info"] = json.dumps(response["meta_response"])
        _response={**response}
        response = post_by_id(response)
        return Response({'status':200,"response":{**response,**_response}})
    except Exception as e:
        print("Error",e)
        return Response({'status':400})

@api_view(['GET'])
def CHAT_HISTORY_BY_ID(request, id):
    try:
        match request.method:
            case "GET":
                response = chat_history_by_id(request, id)
                return Response({"status": 200, "response": response})
    except Exception as e:
        print("Error",e)
        return Response({'status':400})


# @api_view(['PUT'])
# def thumbs_down(request,id):
#     try:
#         pass
#     except Exception as e:
#         pass


@api_view(["POST"])
def VALIDATE_USER(request):
    try:
        response = validate_user(request)
        return Response(response)
    except Exception as e:
        print("Error", e)
        return Response({"status": 400})

@api_view(["GET"])
def HEALTH_CHECK(request):
    try:
        return Response({"status": 200})
    except Exception as e:
        print("Error", e)
        return Response({"status": 400})
