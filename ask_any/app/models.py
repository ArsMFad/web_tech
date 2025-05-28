from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count

class Tag(models.Model):
    title = models.CharField(max_length=16)
    importance = models.IntegerField(default=0)
    color = models.CharField(max_length=16)
    font_size = models.CharField(max_length=8)

    @classmethod
    def get_popular_tags(cls):
        return cls.objects.annotate(
            num_questions=Count('question')
        ).order_by('-num_questions')[:10]

    def questions_count(self):
        return self.question_set.count()

    class Meta:
        ordering = ['-importance']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='uploads/')
    rating = models.IntegerField(default=0)


    @classmethod
    def get_best_members(cls):
        return cls.objects.all().order_by('-rating')[:5]

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None
    
    def __str__(self):
        return f"Profile of {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Question(models.Model):
    title = models.CharField(max_length=32)
    text = models.CharField(max_length=512)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    count_of_answers = models.IntegerField(default=0)
    rating = models.IntegerField(default=1)

    @classmethod
    def get_popular_questions(cls):
        return cls.objects.annotate(
            num_answers=Count('answer')
        ).order_by('-num_answers')
    
    @classmethod
    def get_hot_questions(cls):
        return cls.objects.order_by('-rating')
    
    @classmethod
    def get_questions_by_tag(cls, tag_title):
        return cls.objects.filter(tags__title=tag_title).distinct()
    
    @classmethod
    def get_index_questions(cls):
        return cls.objects.annotate(answers_count=Count('answer'))


class Answer(models.Model):
    text = models.CharField(max_length=512)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    rating = models.IntegerField(default=1)
    is_correct = models.BooleanField(default=False)
