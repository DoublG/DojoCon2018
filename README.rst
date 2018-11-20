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
Example geo request::

|{
|  "homeMobileCountryCode": 206,
|  "homeMobileNetworkCode": 1,
|  "considerIp": false,
|  "carrier": "Proximus",
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

/<routing_key>/street::
---------------------
Example street request::

{'long': 4.8367074, 'lat': 51.321642499999996 }
