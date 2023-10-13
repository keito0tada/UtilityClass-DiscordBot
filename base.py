import abc
import enum
import zoneinfo
from typing import Optional, List, Union, NamedTuple, Sequence, Callable, Any

import discord
from discord.ext import commands, tasks
from discord.interactions import Interaction

from . import commandparser

ZONE_TOKYO = zoneinfo.ZoneInfo("Asia/Tokyo")

class UnSetType:
    pass

UnSet = UnSetType()

class DuplicatedSendError(Exception):
    pass


class Popups:
    def __init__(self, modal_patterns: List[Optional[discord.ui.Modal]]):
        self.modal_patterns = modal_patterns
        self.modal = modal_patterns[0]

    def set_pattern(self, index: int):
        self.modal = self.modal_patterns[index]

    async def response_send(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.modal)


class IWindow(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def send(self, sender: discord.abc.Messageable) -> discord.Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def reply(self, message: discord.Message) -> discord.Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def response_send(self, interaction: discord.Interaction) -> discord.Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def edit(self, message: discord.Message) -> discord.Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def response_edit(self, interaction: discord.Interaction) -> discord.Message:
        raise NotImplementedError


class Window(IWindow):
    def __init__(
        self,
        content: str = None,
        tts: bool = False,
        embed: discord.Embed = None,
        embeds: list[discord.Embed] = None,
        file: discord.File = None,
        files: list[discord.File] = None,
        stickers: Sequence[Union[discord.GuildSticker, discord.StickerItem]] = None,
        delete_after: float = None,
        nonce: int = None,
        allowed_mentions: discord.AllowedMentions = None,
        reference: Union[
            discord.Message, discord.MessageReference, discord.PartialMessage
        ] = None,
        mention_author: bool = None,
        view: discord.ui.View = None,
        suppress_embeds: bool = False,
        silent: bool = False,
        ephemeral: bool = False,
        emojis: list[
            Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]
        ] = None,
    ) -> None:
        self.content = content
        self.tts = tts
        self.embed = embed
        self.embeds = embeds
        self.file = file
        self.files = files
        self.stickers = stickers
        self.delete_after = delete_after
        self.nonce = nonce
        self.allowed_mentions = allowed_mentions
        self.reference = reference
        self.mention_author = mention_author
        self.view = view
        self.suppress_embeds = suppress_embeds
        self.silent = silent
        self.emojis = emojis
        self.ephemeral = ephemeral
        self.args_messageable_send = {
            "tts": tts,
            "suppress_embeds": suppress_embeds,
            "silent": silent,
        }
        self.args_messageable_edit = {
            "suppress": suppress_embeds,
        }
        self.args_interaction_send = {
            "tts": tts,
            "ephemeral": ephemeral,
            "suppress_embeds": suppress_embeds,
            "silent": silent,
        }
        self.args_interaction_edit = {}
        if content is not None:
            self.args_messageable_send["content"] = content
            self.args_messageable_edit["content"] = content
            self.args_interaction_send["content"] = content
            self.args_interaction_edit["content"] = content
        if embed is not None:
            self.args_messageable_send["embed"] = embed
            self.args_messageable_edit["embed"] = embed
            self.args_interaction_send["embed"] = embed
            self.args_interaction_edit["embed"] = embed
        if embeds is not None:
            self.args_messageable_send["embeds"] = embeds
            self.args_messageable_edit["embeds"] = embeds
            self.args_interaction_send["embeds"] = embeds
            self.args_interaction_edit["embeds"] = embeds
        if file is not None:
            self.args_messageable_send["file"] = file
            self.args_messageable_edit["attachments"] = [file]
            self.args_interaction_send["file"] = file
            self.args_interaction_edit["attachments"] = [file]
        if files is not None:
            self.args_messageable_send["files"] = files
            self.args_messageable_edit["attachments"] = files
            self.args_interaction_send["files"] = files
            self.args_interaction_edit["attachments"] = files
        if stickers is not None:
            self.args_messageable_send["stickers"] = stickers
        if delete_after is not None:
            self.args_messageable_send["delete_after"] = delete_after
            self.args_messageable_edit["delete_after"] = delete_after
            self.args_interaction_send["delete_after"]
            self.args_interaction_edit["delete_after"] = delete_after
        if nonce is not None:
            self.args_messageable_send["nonce"] = nonce
        if allowed_mentions is not None:
            self.args_messageable_send["allowed_mentions"] = allowed_mentions
            self.args_messageable_edit["allowed_mentions"] = allowed_mentions
            self.args_interaction_send["allowed_mentions"] = allowed_mentions
            self.args_interaction_edit["allowed_mentions"] = allowed_mentions
        if reference is not None:
            self.args_messageable_send["reference"] = reference
        if mention_author is not None:
            self.args_messageable_send["mention_author"] = mention_author
        if view is not None:
            self.args_messageable_send["view"] = view
            self.args_messageable_edit["view"] = view
            self.args_interaction_send["view"] = view
            self.args_interaction_edit["view"] = view

    def copy(
        self,
        content: str = UnSet,
        tts: bool = UnSet,
        embed: discord.Embed = UnSet,
        embeds: list[discord.Embed] = UnSet,
        file: discord.File = UnSet,
        files: list[discord.File] = UnSet,
        stickers: Sequence[Union[discord.GuildSticker, discord.StickerItem]] = UnSet,
        delete_after: float = UnSet,
        nonce: int = UnSet,
        allowed_mentions: discord.AllowedMentions = UnSet,
        reference: Union[
            discord.Message, discord.MessageReference, discord.PartialMessage
        ] = UnSet,
        mention_author: bool = UnSet,
        view: discord.ui.View = UnSet,
        suppress_embeds: bool = UnSet,
        silent: bool = UnSet,
        ephemeral: bool = UnSet,
        emojis: list[
            Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]
        ] = UnSet,
    ) -> "Window":
        return Window(
            content=self.content if content is UnSet else content,
            tts=self.tts if tts is UnSet else tts,
            embed=self.embed if embed is UnSet else embed,
            embeds=self.embeds if embeds is UnSet else embeds,
            file=self.file if file is UnSet else file,
            files=self.files if files is UnSet else files,
            stickers=self.stickers if stickers is UnSet else stickers,
            delete_after=self.delete_after if delete_after is UnSet else delete_after,
            nonce=self.nonce if nonce is UnSet else nonce,
            allowed_mentions=self.allowed_mentions if allowed_mentions is UnSet else allowed_mentions,
            reference=self.reference if reference is UnSet else reference,
            mention_author=self.mention_author if mention_author is UnSet else mention_author,
            view=self.view if view is UnSet else view,
            suppress_embeds=self.suppress_embeds if suppress_embeds is UnSet else suppress_embeds,
            silent=self.silent if silent is UnSet else silent,
            ephemeral=self.ephemeral if ephemeral is UnSet else ephemeral,
            emojis=self.emojis if emojis is UnSet else emojis
        )

    async def send(self, sender: discord.abc.Messageable) -> discord.Message:
        message: discord.Message = await sender.send(**self.args_messageable_send)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def reply(self, message: discord.Message) -> discord.Message:
        message: discord.Message = await message.reply(**self.args_messageable_send)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def response_send(self, interaction: discord.Interaction) -> discord.Message:
        message = await interaction.response.send_message(**self.args_interaction_send)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def edit(self, message: discord.Message) -> discord.Message:
        message: discord.Message = await message.edit(**self.args_messageable_edit)
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message

    async def response_edit(self, interaction: discord.Interaction) -> discord.Message:
        message: discord.Message = await interaction.response.edit_message(
            **self.args_interaction_edit
        )
        if self.emojis is not None:
            for emoji in self.emojis:
                await message.add_reaction(emoji=emoji)
        return message


