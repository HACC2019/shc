#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HECO.settings')
    try:
        from django.core.management import execute_from_command_line
        from Front.loop import loop
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    Start = threading.Thread(target=execute_from_command_line, args=(sys.argv,))
    backend = threading.Thread(target=loop)
    Start.start()
    backend.start()

if __name__ == '__main__':
    main()
