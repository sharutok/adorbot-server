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

# Create your views here.


@api_view(['POST'])
def DATA_BY_ID(request, id):
    try:
        response = get_by_id(request, id)
        return Response({'status':200,"response":response})
    except Exception as e:
        print("Error",e)
        return Response({'status':400})


@api_view(['POST'])
def GENERATE_RESPONSE(request,id):
    try:
        response = generate_response(
            questions=request.data["questions"]
        )
        response['user_id']=str(id)
        response["response_status"] = False
        response["other_info"] = json.dumps(response["meta_response"])
        response["instance_id"] = request.data["instance_id"]
        _response={**response}
        response = post_by_id(response)
        return Response({'status':200,"response":{**response,**_response}})
    except Exception as e:
        print("Error",e)
        return Response({'status':400})

@api_view(['GET'])
def CHAT_HISTORY_BY_ID(request, id):
    print('CHAT_HISTORY_BY_ID')
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
        print(request)
        response = validate_user(request)
        return Response({"status": 200, "response": response})
    except Exception as e:
        print("Error", e)
        return Response({"status": 400})
