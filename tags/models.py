from django.db import models
from album.models import Album, Photo
from django.db.models import UniqueConstraint


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, unique = True)

    def __str__(self):
        return self.description

class PhotoTagMapping(models.Model):
    tag   = models.ForeignKey(Tag, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['photo', 'tag'], name='unique_photo_tag_mapping')
        ]
    
    def __str__(self):
        return [self.tag, self.photo]