from rest_framework import serializers
from .models import Article, Movies 

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','title', 'author', 'email', 'content','date']

        #fields = '__all__'  #To get all fields
        
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        
        fields  = '__all__'


