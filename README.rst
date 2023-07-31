alert-winglet
=============

A Django app to send any exception to a Discord channel.

Quick start
-----------

1. Add "alert-winglet" to your `INSTALLED_APPS` setting in your Django project's settings file:

   .. code-block:: Django

        INSTALLED_APPS = [
            ...,
            "alert-winglet",
        ]

Discord:
-------

1. Set the `DISCORD_WEBHOOK_URL` variable in your Django settings. This is the URL of the Discord webhook you want to use for sending exceptions.

2. Use the `DiscordEmbedManager` class to create a Discord Embed object, and then use the `Discord` delivery method to send the exception to your Discord channel using the webhook.

Requirements
------------

- django ~= 4.1.5
- discord.py ~=2.2.3
- requests ~=2.28.2

License
-------

This project is licensed under the MIT License.

Bug Reports and Feature Requests
-------------------------------

Please use the GitHub_issue_ tracker to report any bugs or submit feature requests.

Authors
-------

- Mojtaba Davi
- Email: Mojtabadavi14@gmail.com


.. _GitHub_issue: https://github.com/Mojitaba34/alert-winglet/issues
