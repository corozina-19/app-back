from django.contrib.auth.models import User
from django.db import models


class TokenFirebase(models.Model):
    user = models.ForeignKey(User, related_name='user_token', on_delete=models.CASCADE)
    token = models.CharField(unique=True, max_length=250, blank=False, null=False)
    update_date = models.DateTimeField(auto_now=True, editable=True)

    def __unicode__(self):
        return u'user:{0} token:{1} '.format(self.user, self.token)

    def __str__(self):
        return f'user:{self.user} token:{self.token}'