from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Poll(models.Model):

    question = models.CharField(max_length=256)

    def __str__(self):
        return self.question


class PollOption(models.Model):

    poll = models.ForeignKey(Poll, related_name="options", on_delete=models.CASCADE)
    option_text = models.CharField(max_length=256)

    def __str__(self):
        return self.option_text


class PollAnswer(models.Model):

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(PollOption, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('poll', 'user')

    def __str__(self):
        return f'{self.user.username} вiдповiв на "{self.poll.question}"'