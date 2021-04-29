from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,  verbose_name='User', blank=True, null=True)
    title = models.CharField(max_length=250)
    text = models.TextField(verbose_name='descrioptions')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'

    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return self.title



class Comment(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE, related_name=('comments'))
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)


    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.content)