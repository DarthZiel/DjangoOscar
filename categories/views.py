from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from oscarapi.views.product import CategoryList
from oscar.apps.catalogue.models import Category, Product
from .serializers import CustomCategorySerializer, CustomBaseProductSerializer

class CustomCategoryList(CategoryList):

    def get_queryset(self):
        slug = self.kwargs.get("category_slug", None)
        if slug is None:
            return super().get_queryset()

        category = get_object_or_404(Category, slug=slug)

        if category.get_children().exists():
            return category.get_children()
        else:
            category = Category.objects.get(slug=slug)
            products = Product.objects.filter(categories=category)
            return products

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if hasattr(queryset, 'model') and queryset.model == Product:
                serializer = CustomBaseProductSerializer(queryset, many=True, context={'request': request})
            else:
                serializer = CustomCategorySerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        except Http404:
            return Response({"detail": "Категория не найдена"}, status=status.HTTP_404_NOT_FOUND)

