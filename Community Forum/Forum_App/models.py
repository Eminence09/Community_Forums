from django.db import models
import getpass
import socket


class topic_info(models.Model):
    username = getpass.getuser()
    system_name = socket.gethostname()
    
    topic_names = models.CharField(max_length=1000)
    topic_description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.username} - {self.system_name}"

# class forum_post(models.Model):
#     forum = models.CharField(max_length=1000)