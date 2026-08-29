from django.db import models


class topic_info(models.Model):
    username = models.CharField(max_length=255, default='')
    system_name = models.CharField(max_length=255, default='')
    topic_names = models.CharField(max_length=1000)
    topic_description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.username or 'Unknown user'} - {self.system_name or 'Unknown system'}"