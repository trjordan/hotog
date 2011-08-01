import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'hotog.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Make sure the path is in the pythonpath
path = '/deploy/hotog/hotog/'
if path not in sys.path:
    sys.path.append(path)
