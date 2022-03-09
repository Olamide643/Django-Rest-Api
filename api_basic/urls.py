
from django.urls import path, include
from .views import article_list, article, ArticleList,ArticleDetail,get_movies, Movie,MovieViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', MovieViewSet,basename='movies')

urlpatterns = [
    #path('article/', article_list),
    path('article/', ArticleList.as_view()),
    path ('article/<int:id>/',article),
    path('articledetails/<int:id>/',ArticleDetail.as_view()),
    path ('movies/', get_movies ),
    #path('movie/',get_movie)
    path('api/Movies/<int:id>', Movie.as_view(), name = 'with-params'),
    path('api/Movies', Movie.as_view(), name = 'without-params'),
    path('viewsets/', include(router.urls)),
    path('viewsets/<int:pk>/', include(router.urls))

]