class Windows:
    def __init__(self, defaultWindow: Window) -> None:
        self.defautlWindow = defaultWindow
        self.message: discord.Message = None

    async def run(self, interaction: discord.Interaction):
        self.message = await self.defautlWindow.response_send(interaction=interaction)

    async def destroy(self):
        if self.message is not None:
            await self.message.destroy()


class Pages(Windows):
    class PageNumberModal(discord.ui.Modal, title='ページ番号'):
        page_input = discord.ui.TextInput(label='ページ番号')
        def __init__(self, pages: 'Pages'):
            super().__init__()
            self.pages = pages 
        async def on_submit(self, interaction: discord.Interaction) -> None:
            await self.pages.move_on_page_number(page_number=int(self.page_input.value), interaction=interaction)
    class NextButton(discord.ui.Button):
        def __init__(self, pages: 'Pages', disabled: bool = False):
            super().__init__(label='>>', disabled=disabled)
            self.pages = pages
        async def callback(self, interaction: discord.Interaction) -> None:
            await self.pages.move_to_side(next=True, interaction=interaction)
    class PrevButton(discord.ui.Button):
        def __init__(self, pages: 'Pages', disabled: bool = False):
            super().__init__(label='<<', disabled=disabled)
            self.pages = pages
        async def callback(self, interaction: discord.Interaction) -> None:
            await self.pages.move_to_side(next=False, interaction=interaction)
    class PageButton(discord.ui.Button):
        def __init__(self, pages: 'Pages', index: int):
            super().__init__(label='{0}/{1}'.format(index, pages.length()))
            self.pages = pages
        async def callback(self, interaction: discord.Interaction) -> None:
            await interaction.response.send_modal(Pages.PageNumberModal(pages=self.pages))

            
    def __init__(self, windows: list[Window], defaultIndex: int = 0) -> None:
        if len(windows) <= 0:
            raise ValueError
        self.index = defaultIndex
        self.windows = windows
        for index in range(self.length()):
            if self.windows[index].view is None:
                self.windows[index] = self.windows[index].copy(view=discord.ui.View())
            window = self.windows[index]
            if len(window.view.children) >= 23:
                raise ValueError
            window.view.add_item(Pages.PrevButton(pages=self, disabled=index <= 0))
            window.view.add_item(Pages.PageButton(pages=self, index=index + 1))
            window.view.add_item(Pages.NextButton(pages=self, disabled=self.length() - 1 <= index))
        super().__init__(defaultWindow=windows[defaultIndex])

    def length(self):
        return len(self.windows)

    async def move_on_page_number(self, page_number: int, interaction: discord.Interaction):
        page_number -= 1
        if page_number < 0 or self.length() <= page_number:
            raise IndexError
        self.index = page_number
        await self.windows[page_number].response_edit(interaction=interaction)

    async def move_to_side(self, next: bool, interaction: discord.Interaction):
        if next:
            if self.index + 1 < self.length():
                await self.windows[self.index + 1].response_edit(interaction=interaction)
                self.index += 1
            else:
                raise IndexError
        else:
            if 0 <= self.index - 1:
                await self.windows[self.index - 1].response_edit(interaction=interaction) 
                self.index -= 1
            else:
                raise IndexError


class IRunner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def run(self, interaction: discord.Interaction):
        raise NotImplementedError

    @abc.abstractmethod
    async def destroy(self):
        raise NotImplementedError


class Runner(IRunner):
    def __init__(self, channel: discord.TextChannel, timeout: float = None):
        self.channel = channel
        self.timeout = timeout

    async def timeout_check(self, minutes: float) -> bool:
        self.timeout -= minutes
        if self.timeout <= 0:
            await self.destroy()
            return True
        else:
            return False


class GroupCog(commands.GroupCog):
    def __init__(self, bot: discord.ext.commands.Bot, allow_duplicated: bool):
        super().__init__()
        self.bot = bot
        self.allow_duplicated = allow_duplicated


class Command(commands.Cog):
    MINUTES = 3.0

    def __init__(self, bot: discord.ext.commands.Bot, allow_duplicated=False):
        self.bot = bot
        self.allow_duplicated = allow_duplicated
        self.parser = commandparser.CommandParser()
        self.runners: List[Runner] = []

    @tasks.loop(minutes=MINUTES)
    async def timeout_check(self):
        self.runners = [
            runner
            for runner in self.runners
            if await runner.timeout_check(minutes=Command.MINUTES)
        ]
