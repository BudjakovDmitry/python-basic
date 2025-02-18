from model import Contact, ContactNotFound, PhonebookModel
from view import Choices, Commands, ErrorView, InputView, OutputView


class FieldRequired(Exception):
    """Raises if required field does not pass."""
    def __init__(self, field_name: str):
        self.field_name = field_name

    def __str__(self):
        return f"Field {self.field_name} is required"


class CommandNotFound(Exception):
    """Raises if there is unknown command."""
    def __init__(self, cmd: str):
        self.cmd = cmd

    def __str__(self):
        return f"Command {self.cmd} not found"


class PhonebookController:
    """
    PhonebookController acts as intermediary between views and models.
    It handles user input and updates the models accordingly.
    """

    def __init__(self):
        self.phonebook = PhonebookModel()

    @staticmethod
    def _get_required_field(field: str) -> str:
        """
        Get required field from view. If value is empty raises FileRequired exception.
        :param field: field name
        """
        value = InputView.ask_required_field(field)
        if not value:
            raise FieldRequired(field)
        return value

    @staticmethod
    def _get_command_or_raise() -> str:
        """Waits for user's command and return it."""
        command = InputView.ask_command()
        if command and command not in Commands.values():
            raise CommandNotFound(command)
        return command

    @classmethod
    def _get_required_integer_field(cls, field: str) -> int:
        """
        Get required field from view, convert to int if it is possible. If not, raises
        ValueError.
        :param field: field name
        """
        value = cls._get_required_field(field)
        if not value.isdigit():
            raise ValueError(f"Incorrect value for contact ID. It must be an integer")
        return int(value)


    def _add_contact(self):
        """Add contact to phonebook."""
        contact: Contact = self.phonebook.add_contact(
            name=self._get_required_field("Name"),
            phone=self._get_required_field("Phone"),
            comment=InputView.ask_optional_field("Comment"),
        )
        OutputView.new_contact(
            contact_id=contact.id_,
            name=contact.name,
            phone=contact.phone,
            comment=contact.comment,
        )

    def _print_contacts(self):
        """Print all contacts."""
        for contact in self.phonebook.contacts():
            OutputView.contact_info(
                contact_id=contact.id_,
                name=contact.name,
                phone=contact.phone,
                comment=contact.comment,
            )

    def _find_contact(self):
        """Find contact via its ID."""
        search_string = self._get_required_field("Search")
        contacts = self.phonebook.find_contacts(search_string)
        for contact in contacts:
            OutputView.contact_info(
                contact_id=contact.id_,
                name=contact.name,
                phone=contact.phone,
                comment=contact.comment,
            )

    def _edit_contact(self) -> Contact:
        """Update contact info."""
        contact_id = self._get_required_integer_field("ID")
        contact: Contact = self.phonebook.get(contact_id)

        contact.update(
            new_name=InputView.update_field("name"),
            new_phone=InputView.update_field("phone"),
            new_comment=InputView.update_field("comment"),
        )
        return contact

    def _delete_contact(self):
        """Delete contact."""
        contact_id = self._get_required_integer_field("Contact ID")
        self.phonebook.delete_contact(contact_id)

    def _show_storage(self):
        """Print raw contacts data from storage."""
        data = self.phonebook.raw_storage()
        OutputView.print_raw(data)


    def run(self):
        """Main program cycle."""
        command = None
        while command != Commands.EXIT:
            try:
                command = self._get_command_or_raise()
            except CommandNotFound as err:
                ErrorView.unknown_command(err.cmd)
                continue

            if command == Commands.ADD:
                try:
                    self._add_contact()
                except FieldRequired as err:
                    ErrorView.required_field(err.field_name)
                finally:
                    continue

            elif command == Commands.FIND_CONTACT:
                try:
                    self._find_contact()
                except FieldRequired as err:
                    ErrorView.required_field(err.field_name)
                finally:
                    continue

            elif command == Commands.EDIT_CONTACT:
                try:
                    contact = self._edit_contact()
                except FieldRequired as err:
                    ErrorView.required_field(err.field_name)
                except ValueError as err:
                    ErrorView.wrong_value(err.args[0])
                except ContactNotFound:
                    ErrorView.not_found("contact")
                else:
                    OutputView.contact_info(
                        contact_id=contact.id_,
                        name=contact.name,
                        phone=contact.phone,
                        comment=contact.comment,
                    )
                finally:
                    continue

            elif command == Commands.DELETE_CONTACT:
                try:
                    self._delete_contact()
                except FieldRequired as err:
                    ErrorView.required_field(err.field_name)
                except ValueError as err:
                    ErrorView.wrong_value(err.args[0])
                finally:
                    continue

            elif command == Commands.SHOW_ALL:
                self._print_contacts()
            elif command == Commands.SHOW_STORAGE:
                self._show_storage()
            elif command == Commands.SAVE:
                self.phonebook.save()
            elif command == Commands.HELP:
                OutputView.help()

        if self.phonebook.has_unsaved_changes():
            save = InputView.ask_to_save_changes() or Choices.DEFAULT
            if save == Choices.YES:
                self.phonebook.save()
