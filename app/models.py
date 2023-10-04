from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to='profileimg', default='default.jpg')
    location = models.CharField(max_length=100, blank=True)

    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, blank=True, related_name='post_like')

    def comments(self):
        return Comment.objects.filter(post=self).all()

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name='comment_like')

    def __str__(self):
        return f"Comment by {self.user.username}"
