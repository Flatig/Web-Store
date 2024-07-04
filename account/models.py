from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_photo/user_<id>_<username>/<filename>
    return 'profile_photo/id:{0}_{1}/{2}'.format(instance.user.id, instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, default='default.jpg')
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
