from django.db import models

# Create your models here.

class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=50)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.album_name


class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    photo_data = models.BinaryField()
    caption = models.CharField(max_length=50)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption