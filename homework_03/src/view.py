"""CLI Views"""

from enum import StrEnum
from typing import Any


class Commands(StrEnum):
    """Available commands."""
    HELP = "help"
    ADD = "add"
    SHOW_ALL = "all"
    FIND_CONTACT = "find"
    EDIT_CONTACT = "edit"
    DELETE_CONTACT = "delete"
    SAVE = "save"
    SHOW_STORAGE = "show_storage"
    EXIT = "exit"

    @classmethod
    def descriptions(cls) -> dict:
        """Command descriptions."""
        return {
            cls.HELP: "get help",
            cls.ADD: "add contact",
            cls.SHOW_ALL: "show all contacts",
            cls.FIND_CONTACT: "find contact",
            cls.EDIT_CONTACT: "edit contact",
            cls.DELETE_CONTACT: "delete contact",
            cls.SAVE: "save changes to file",
            cls.SHOW_STORAGE: "show raw storage",
            cls.EXIT: "exit",
        }

    @classmethod
    def values(cls) -> set:
        """Available command string values."""
        return set(cls._member_map_.values())


class Choices(StrEnum):
    """User choices Yes/No"""
    YES = "y"
    NO = "n"
    DEFAULT = YES


CLEAR_SYMBOL = "<"


class InputView:
    """Views for getting data from stdin."""

    prompt_required = "{field_name} (required): "
    prompt_optional = "{field_name} (optional): "

    @staticmethod
    def ask_command() -> str:
        """Asks command from stdin and return it."""
        return input(f"Enter command or type '{Commands.HELP}' to get help: ")

    @staticmethod
    def ask_new_value(name: str) -> str:
        """
        Asks for new value.
        :param name: field name
        """
        prompt = "New {field} (keep empty if do not want to change it): "
        return input(prompt.format(field=name))

    @staticmethod
    def ask_to_save_changes() -> str:
        """Asks user to save changes to the storage."""
        return input(
            f"Save changes [{Choices.YES}/{Choices.NO}] (Default: {Choices.DEFAULT})? "
        )

    @staticmethod
    def update_field(name: str) -> str:
        """
        Asks user for new value to the specified field.
        :param name: field name
        """
        prompt = (
            "New {field} (keep empty if do not want to change it or "
            f"type '{CLEAR_SYMBOL}' to clear if it's possible): "
        )
        return input(prompt.format(field=name))

    @classmethod
    def ask_required_field(cls, field: str) -> str:
        """
        Asks required field from stdin and return it.
        :param field: field name
        """
        return input(cls.prompt_required.format(field_name=field))

    @classmethod
    def ask_optional_field(cls, field: str) -> str:
        """
        Asks optional field from stdin and return it.
        :param field: field name
        """
        return input(cls.prompt_optional.format(field_name=field))



class OutputView:
    """Standard output views."""

    @staticmethod
    def print_raw(data: Any):
        """Print raw data as is."""
        print(data)

    @staticmethod
    def help():
        """Prints help message."""
        command_descriptions = Commands.descriptions()
        prompt = ["Phonebook app. Commands:"]
        indent = " " * 2
        for cmd in Commands:
            description = command_descriptions.get(cmd)
            prompt.append(indent + f"- '{cmd}' - {description};")

        print("\n".join(prompt))

    @staticmethod
    def _format_contact_info(
        contact_id: int, name: str, phone: str, comment: str | None = None
    ) -> str:
        """Format contact info for pretty print."""
        return f"ID={contact_id} " + " ".join((name, phone, comment))

    @classmethod
    def new_contact(
        cls, contact_id: int, name: str, phone: str, comment: str | None = None
    ):
        """Tells user that new contact created."""
        info = cls._format_contact_info(
            contact_id=contact_id, name=name, phone=phone, comment=comment,
        )
        print("Contact added: " + info)

    @classmethod
    def contact_info(
        cls, contact_id: int, name: str, phone: str, comment: str | None = None
    ):
        """Prints contact info."""
        print(
            cls._format_contact_info(
                contact_id=contact_id, name=name, phone=phone, comment=comment,
            )
        )


class ErrorView:
    """Views for printing error messages."""

    @staticmethod
    def _format_message(message: str) -> str:
        """
        Format message to specified pattern (error messages).
        :param message: message to format
        :return formatted message
        """
        return f"Error: {message}"

    @classmethod
    def required_field(cls, field: str):
        """
        Prints error if user skip required field.
        :param field: field name
        """
        message = cls._format_message(f"{field} is required")
        print(message)

    @classmethod
    def unknown_command(cls, cmd: str):
        """
        Prints error if user entered unknown command.
        :param cmd: user's command
        """
        message = cls._format_message(f"unknown command '{cmd}'")
        print(message)

    @classmethod
    def wrong_value(cls, message: str):
        """
        Prints error if user entered incorrect value.
        :param message: error message
        """
        print(cls._format_message(message))

    @classmethod
    def not_found(cls, entity: str):
        """
        Prints error if some entity not found.
        :param entity: entity name
        """
        message = cls._format_message(f"{entity} not found")
        print(message)
