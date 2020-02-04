from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    t_id = models.IntegerField()
    name = models.TextField()
    link = models.CharField(default='', max_length=255)

    def __str__(self):
        return str(self.t_id)


class Question(models.Model):
    q_id = models.IntegerField()
    text = models.TextField(default='')
    b = models.FloatField()
    a = models.FloatField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.q_id)


class Response(models.Model):
    r_id = models.CharField(max_length=255)
    ques = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    res = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.r_id


class UserTheta(models.Model):
    theta = models.FloatField(blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True)
    questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return str(self.theta)
