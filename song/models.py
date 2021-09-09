from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=55, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to='authors')

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    slug = models.SlugField(max_length=55, primary_key=True)
    name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=65, unique=True)
    image= models.ImageField()
    audio_file = models.FileField(blank=True,null=True)
    artist = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='songs')
    genre = models.ManyToManyField(Genre)
    duration = models.CharField(max_length=20)
    paginate_by = 2

    def __str__(self):
        return f'{self.artist} - {self.title} '


class Comment(models.Model):
    song = models.ForeignKey(Song ,on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Песня : {self.song}. Пользователь : {self.author}.'


def validate_rating(rating):
    if rating < 0:
        raise ValidationError(('Рейтинг не может быть ниже 0'), params={'rating': rating}, )
    elif rating > 5:
        raise ValidationError(('Рейтинг не может быть выше 5'), params={'rating': rating}, )
    else:
        return rating


class Rating(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='rating_manga')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rating')
    rating = models.SmallIntegerField(default=0, validators=[validate_rating])

    def __str__(self):
        return f'Песня : {self.song}. Пользователь : {self.user}. Рейтинг : {self.rating}.'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'Песня : {self.song}. Пользователь : {self.user}. Лайк и дизлайк : {self.is_liked}.'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'Песня : {self.song}. Пользователь : {self.user}. Избранное : {self.favorite}.'
