from django.db import models


#Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    content = models.CharField(max_length= 1000)
    date = models.DateTimeField(auto_now_add=True)

    def __repr__(self) :
        return self.title
    
class Movies(models.Model):
    name = models.CharField(max_length=300)
    director = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=500, unique=True)
    
    def __repr__(self):
        return self.name

     
  