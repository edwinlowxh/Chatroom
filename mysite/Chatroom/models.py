from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class groups(models.Model):
    group_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.group_name

class group_members(models.Model):
    group = models.ForeignKey('groups', on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering=['group']
        
    def __str__(self):
        return self.group.group_name

class friend_request(models.Model):
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requestor")
    requestee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requestee")

class friend(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initiator")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
