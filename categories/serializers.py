from rest_framework import serializers
from oscar.apps.catalogue.models import Category, Product
from oscarapi.serializers.product import BaseCategorySerializer, BaseProductSerializer, ProductImageSerializer

class ChildCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class CustomCategorySerializer(BaseCategorySerializer):
    children = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    def get_children(self, instance):
        if isinstance(instance, Category):
            child_categories = instance.get_children()
            request = self.context.get('request')
            children_data = []
            for child_category in child_categories:
                child_serializer = ChildCategorySerializer(child_category, context={'request': request})
                child_data = child_serializer.data
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
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
