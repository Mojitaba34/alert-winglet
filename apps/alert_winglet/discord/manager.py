import traceback
from typing import Optional

import discord
from discord import Embed
from django.http import HttpRequest
from django.utils import timezone

from ..base.manager import BaseManager


class DiscordEmbedManager(BaseManager):
    """
    A class for managing Discord embed messages for exception handling.

    Args:
        exc (Exception): The exception instance.
        request (HttpRequest | None, optional): The HttpRequest object associated with the exception.
        exc_id (str | int | None, optional): ID associated with the exception. Defaults to None.
        title (str, optional): Title of the embed. Defaults to an empty string.
        description (str, optional): Description of the embed. Defaults to an empty string.
        embed_color (discord.Color | None, optional): Color of the embed. Defaults to None.
        embed (discord.Embed | None, optional): Predefined discord.Embed object. Defaults to None.

    Attributes:
        exc (Exception): The exception instance.
        exc_id (str | int | None): ID associated with the exception.
        request (HttpRequest | None): The HttpRequest object associated with the exception, if provided.
        title (str): Title of the embed.
        description (str): Description of the embed.
        embed_color (discord.Color): Color of the embed.
        embed (discord.Embed): Discord embed object.

    Methods:
        setup_embed(): Sets up the discord.Embed object.
        _frame_summary_handler(frame_summary: list[traceback.FrameSummary]): Handles the formatting of a frame summary.
        format_exception() -> tuple[str, str | None]: Formats the exception and returns formatted text and extra detail.
        _embed_footer_data(): Generates data for the embed footer.
        prepare_embed_data(formatted_exception: str, extra_detail: Optional[str] = None) -> dict: Prepares and returns the embed data as a dictionary.
    """

    def __init__(
        self,
        exc: Exception,
        request: Optional[HttpRequest] = None,
        exc_id: str | int | None = None,
        title: str = "",
        description: str = "",
        embed_color=None,
        embed: discord.Embed | None = None,
    ):
        if not exc:
            raise ValueError(
                "Exception instance must be provide (exc can't be None or falsy value)"
            )

        self.exc = exc
        self.exc_id = exc_id
        self.request = request

        self.title = title
        self.description = description

        self.embed_color = embed_color if embed_color else discord.Color.red()

        self.embed = embed if embed else self.setup_embed()

    def setup_embed(self) -> discord.Embed:
        return Embed(
            title=self.title, description=self.description, colour=self.embed_color
        )

    def _frame_summary_handler(self, frame_summary: list[traceback.FrameSummary]):
        return traceback.format_list(frame_summary)

    def format_exception(self) -> tuple[str, str | None]:
        frame_summary: list = traceback.extract_tb(self.exc.__traceback__)[-2:]
        formatted_exc = "\n".join(self._frame_summary_handler(frame_summary))

        formatted_exc += f"{str(self.exc)}\n"

        extra_detail = (
            (
                f"Request API  -> {self.request.build_absolute_uri()}\n"
                f"Request Method -> {self.request.method}"
            )
            if self.request
            else None
        )

        return formatted_exc, extra_detail

    def _embed_footer_data(self):
        data = f"DateTime: {timezone.now()}\n"
        data += f"Error ID : {self.exc_id}" if self.exc_id else ""
        return data

    def prepare_embed_data(
        self, formatted_exception: str, extra_detail: Optional[str] = None
    ) -> dict:
        """
        Prepare and return the embed data as a dictionary.

        Args:
            formatted_exception (str): The formatted exception as a string.
            extra_detail (str | None, optional): Additional details related to the exception. Defaults to None.

        Returns:
            dict: Embed data as a dictionary containing formatted exception, extra detail, and other embed fields.
        """
        self.embed.add_field(
            name=str(self.exc.__class__.__name__), value=formatted_exception
        )
        if extra_detail:
            self.embed.add_field(name="Extra Detail", value=extra_detail, inline=False)

        self.embed.set_footer(text=self._embed_footer_data())
        return self.embed.to_dict()
