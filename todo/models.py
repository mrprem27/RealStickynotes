from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.email


class Task(models.Model):
    priority_choices = [
        ('1', '1️'),
        ('2', '2️'),
        ('3', '3️'),
        ('4', '4️'),
        ('5', '5️'),
        ('6', '6️'),
        ('7', '7️'),
        ('8', '8️'),
        ('9', '9️'),
        ('10', '10')
    ]
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=4000)
    date = models.DateField(auto_now=True)
    img = models.ImageField(upload_to="uploads/images", height_field=None, width_field=None,
                            max_length=None, null=True, blank=True, default="image\download\wallpaper2you_341524.jpg")
    status = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_ls")
    priority = models.CharField(max_length=2, choices=priority_choices)

    def __str__(self):
        return self.title
