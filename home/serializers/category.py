from rest_framework.serializers import ModelSerializer

from home.models.category import Category


class CategorySerializer(ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
