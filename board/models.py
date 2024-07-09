from django.db import models
from member.models import CustomUser

class Post(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name="posts")
    #nickname = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    #nickname = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class UnivPost(Post):
#     university = models.ForeignKey(CustomUser, nulll=True, on_delete=models.CASCADE)