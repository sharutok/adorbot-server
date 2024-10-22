from django.urls import path, include

from conversation.views import (
    DATA_BY_ID,
    CHAT_HISTORY_BY_ID,
    GENERATE_RESPONSE,
    VALIDATE_USER,
    HEALTH_CHECK
)

urlpatterns = [
    path("chats-by-id/<uuid:id>", DATA_BY_ID, name="DATA-BY-ID"),
    path("generate-response/<uuid:id>", GENERATE_RESPONSE, name="GENERATE-RESPONSE"),
    path("history/<uuid:id>", CHAT_HISTORY_BY_ID, name="CHAT-HISTORY-BY-ID"),
    path("validate/login/user", VALIDATE_USER, name="VALIDATE-USER"),
    path("health-check",HEALTH_CHECK,name="health-check")
]
