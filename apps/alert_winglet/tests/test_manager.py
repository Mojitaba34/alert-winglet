from unittest import TestCase

from discord import Embed
from django.http import HttpRequest

from ..discord.manager import DiscordEmbedManager
import discord


class DiscordEmbedManagerTest(TestCase):
    def create_test_request(self):
        request = HttpRequest()
        request.method = "GET"
        request.META["SERVER_NAME"] = "localhost"
        request.META["SERVER_PORT"] = "8000"
        return request

    def test_init(self):
        exc = Exception("Test exception for DiscordEmbedManager init")
        request = self.create_test_request()
        exc_id = "123456789-321654987"
        title = "Test title for init"
        description = "Test discription for init "
        embed_color = discord.Color.red()
        embed = Embed(
            title="Embed Test title",
            description="Embed Test description",
            colour=discord.Color.red(),
        )
        discord_manager = DiscordEmbedManager(
            exc, request, exc_id, title, description, embed_color, embed
        )

        self.assertEqual(discord_manager.exc, exc)
        self.assertEqual(request, request)
        self.assertEqual(exc_id, exc_id)
        self.assertTrue(title, title)
        self.assertEqual(description, description)
        self.assertEqual(embed_color, embed_color)
        self.assertEqual(embed, embed)

    def test_discord_manager_without_request(self):
        discord_manager = DiscordEmbedManager(Exception("This is a test Exception"))
        formatted_exc, extra_detail = discord_manager.format_exception()
        self.assertEqual(extra_detail, None)
        self.assertIsInstance(formatted_exc, str)

    def test_discord_manager_with_request(self):
        discord_manager = DiscordEmbedManager(
            Exception("This is a test Exception"), request=self.create_test_request()
        )
        formatted_exc, extra_detail = discord_manager.format_exception()
        self.assertNotEquals(extra_detail, None)
        self.assertIsInstance(formatted_exc, str)

    def test_embed_data_instance(self):
        discord_manager = DiscordEmbedManager(Exception("This is a test Exception"))
        formatted_exc, extra_detail = discord_manager.format_exception()
        data = discord_manager.prepare_embed_data(formatted_exc, extra_detail)
        self.assertIsInstance(data, dict)

    def test_embed_data_keys(self):
        discord_manager = DiscordEmbedManager(Exception("This is a test Exception"))
        formatted_exc, extra_detail = discord_manager.format_exception()
        data = discord_manager.prepare_embed_data(formatted_exc, extra_detail)

        data_keys = data.keys()
        self.assertIn("color", data_keys)
        self.assertIn("fields", data_keys)
        self.assertIn("footer", data_keys)
        self.assertIn("type", data_keys)
