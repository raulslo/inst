from django.db import models
from user.models import User
from django.utils.timezone import now

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Post(models.Model):
    text = models.TextField(max_length=1000)
    create_date = models.DateTimeField(blank=True, default=now, editable=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to="home")
    view_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="home")

    def __str__(self):
        return f'post {self.author}'

    class Meta:
        ordering = ["-create_date"]

    def comments_count(self):
        return self.comments.count()


class AbstractComment(models.Model):
    text = models.TextField(max_length=512)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        abstract = True



class Comment(AbstractComment, MPTTModel):
    text = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True, related_name='author')
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, null=True,
                             blank=True, )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return "{} - {}".format(self.user, self.post)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"Like {self.author} to {self.post}"
