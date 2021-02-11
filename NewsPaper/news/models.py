from django.db import models
import datetime

class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    labor_contract = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, through='ProductOrder')


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

def get_last_name(self):
    return self.full_name.split()[0]


def get_duration(self):
    if self.complete:# если завершен, возвращаем разность объектов
        return (self.time_out - self.time_in).total_seconds() // 60
    else:# если еще нет, то сколько длится выполнение
        return (datetime.now() - self.time_in).total_seconts() // 60


from django.contrib.auth.models import User
class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    raiting = models.CharField(default=0)

    def update_rating(self):
        self.title_rating *= 3
        self.comments_rating = ()
        self.title_rating = ()
        self.save()

class Category(models.Model):
    unique = True

class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_choice = models.CharField(max_length=2, choices=TYPE_NEWS, default=article)
    post_datetime_create = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through="PostCategory")
    post_title = models.CharField(max_length=60, unique=True)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)


    def preview(self):
        self.post_text = self.post_text[:124] + "..."
        return self.post_text

    def like(self):
        self.post_rating += 1
        self.save()


    def dislike(self):
        self.post_rating -= 1
        self.save()


    def __str__(self):
        return self.post_text



class PostCategory(models.Model):
    postcategory_post = models.OneToOneField(Post, on_delete = models.CASCADE)
    postcategory_category = models.OneToOneField(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    comment_post = models.OneToOneField(Post, on_delete = models.CASCADE)
    comment_user = models.OneToOneField(User, on_delete = models.CASCADE)
    comment_datetime_create = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)


    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating += 1
        self.save()