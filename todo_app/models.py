
from django.db import models
from django.conf import settings
from django.urls import reverse
from accounts.models import User



class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    text = models.CharField(max_length=250)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todo_app:detail",kwargs={"pk":self.id})





