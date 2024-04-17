from oscar.apps.catalogue.models import Category, Product
from oscarapi.serializers.product import BaseCategorySerializer, BaseProductSerializer
from rest_framework import serializers


class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('path', 'depth')


class CustomCategorySerializer(BaseCategorySerializer):
    children = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    def get_children(self, instance):
        if isinstance(instance, Category):
            child_categories = instance.get_children()
            request = self.context.get('request')
            children_data = []
            for child_category in child_categories:
                child_data = ChildCategorySerializer(child_category).data
                if request:
                    hostname = request.get_host()
                    url = f'http://{hostname}/api/mycategories/{child_category.slug}'
                    child_data['url'] = url
                children_data.append(child_data)
            return children_data
        return None
    def get_products(self, instance):
        products = instance.product_set.all()
        product_serializer = CustomBaseProductSerializer(products, many=True, context=self.context)
        return product_serializer.data

    class Meta:
        model = Category
        exclude = ('path', 'depth')


class CustomBaseProductSerializer(BaseProductSerializer):
    class Meta:
        model = Product
        fields = '__all__'