from django.db import models

class Tag(models.Model):
    title = models.CharField(max_length=16)
    importance = models.IntegerField()
    color = models.CharField(max_length=16)
    font_size = models.CharField(max_length=8)

    def questions_count(self):
        return self.question_set.count()  # Количество вопросов с этим тегом

    class Meta:
        ordering = ['-importance']  # Сортировка по важности по умолчанию


class User(models.Model):
    name = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to='uploads/')
    rating = models.IntegerField(default=0)

    @property
    def avatar_url(self):
        if self.avatar:
            return f"/{self.avatar.name}"
        return None


class Question(models.Model):
    title = models.CharField(max_length=32)
    text = models.CharField(max_length=512)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)  # Изменили на ManyToMany
    count_of_answers = models.IntegerField(default=0)
    rating = models.IntegerField(default=1)


class Answer(models.Model):
    text = models.CharField(max_length=512)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    rating = models.IntegerField(default=1)
    is_correct = models.BooleanField(default=False)
