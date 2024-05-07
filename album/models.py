from django.db import models
import base64

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
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, related_name='owned_photos')  # Added a custom related_name because it had a clash

    def __str__(self):
        return self.caption
    


class Photo_likes(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " likes " + self.photo.caption