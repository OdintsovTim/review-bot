#!/usr/bin/env python
import os
import sys
from pathlib import Path


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

    from configurations.management import execute_from_command_line

    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / 'review_bot'))

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
