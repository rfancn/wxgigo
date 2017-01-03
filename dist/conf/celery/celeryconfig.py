BROKER_URL='redis://guest@${wxgigo_dbhost_ip}:6379//'
CELERY_RESULT_BACKEND='redis://${wxgigo_dbhost_ip}:6379/0'
CELERY_TASK_SERIALIZER='json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TIMEZONE='Asia/Shanghai'
CELERY_ENABLE_UTC=True
#CELERYD_TASK_TIME_LIMIT=30

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'update-access_token': {
        'task': 'api.basic.update_access_token',
        'schedule': timedelta(seconds=300),
    },
}

#######################
# customized opttions #
#######################
PLUGINS_HOME='${wxgigo_plugins_home}'


