
from rest_framework.serializers import ModelSerializer

from .models import Comment, Contributor, Issue, Project

from django.contrib.auth import get_user_model

from django.contrib.auth.models import User



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

