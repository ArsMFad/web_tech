from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to='uploads/')

    @property
    def avatar_url(self):
        if self.avatar:
            return f"{self.avatar.name}"
        return None


class Question(models.Model):
    title = models.CharField(max_length=32)
    text = models.CharField(max_length=512)
    author = models.ForeignKey('User', on_delete=models.PROTECT)


class Answer(models.Model):
    text = models.CharField(max_length=512)
    author = models.ForeignKey('User', on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.PROTECT)


class Tag(models.Model):
    title = models.CharField(max_length=16)
    importance = models.IntegerField()
    color = models.CharField(max_length=16)
    font_size = models.CharField(max_length=8)

