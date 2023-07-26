from rest_framework import serializers


class TestPostSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
