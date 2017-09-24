from fabric.api import run, env, cd
from fabric.contrib.files import append
from escrutinio_social.local_settings import HOST_IP, HOST_USER

env.hosts = [HOST_IP]
env.user = HOST_USER


def manage(command):
    run("source /virtualenvs/escrutinio-ciudadano/bin/activate")
    with cd('/projects/escrutinio-ciudadano'):
        run(f"/virtualenvs/escrutinio-ciudadano/bin/python manage.py {command}")


def shell_plus():
    manage('shell_plus')


def dbbackup():
    manage('dbbackup -z')


def dbrestore():
    manage('dbrestore -z')


def append_to_local_settings(path):
    run("source /virtualenvs/escrutinio-ciudadano/bin/activate")
    with open(path) as ls:
        content = ls.read()
    with cd('/projects/escrutinio-ciudadano'):
        append('./escrutinio-ciudadano/local_settings.py', f'\n{content}')


def loaddata(fixture):
    run("source /virtualenvs/escrutinio-ciudadano/bin/activate")
    with cd('/projects/escrutinio-ciudadano'):
        run("git pull")
        run("/virtualenvs/escrutinio-ciudadano/bin/python manage.py loaddata fixtures/{}".format(fixture))


def deploy():
    run("source /virtualenvs/escrutinio-ciudadano/bin/activate")
    with cd('/projects/escrutinio-ciudadano'):
        run("git pull")
        run("supervisorctl restart escrutinio_social")


def full_deploy():
    run("source /virtualenvs/escrutinio-ciudadano/bin/activate")
    with cd('/projects/escrutinio-ciudadano'):
        run("git pull")
        run("/virtualenvs/escrutinio-ciudadano/bin/pip install -r requirements.txt")
        run("/virtualenvs/escrutinio-ciudadano/bin/python manage.py migrate")
        run("/virtualenvs/escrutinio-ciudadano/bin/python manage.py collectstatic --noinput")
        run("supervisorctl restart escrutinio_social")
