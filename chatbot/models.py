# chatbot_app/models.py
from django.db import models

class Conversation(models.Model):
    session_id = models.CharField(max_length=255, unique=True, db_index=True) # Ex: clé de session Django ou ID utilisateur
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.session_id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('model', 'Model')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"