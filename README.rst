Webhook
=======
The webhook application was build for the *EnviromentalSensor* project.
I acts as an entrypoint to a internal RabbitMQ server.


Configuration
-------------
Configuration is provided via a configuration file supplied
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
The "real" response is published under RabbitMQ under the *RABBITMQ_EXCHANGE*
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
All url's are protected by a simple API key. For every call you need to
supply this key, you have multiple possibilities.

============= ==================
Name          Description
============= ==================
*api_key*     GET HTTP attribute
*X-API-Key*   HTTP Header
*X-API-KEY*   Cookie name
============= ==================


