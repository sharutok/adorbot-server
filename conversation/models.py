from django.db import models

import uuid

class ConversationModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=True)
    user_id = models.TextField(editable=True)
    instance_id = models.TextField(editable=True)
    questions=models.TextField(null=True)
    response = models.TextField(null=True)
    response_status=models.BooleanField()
    other_info = models.TextField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat_conversation"

class InstanceModel(models.Model):
    instance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user_id = models.TextField(editable=True)
    questions = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table="chat_instance"