from fabric.api import run, sudo, put
from fabric.context_managers import prefix, cd
from fabric.contrib.files import exists

deploy_user = 'ubuntu'

def deploy():
    packages = ['apache2', 'git-core', 'libapache2-mod-wsgi', 'python-setuptools', 'sqlite3']
    apt_install(packages)
    
    source()
    venv()
    apache()
    db()

def source():
    'Check out repo'
    if not exists('/deploy'):
        sudo('mkdir /deploy')
    if exists('/deploy/hotog'):
        sudo('rm -rf /deploy/hotog')
    run('git clone git://github.com/trjordan/hotog.git /deploy/hotog')
    sudo('chown %s:www-data /deploy/hotog' % deploy_user)

def venv():
    'Install venv'
    sudo('easy_install virtualenv')
    sudo('easy_install pip')
    sudo('virtualenv /venv/')
    sudo('chown %s:%s /venv' % (deploy_user, deploy_user))
    with prefix('. /venv/bin/activate'):
        run('pip install -U -r /deploy/hotog/deploy/requirements.txt')

def apache():
    'Set up and restart apache'
    put('.htaccess', '/var/www/.htaccess', use_sudo=True)
    put('.htpasswd', '/var/www/.htpasswd', use_sudo=True)
    put('default', '/etc/apache2/sites-available/default', use_sudo=True)

    sudo('service apache2 restart')

def db():
    'Creates our SQLite3 DB, if not already there.'
    if not exists('/deploy/hotog.db'):
        with cd('/deploy/hotog/hotog'):
            with prefix('. /venv/bin/activate'):
                run('python manage.py syncdb')
                run('mv hotog.db /deploy/')
        with cd('/deploy'):
            sudo('chgrp www-data hotog.db')
            sudo('chmod g+w hotog.db')

##############################
# Utils
##############################

def apt_install(packages):
    sudo('apt-get update')
    sudo('apt-get install %s' % ' '.join(packages))
