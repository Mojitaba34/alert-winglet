alert-winglet
=============

A Django app to send any exception to a Discord channel.

Quick start
-----------

Installation
------------

You can install ``django-alert-winglet`` using ``pip``::
    pip install django-alert-winglet

1. Add "alert_winglet" to your `INSTALLED_APPS` setting in your Django project's settings file::

    INSTALLED_APPS = [
        ...,
        "alert_winglet",
    ]

Discord
-------

1. Set the `DISCORD_WEBHOOK_URL` variable in your Django settings. This is the URL of the Discord webhook you want to use for sending exceptions.

2. Use the `DiscordEmbedManager` class to create a Discord Embed object. ::

    from alert_winglet.discord.manager import DiscordEmbedManager

    # If the request is not provided, the `extra_detail` variable will be None
    discord_manager = DiscordEmbedManager(
          exc,
      )
    formatted_exc, extra_detail = discord_manager.format_exception()
    data = discord_manager.prepare_embed_data(formatted_exc, extra_detail)

3. Then use the `DiscordDelivery` class to send the exception to your Discord channel using the webhook.
This class can be used for other purposes as well, like sending messages or files... . ::

    from alert_winglet.discord.sender import DiscordDelivery

    delivery = DiscordDelivery(
        embeds=[
            data,
        ]
    )
    delivery.send()


Requirements
------------

- django >= 3.0
- discord.py >=2.2.3
- requests >=2.28.2

License
-------

This project is licensed under the MIT License.

Bug Reports and Feature Requests
--------------------------------

Please use the GitHub_issue_ tracker to report any bugs or submit feature requests.

Authors
-------

- Mojtaba Davi
- Email: Mojtabadavi14@gmail.com


.. _GitHub_issue: https://github.com/Mojitaba34/alert-winglet/issues
