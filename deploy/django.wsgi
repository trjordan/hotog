import os
import sys

# Make sure the path is in the pythonpath
path = '/deploy/hotog/'
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(path + 'hotog/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'hotog.settings_prod'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
