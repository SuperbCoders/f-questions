#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import re
import sys


def text_processor(text: str) -> str:
    tokens = re.findall(r"[а-яa-z]+", text.lower())
    return " ".join([f"#{token}#" for token in tokens])


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deal_digger.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
