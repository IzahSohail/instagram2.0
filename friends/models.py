from django.db import models
from django.db.models import UniqueConstraint
from user.models import User

# Define the Friends model, which extends Django's Model class
class Friends(models.Model):
    user_a = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name = 'friend_a')
    user_b = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name = 'friend_b')
    
    # Defining a primary
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user_a', 'user_b'], name='unique_friendship')
        ]

    def __str__(self):
        return [self.user_a, self.user_b]