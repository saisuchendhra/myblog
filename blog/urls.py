from django.urls import path
from . import views
from blog.views import frontpage, post_detail
# from .views import HomePageView, AboutPageView  # new
urlpatterns = [
    path("", frontpage, name="home"),
    path("<slug:slug>/", post_detail, name='post_detail' ),
]