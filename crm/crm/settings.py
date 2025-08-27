INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'customers',  # your app
    'django_crontab', 
]

# Cron jobs configuration
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]
