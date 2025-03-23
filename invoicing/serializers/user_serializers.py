from rest_framework import serializers

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from invoicing.models import Customer

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = User
        fields = ["url", "username", "email", "customer"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
