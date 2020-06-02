from django.db import models
from django.contrib.auth import get_user_model


class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=50)
    comment = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)