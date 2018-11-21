from fabric import task
import time

@task
def build_application(c):

    # create python package
    if not c.local('python setup.py sdist --formats=gztar', warn=True).failed:
        filename = '{}.tar.gz'.format(c.local('python setup.py --fullname').stdout.strip())

        application_folder = c.local('python setup.py --name').stdout.strip().lower()

        # upload package to server
        c.put('dist/{}'.format(filename), '/tmp/{}'.format(filename))

        # first deployment
        if c.run('[ ! -d "/var/www/{}/env/bin/pip" ] && echo "True"'
                         .format(application_folder)).stdout.strip() == 'True':

            # create user
            usergroup = username = 'www-{}'.format(application_folder)
            c.run('useradd -r -M -U -s /sbin/nologin {}'.format(username))

            # create folder
            c.run('mkdir /var/www/{}'.format(application_folder))

            # create virtual env
            c.run('python3 -m venv /var/www/{}/env'.format(application_folder))

            # update pip
            c.run('/var/www/{}/env/bin/pip install --upgrade pip'.format(application_folder))

            # upload the config files
            c.put('config/config.cfg', '/var/www/{}'.format(application_folder))
            c.put('config/uwsgi_params', '/var/www/{}'.format(application_folder))

        # install application in venv
        c.run('/var/www/{}/env/bin/pip install /tmp/{}'.format(application_folder, filename))

        # change ownership
        c.run('chown -R {}:{} /var/www/{}'.format(username, usergroup, application_folder))

        # update the uwsgi configuration (symlink based on template.ini)
        c.run('ln -s /etc/uwsgi/apps-available/template.ini /etc/uwsgi/vassals/{}.ini'.format(application_folder))

        # update the ngix configuration
        c.put('dist/{}'.format(filename), '/tmp/{}'.format(filename))

@task
def cleanup_application(c):

    application_folder = c.local('python setup.py --name').stdout.strip().lower()

    # delete symlink
    c.run('unlink /etc/uwsgi/vassals/{}.ini'.format(application_folder))

    # wait until application is shut down by the emperor
    time.sleep(5)

    # delete folders
    c.run('rm -r /var/www/{}'.format(application_folder))

    # delete users
    username = 'www-{}'.format(application_folder)
    c.run('userdel {}'.format(username))



