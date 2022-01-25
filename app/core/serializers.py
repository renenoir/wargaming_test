# from pyrsistent import field
from rest_framework import serializers


class FibonacciSequenceSerializer(serializers.Serializer):
    """Serializer for fibonacci sequence"""
    data = serializers.ListField(child=serializers.IntegerField())
