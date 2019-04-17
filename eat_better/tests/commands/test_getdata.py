"""Tests for getdata command."""


import re
from io import StringIO

import pytest

from django.core.management.base import BaseCommand
from django.core.management import call_command

from eat_better.management.commands.getdata import Command
from eat_better.models import Product


def test_class():
    """Test that class exist and is a subclass of BaseCommand."""
    assert Command()
    assert issubclass(Command, BaseCommand)


@pytest.mark.django_db
def test_handle():
    """Test the handle method."""
    assert len(Product.objects.all()) == 0
    c = Command()
    c.handle()
    assert Product.objects.get(name="Granola Chocolat au Lait")


@pytest.mark.django_db
def test_getdata_output():
    """Test the interface of the command."""
    out = StringIO()
    call_command("getdata", stdout=out)
    assert "Populating database..." in out.getvalue()
    assert re.search(r"\d+\/\d+", out.getvalue()) is not None
    assert "Database populating done successfully !" in out.getvalue()
