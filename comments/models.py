from django.db import models

# Create your models here.
from user.models import User
from album.models import Photo

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.CharField(max_length=200)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text