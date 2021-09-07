from rest_framework import serializers

from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
