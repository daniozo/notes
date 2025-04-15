from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    is_pinned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_pinned', '-updated_at']
    
    def __str__(self):
        return self.title
