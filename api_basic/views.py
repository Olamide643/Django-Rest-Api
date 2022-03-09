from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from  rest_framework.parsers import JSONParser
from rest_framework.serializers import ModelSerializer, Serializer
from .models  import Article, Movies
from .serializer import ArticleSerializer, MovieSerializer
from   django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView





# Create your views here.
#___________________________CLASS BASED API___________________________
class ArticleList(APIView):
    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = ArticleSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):

    def get_object(self,id):
        try:
             return  Article.objects.get(id = id)
        except Article.DoesNotExist:
            return Response(status= status.HTTP_400_BAD_REQUEST)
    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

# ________________________END OF CLASS BASED API_________________________________________



#-___________________FUNCTION BASED API_____________________________________ 
@api_view(["GET", "POST"])
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer  = ArticleSerializer(articles, many = True)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    elif request.method == "POST":
        serializer = ArticleSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT", "DELETE"])
def article(request,id):
    try:
        article = Article.objects.get(id =id)
    except Article.DoesNotExist:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ArticleSerializer(article,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return HttpResponse(serializer.errors,status =status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        article.delete()
        return HttpResponse(status = status.HTTP_204_NO_CONTENT)
    
    # ________________________END OF FUNCTION BASED API_________________________________________



#______________________GENERIC BASED API________________________________________


@api_view(["GET", "POST"])
def get_movies(request):
    if request.method == "GET":
        movies  = Movies.objects.all()
        serializer = MovieSerializer(movies, many = True)
        #serializermovies = serializer(data=movies)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    elif(request.method == "POST"):
        movie = MovieSerializer(data = request.data)
        if movie.is_valid():
            movie.save()
            return Response(movie.data, status = status.HTTP_200_OK)
        return Response(movie.errors, status = status.HTTP_400_BAD_REQUEST)


from rest_framework.views  import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class Movie(APIView):
    # Adding Authentication and Permission
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(request,id = None): 
        if id is None:
            movies = Movies.objects.all()
            return movies     
          
        movie = get_object_or_404(Movies,pk = id)
        return movie
               
    def get(self,request,id = None):
        if id is None:
            articles = self.get_object()
            serialized_movies = MovieSerializer(articles,many = True)
            return Response(serialized_movies.data, status = status.HTTP_200_OK)
        article = self.get_object(id)
        serializedmovie = MovieSerializer(article)
        return Response(serializedmovie.data, status = status.HTTP_200_OK)
    def post(self, request):
        serializer_request = MovieSerializer(data = request.data)
        if serializer_request.is_valid():
            serializer_request.save()
            return Response(serializer_request.data,status = status.HTTP_201_CREATED)
        return Response(serializer_request.errors, status = status.HTTP_400_BAD_REQUEST)
            
    def delete(self,request,id = None):
        if id is None :
            return Response(status = status.HTTP_400_BAD_REQUEST)              
        article = self.get_object(id)
        print("I am here now")
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    def put(self,request,id = None):
        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        article = self.get_object(id = id)
        serialize = MovieSerializer(article , data =request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status = status.HTTP_200_OK)
        return Response(serialize.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    
# Use Viewset
from rest_framework import viewsets

class MovieViewSet(viewsets.ViewSet):
    def list(self, request):
        movies = Movies.objects.all()
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def retrieve(self, request,pk = None):
        queryset = Movies.objects.all()
        article = get_object_or_404(queryset, pk = pk)
        serializer = MovieSerializer(article)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
        serialize = MovieSerializer(request.data)
        if serialize.is_valid():
            serialize.save()
            Response(serialize.data, status = status.HTTP_201_CREATED)
        return Response(serialize.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self,request, pk = None):
        movie = Movies.objects.get(pk=pk)
        serializer = MovieSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
            
            







