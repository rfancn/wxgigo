from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    user = models.ForeignKey(User, null=True)
    open_id = models.CharField(max_length=128, db_index=True)
    union_id = models.CharField(max_length=128, db_index=True, null=True)
    telephone = models.CharField(max_length=11, db_index=True)
    nickname = models.CharField(max_length=128)
    headimg_url = models.CharField(max_length=256, null=True)
    # 0: unknown, 1: male, 2: female
    sex = models.PositiveSmallIntegerField(default=0)
    # QRCode ticket
    ticket = models.CharField(max_length=256, null=True)

    class Meta:
        db_table = 'apps_member'

