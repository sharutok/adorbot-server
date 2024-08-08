from conversation.models import ConversationModel, InstanceModel
from rest_framework import serializers


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationModel
        fields = "__all__"

class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceModel
        fields = "__all__"
