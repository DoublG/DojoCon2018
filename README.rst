Webhook
=======
The webhook application was build for the *EnviromentalSensor* project, presented on DojoCon2018 (Belgium).
I acts as an entrypoint to a internal RabbitMQ server.


Configuration
-------------
Configuration is loaded via a configuration file supplied
via the APP_SETTINGS environment variable.

=========================== =========================================
Configuration name          Description
=========================== =========================================
*GOOGLE_KEY*                Google API key
*API_KEY*                   "API Password" for webhook authorisation
*RABBITMQ_HOST*             RabbitMQ host ip
*RABBITMQ_USER*             RabbitMQ username
*RABBITMQ_PWD*              RabbitMQ password
*RABBITMQ_EXCHANGE*         RabbitMQ exchange name
*RABBITMQ_EXCHANGE_TYPE*    RabbitMQ exchange type
=========================== =========================================

URL's
-----
All url's use the POST method. The method only returns a success message.
The "real" response is published under *RABBITMQ_EXCHANGE*
with routing key *<routing_key>*.

=========================== ==========================================
Configuration name          Description
=========================== ==========================================
*/<routing_key>/street*     Get the nearest street
*/<routing_key>/geo*        Get the location based on GSM network info
*/<routing_key>*            Publish JSON to RabbitMQ exchange
=========================== ==========================================


Authorisation
-------------
All url's are protected by a simple API key, for every call you need to
supply this key. 

============= ==================
Name          Location
============= ==================
*api_key*     GET HTTP attribute
*X-API-Key*   HTTP Header
*X-API-KEY*   Cookie name
============= ==================

Request format
--------------
/<routing_key>/geo
------------------
**Example geo request:** ::

	{
	  "homeMobileCountryCode": 206,
	  "homeMobileNetworkCode": 1,
	  "considerIp": false,
	  "carrier": "Proximus",
	  "cellTowers": [
		{
		  "cellId": 66674698,
		  "locationAreaCode": 3024,
		  "mobileCountryCode": 206,
		  "mobileNetworkCode": 1
		},
		{
		  "cellId": 46190596,
		  "locationAreaCode": 3052,
		  "mobileCountryCode": 206,
		  "mobileNetworkCode": 1
		},
		{
		  "cellId": 21409538,
		  "locationAreaCode": 3052,
		  "mobileCountryCode": 206,
		  "mobileNetworkCode": 1
		}
	  ]
	}


/<routing_key>/street
---------------------
**Example street request:** ::

	{'long': 4.8367074, 'lat': 51.321642499999996 }

Server config files
-------------------
Backend server configuration
----------------------------
**/etc/ngix/ngix.conf** ::

    user www-data;
    worker_processes auto;
    pid /run/nginx.pid;

    events {
            worker_connections 768;
    }

    http {
            sendfile on;
            tcp_nopush on;
            tcp_nodelay on;
            keepalive_timeout 65;
            types_hash_max_size 2048;

            include /etc/nginx/mime.types;
            default_type application/octet-stream;

            ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
            ssl_prefer_server_ciphers on;

            access_log /var/log/nginx/access.log;
            error_log /var/log/nginx/error.log;

            gzip on;
            gzip_disable "msie6";

            include /etc/nginx/conf.d/*.conf;
            include /etc/nginx/sites-enabled/*;
    }

**/etc/nginx/sites-enabled/applications** ::

    server {
      listen 5051 ssl default_server;

      server_name rabbitmq;

      ssl_certificate     /root/CA/keys/rabbitmq.crt;
      ssl_certificate_key /root/CA/keys/rabbitmq.key;
      ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
      ssl_ciphers         HIGH:!aNULL:!MD5;

      include /etc/nginx/applications-enabled/*;
    }

**/etc/nginx/applications-enabled/webhook** ::

    location /webhook/ {
      include /var/www/webhook/uwsgi_params;
      rewrite ^/webhook/(.*)$ /$1 break;
      uwsgi_pass unix:/var/www/webhook/webhook.socket;
    }
**/etc/default/uwsgi** ::

    RUN_AT_STARTUP=yes
    VERBOSE=yes
    PRINT_CONFNAMES_IN_INITD_SCRIPT_OUTPUT=no
    INHERITED_CONFIG=/etc/uwsgi/config.ini


**/etc/uwsgi/config.ini** ::

    [uwsgi]
    autoload = true
    master = true
    workers = 2
    no-orphans = true
    pidfile = /run/uwsgi/%(deb-confnamespace)/%(deb-confname)/pid
    socket = /run/uwsgi/%(deb-confnamespace)/%(deb-confname)/socket
    chmod-socket = 660
    log-date = true

**/etc/uwsgi/apps-available/emperor.ini** ::

    [uwsgi]
    emperor = /etc/uwsgi/vassals/*.ini
    emperor-use-clone = fs,ipc,pid,uts
**/etc/uwsgi/apps-available/template.ini** ::

    [uwsgi]
    socket = /var/www/%n/%n.socket
    module = %n:create_app()
    chdir = /var/www/%n
    home = /var/www/%n
    env = APP_SETTINGS=/var/www/%n/config.cfg
    virtualenv = /var/www/%n/env
    plugins=python3
    vacuum = true
    uid=www-%n
    guid=www-%n

Deployment
----------
**cleanup of the previous setup** ::

    fab -H root@100.100.0.2 build-application

**update / install new application** ::

    fab -H root@100.100.0.2 build-application

