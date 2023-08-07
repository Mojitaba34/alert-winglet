import json
from typing import Any

import requests
from django.conf import settings

from ..base.sender import BaseSender


class DiscordDelivery(BaseSender):
    """
    A class for sending messages or files to a Discord webhook.

    Attributes:
        DATA (dict): A class-level dictionary to store the message data.

    Args:
        content (str): The text content of the message. If `None`, either `file` or `embeds` must be provided.
        username (str): The username to display for the message sender.
        avatar_url (str): The URL of the avatar image to display for the message sender.
        tts (bool): Specifies if the message should be sent as a text-to-speech message.
        file (file-like object): A file-like object to upload and send along with the message.
        embeds (list): A list of Discord embed objects to include with the message.
        allowed_mentions (dict): A dictionary specifying the allowed mentions in the message.
        webhook (str): The URL of the Discord webhook to send the message to.

    Raises:
        ValueError: If neither `content`, `file`, nor `embeds` are provided.
        AttributeError: If `DISCORD_WEBHOOK_URL` is not provided in settings.

    Methods:
        post():
            Sends the constructed message or file to the specified Discord webhook.

    Usage example:
        discord = Discord(
            content="Hello, everyone!",
            username="MyBot",
            avatar_url="https://example.com/avatar.png",
            tts=False,
            file=open("example.txt", "rb"),
            embeds=[{
                "title": "Example Embed",
                "description": "This is an example embed."
            }],
            allowed_mentions={"users": [1234567890]},
            webhook="https://discord.com/api/webhooks/1234567890/abcdefgh"
        )
        response = discord.post()
        print(response.status_code)
    """

    DATA = {}

    def __init__(
        self,
        content: str = None,
        username: str = None,
        avatar_url: str = None,
        tts: bool = False,
        file: Any = None,
        embeds: list = None,
        allowed_mentions=None,
    ):
        """
        Initializes a new Discord message or file.

        Args:
            content (str): The text content of the message. If `None`, either `file` or `embeds` must be provided.
            username (str): The username to display for the message sender.
            avatar_url (str): The URL of the avatar image to display for the message sender.
            tts (bool): Specifies if the message should be sent as a text-to-speech message.
            file (file-like object): A file-like object to upload and send along with the message.
            embeds (list): A list of Discord embed objects to include with the message.
            allowed_mentions (dict): A dictionary specifying the allowed mentions in the message.
            webhook (str): The URL of the Discord webhook to send the message to.

        Raises:
            ValueError: If neither `content`, `file`, nor `embeds` are provided.
            AttributeError: If `DISCORD_WEBHOOK_URL` is not provided in settings.
        """
        if content is None and file is None and embeds is None:
            raise ValueError("Required one of content, file, embeds")

        if content is not None:
            self.DATA["content"] = content

        if username is not None:
            self.DATA["username"] = username

        if avatar_url is not None:
            self.DATA["avatar_url"] = avatar_url

        if embeds is not None:
            self.DATA["embeds"] = embeds

        if allowed_mentions is not None:
            self.DATA["allowed_mentions"] = allowed_mentions

        self.file = file

        try:
            self.webhook = settings.DISCORD_WEBHOOK_URL
        except AttributeError:
            raise AttributeError(
                "DISCORD_WEBHOOK_URL variable must set in django settings"
            )

        self.DATA["tts"] = tts

    def send(self):
        """
        Sends the constructed message or file to the specified Discord webhook.

        Returns:
            The response
        """
        if self.file is not None:
            return requests.post(
                self.webhook, {"payload_json": json.dumps(self.DATA)}, files=self.file
            )

        return requests.post(
            self.webhook,
            json.dumps(self.DATA),
            headers={"Content-Type": "application/json"},
        )
