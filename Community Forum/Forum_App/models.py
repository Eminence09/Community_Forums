from django.db import models


class topic_info(models.Model):
    username = models.CharField(max_length=255, default='')
    system_name = models.CharField(max_length=255, default='')
    topic_names = models.CharField(max_length=1000)
    topic_description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.username or 'Unknown user'} - {self.system_name or 'Unknown system'}"


class TopicReply(models.Model):
    topic = models.ForeignKey(topic_info, on_delete=models.CASCADE, related_name='replies')
    username = models.CharField(max_length=255, default='')
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', 'id')

    def __str__(self):
        return f"Reply by {self.username or 'Unknown user'} on {self.topic.topic_names}"