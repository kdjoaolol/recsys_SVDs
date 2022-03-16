from django.db import models

# Create your models here.

class Filme(models.Model):
    id = models.AutoField(primary_key=True)
    id_filmes = models.IntegerField()
    title = models.CharField(max_length=200)
    urls_imgs_185 = models.CharField(max_length=400)
    urls_imgs_500 = models.CharField(max_length=400)
    overview = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.CharField(max_length=200)
    rating = models.IntegerField()
    id_filme = models.IntegerField()

    def __str__(self):
        return self.id_usuario
