from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """
    Only authors can write posts but all users can write comments.
    Has one-to-one relation with User.
    """

    rating = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        """Update author's rating, based on posts and comments ratings"""

        post_rating = sum(dct['rating'] for dct in Post.objects.filter(author=self).values('rating')) // 3
        author_comm = sum(dct['rating'] for dct in Comment.objects.filter(user=self.user).values('rating'))
        comm_under_posts = sum(dct['rating'] for dct in Comment.objects.filter(post__author=self).values('rating'))
        return post_rating + author_comm + comm_under_posts


class Category(models.Model):
    """Has many-to-many relation with posts trough model PostCategories"""

    name = models.CharField(max_length=150, unique=True)


class Post(models.Model):
    """Can be news or article; has relation with Author"""

    PREVIEW_LENGTH = 124

    news = 'NE'
    article = 'AR'
    ITEM_TYPE = [(news, 'news'),
                 (article, 'article')]

    type = models.CharField(max_length=2, choices=ITEM_TYPE, default=news)
    add_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        """Increase a rating by 1"""
        self.rating += 1
        self.save()

    def dislike(self):
        """Decrease a rating by 1"""
        self.rating -= 1
        self.save()

    def preview(self):
        """Show the beginning of the post"""
        return self.content[:self.PREVIEW_LENGTH] + '...'


class PostCategory(models.Model):
    """Release the many-to-many relation between Post and Category"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """All users can add comment under a post"""

    content = models.CharField(max_length=1000)
    add_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        """Increase a rating by 1"""
        self.rating += 1
        self.save()

    def dislike(self):
        """Decrease a rating by 1"""
        self.rating -= 1
        self.save()
