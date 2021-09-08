from django_filters import rest_framework as rest_filters
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .permissions import *


class SongFilter(filters.FilterSet):
    class Meta:
        model = Song
        fields = ('genre', )


from rest_framework import filters

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [rest_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SongFilter
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'list':
            return SongSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthorOrIsAdmin()]
        elif self.action in ['like', 'add_to_favorite']:
            return [IsAuthenticated()]
        return []
        return []

    @action(detail=True, methods=['post'])
    def like(self, request, pk):
        song = self.get_object()
        user = request.user
        like_obj, created = Like.objects.get_or_create(song=song, user=user)
        if like_obj.is_liked:
            like_obj.is_liked = False
            like_obj.save()
            return Response('disliked')
        else:
            like_obj.is_liked = True
            like_obj.save()
            return Response('liked')

    @action(detail=True, methods=['post'])
    def add_to_favorite(self, request, pk):
        song = self.get_object()
        user = request.user
        fav, created = Favorite.objects.get_or_create(song=song, user=user)
        if fav.favorite:
            fav.favorite = False
            fav.save()
            return Response('Удален из избранных')
        else:
            fav.favorite = True
            fav.save()
            return Response('Добавлен в избранные')


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [rest_filters.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', ]:
            return [IsAuthenticated()]
        return []


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', ]:
            return [IsAuthenticated()]
        return []


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthorOrIsAdmin(), IsAuthenticated()]
        return []


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthorOrIsAdmin()]
        return []


class FavoritesView(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteListSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthorOrIsAdmin(), IsAuthenticated()]
        return []


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthorOrIsAdmin(), IsAuthenticated()]
        return []
