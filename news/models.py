from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
def BestOfTheBest():
    best = Author.objects.order_by('rating')[0]
    return best.athor.username + ' ' + str(best.rating)


def BestOfTheBestPost():
    post = Post.objects.order_by('rating')[0]
    return ' '.join([post.author.athor.username, str(post.created), post.title])


def AllComments():
    comments = Comment.objects.all()
    for comment in comments:
        print(comment.author_comment.username, str(comment.created), comment.body, str(comment.rating))


class Author(models.Model):
    athor = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, default=0.0, decimal_places=2)

    def __str__(self):
        return f'{self.athor.username}'

    def update_rating(self):
        rating_post = sum(item['rating'] for item in Post.objects.filter(author=self.pk).values('rating')) * 3
        rating_comment = sum(
            item['rating'] for item in Comment.objects.filter(author_comment=self.athor).values('rating'))
        rating_post_comment = sum(
            item['rating'] for item in Comment.objects.filter(post=Post.objects.get(pk=self.pk)).values('rating'))
        self.rating = rating_post + rating_comment + rating_post_comment
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    _choiser = [
        ('nw', 'news'),
        ('ar', 'article')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choise = models.CharField(choices=_choiser, default='nw', max_length=2)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    rating = models.DecimalField(max_digits=5, default=0.0, decimal_places=2)
    categories = models.ManyToManyField(Category, through='PostCategory')
    body = models.TextField()

    def get_absolute_url(self):
        name_url = ''
        if self.choise == 'nw':
            name_url = 'news'
        else:
            name_url = 'posts'
        return reverse(name_url)

    def __str__(self):
        return f'{self.title}'

    def preview(self):
        return self.body[:124] + '.....'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class SubscriptionCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=5, default=0.0, decimal_places=2)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
