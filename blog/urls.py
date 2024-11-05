from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',views.PostDetail.as_view(),name='detail'),
    path('share/<pk>/',views.PostShareView.as_view(), name='share'),
]
