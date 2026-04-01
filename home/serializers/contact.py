from rest_framework import serializers


class ContactMessageInputSerializer(serializers.Serializer):
    """Validate contact message input payload."""

    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()
