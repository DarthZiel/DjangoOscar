from django.urls import path, re_path
from .views import CustomCategoryList

urlpatterns = [
    path('mycategories/', CustomCategoryList.as_view()),
    path('mycategories/<slug:category_slug>/', CustomCategoryList.as_view(), name='mycategories-list'),
]