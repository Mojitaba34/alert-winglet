import unittest

from django.test import override_settings
from ..discord.manager import DiscordEmbedManager
from ..discord.sender import DiscordDelivery
from config import settings


class DiscordDeliveryTest(unittest.TestCase):
    @override_settings(DISCORD_WEBHOOK_URL="https://your.temporary.webhook.url")
    def test_init(self):

        content = "Test message"
        username = "TestUser"
        avatar_url = "http://example.com/avatar.png"
        tts = True
        embeds = [{"title": "Test Embed", "description": "This is a test embed"}]

        delivery = DiscordDelivery(
            content=content,
            username=username,
            avatar_url=avatar_url,
            tts=tts,
            embeds=embeds,
        )

        self.assertEqual(delivery.DATA["content"], content)
        self.assertEqual(delivery.DATA["username"], username)
        self.assertEqual(delivery.DATA["avatar_url"], avatar_url)
        self.assertTrue(delivery.DATA["tts"])
        self.assertEqual(delivery.DATA["embeds"], embeds)

    def test_send(self):
        try:
            raise Exception("This is a test Exception for discord delivery")
        except Exception as exc:
            discord_manager = DiscordEmbedManager(
                exc,
            )
        formatted_exc, extra_detail = discord_manager.format_exception()
        data = discord_manager.prepare_embed_data(formatted_exc, extra_detail)
        if hasattr(settings, "DISCORD_WEBHOOK_URL"):
            delivery = DiscordDelivery(
                embeds=[
                    data,
                ]
            )
            response = delivery.send()
            self.assertEquals(response.status_code, 204)

    def test_send_without_content_file_embeds(self):
        self.assertRaises(ValueError, DiscordDelivery)

    def test_send_without_webhook_url(self):
        if not hasattr(settings, "DISCORD_WEBHOOK_URL"):
            self.assertRaises(AttributeError, DiscordDelivery, content="Test message")
