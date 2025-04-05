import random
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from faker import Faker
from django.db.models import Count, Sum
from app.models import User, Question, Answer, Tag

fake = Faker()

class Command(BaseCommand):
    help = 'Insert to DB'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='[ratio]')

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(f'Generating data with ratio={ratio}...')

        avatars = [
            'cacodemon.jpg',
            'elemental.jpg',
            'soul.jpg',
            'spectre.jpg'
        ]

        font_sizes_by_importance = [
            '0.83em',
            '1.23em',
            '1.53em'
        ]

        tags = []
        for _ in range(ratio):
            tag = Tag.objects.create(
                title=fake.unique.word()[:16],
                importance=random.randint(1, 10),
                color=fake.hex_color(),
                font_size=random.choice(font_sizes_by_importance)
            )
            tags.append(tag)
        print(f'Created {len(tags)} tags')

        users = []
        for _ in range(ratio):
            user = User.objects.create(
                name=fake.user_name()[:32],
                rating=random.randint(-100, 500)
            )

            avatar_name = random.choice(avatars)
            avatar_path = os.path.join('uploads', avatar_name)
            if os.path.exists(avatar_path):
                with open(avatar_path, 'rb') as f:
                    user.avatar.save(avatar_name, File(f))
            users.append(user)
        print(f'Created {len(users)} users')


        questions = []
        for _ in range(ratio * 10):
            question = Question.objects.create(
                title=fake.sentence(nb_words=6)[:32],
                text=fake.paragraph(nb_sentences=5)[:512],
                author=random.choice(users),
                rating=random.randint(-10, 50)
            )
            question.tags.set(random.sample(tags, k=random.randint(1, 3)))
            questions.append(question)
        print(f'Created {len(questions)} questions')


        answers = []
        for _ in range(ratio * 100):
            answer = Answer.objects.create(
                text=fake.paragraph(nb_sentences=3)[:512],
                author=random.choice(users),
                question=random.choice(questions),
                rating=random.randint(-5, 30),
                is_correct=random.choice([True, False])
            )
            answers.append(answer)
        print(f'Created {len(answers)} answers')


        questions = Question.objects.annotate(
            answers_count=Count('answer')
        ).all()

        for question in questions:
            question.count_of_answers = question.answers_count

        Question.objects.bulk_update(questions, ['count_of_answers'])

        for user in users:
            user.rating = (
                user.question_set.aggregate(Sum('rating'))['rating__sum'] +
                user.answer_set.aggregate(Sum('rating'))['rating__sum']
            ) or 0
            user.save()

        print(
            f'Successfully populated database with:\n'
            f'- {len(users)} users\n'
            f'- {len(tags)} tags\n'
            f'- {len(questions)} questions\n'
            f'- {len(answers)} answers'
        )
