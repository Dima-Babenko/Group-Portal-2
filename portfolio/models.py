from django.db import models
from django.conf import settings

class Portfolio(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    file = models.FileField(upload_to='portfolio_files/', blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title


class Like(models.Model):
    project = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.project.title} liked by {self.user.username}"


class DisLike(models.Model):
    project = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dislikes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.project.title} disliked by {self.user.username}"