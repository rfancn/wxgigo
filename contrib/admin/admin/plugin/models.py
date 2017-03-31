from django.db import models

# Create your models here.
class WXMPPlugin(models.Model):
    class Meta:
        db_table = "wxmp_plugin"

    uuid = models.CharField(primary_key=True, verbose_name="UUID", max_length=32)
    name = models.CharField(verbose_name="Plugin Name", max_length=32)
    # match patter which used to match the keyword received from weixin client
    pattern = models.CharField(verbose_name="Match Pattern", max_length=128)
    version =  models.CharField(verbose_name="Plugin Version", max_length=16)
    enabled = models.BooleanField(verbose_name="Enabled")