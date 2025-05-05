from django.db import models

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MediaFile(models.Model):
    CATEGORY_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='media_files/', blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    youtube_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
