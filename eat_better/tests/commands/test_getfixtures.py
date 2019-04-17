from django.core.management.base import BaseCommand

from eat_better.management.commands.getfixtures import Command


def test_class_exist():
    """Test that class exist."""
    assert Command()
    assert issubclass(Command, BaseCommand)
