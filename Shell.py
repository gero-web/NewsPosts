#посколько я забыл сделать файл в 1 раз и мне лень его делать по новой ,я сделал короткую версию
from news.models import *
from django.contrib.auth.models import User


us = User.objects.create_user('user3')# у данного пользователя 3 id
us.save()

avtor = Author(athor=us,rating=0.0)
avtor.save()
cat1 = Category.objects.get(pk=1)
cat2 = Category.objects.get(pk=2)

post = Post.objects.create(author=avtor,title='New news',rating=0.0)
post.categories.add(cat1)
post.categories.add(cat2)
post.save()
coment_user = User.objects.get(pk=1)
post = Post.objects.get(pk=5)

coment = Comment(post=post, author_comment=coment_user, rating=0.0)
coment.save()
coment.like()
coment.rating


