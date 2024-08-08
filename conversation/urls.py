from django.urls import path, include
from conversation.views import DATA_BY_ID, CHAT_HISTORY_BY_ID

urlpatterns = [
    path("chats-by-id/<uuid:id>/", DATA_BY_ID, name="DATA-BY-ID"),
    path("history/<uuid:id>/", CHAT_HISTORY_BY_ID, name="CHAT-HISTORY-BY-ID"),
]
