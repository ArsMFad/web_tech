from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import User, Question, Answer, Tag


class Command(BaseCommand):
    help = 'Destroy db data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_false',
            dest='interactive',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        interactive = options['interactive']

        if interactive:
            confirm = input("""
ВНИМАНИЕ! Это удалит все данные из базы:
- Пользователей
- Вопросы
- Ответы
- Теги

Вы уверены? [y/N]: """)
            if confirm.lower() != 'y':
                print("Операция отменена")
                return

        with transaction.atomic():
            Answer.objects.all().delete()
            print("Удалены все ответы")
            
            Question.tags.through.objects.all().delete()
            print("Удалены все связи вопрос-тег")
            
            Question.objects.all().delete()
            print("Удалены все вопросы")
            
            Tag.objects.all().delete()
            print("Удалены все теги")
            
            User.objects.all().delete()
            print("Удалены все пользователи")

        print("База данных полностью очищена!")
