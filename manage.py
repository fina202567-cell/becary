#!/usr/bin/env python
# Django プロジェクト実行ファイル
import os, sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_project.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
