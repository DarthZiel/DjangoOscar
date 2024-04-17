from oscarapi.utils.categories import find_from_full_slug
from rest_framework import status
from rest_framework.generics import ListAPIView
from oscarapi.views.product import CategoryList
from rest_framework.response import Response
from oscar.apps.catalogue.models import Category, Product
from .serializers import CustomCategorySerializer, CustomBaseProductSerializer

from django.http import Http404
from rest_framework.generics import get_object_or_404

class CustomCategoryList(CategoryList):

    def get_queryset(self):
        slug = self.kwargs.get("category_slug", None)
        if slug is None:
            return super().get_queryset()

        category = get_object_or_404(Category, slug=slug)

        if category.get_children().exists():
            # Если у категории есть дочерние категории, возвращаем их
            return category.get_children()
        else:
            # Иначе возвращаем товары для данной категории
            category = Category.objects.get(slug=slug)
            print(category)
            products = Product.objects.filter(categories=category)
            return products

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if hasattr(queryset, 'model') and queryset.model == Product:
                # Если это набор товаров, используем соответствующий сериализатор для товаров
                serializer = CustomBaseProductSerializer(queryset, many=True, context={'request': request})
            else:
                # Если это набор категорий, используем соответствующий сериализатор для категорий
                serializer = CustomCategorySerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        except Http404:
            return Response({"detail": "Категория не найдена"}, status=status.HTTP_404_NOT_FOUND)