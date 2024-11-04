from django.db import models

# Create your models here.

from django.db import models


class User(models.Model):
    user_key = models.CharField(max_length=45, primary_key=True)
    name = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name} - {self.user_key}"

    class Meta:
        db_table = 'users'


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    batch = models.CharField(max_length=45)
    pick_date = models.IntegerField()
    is_end = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'items'


class Post(models.Model):
    post_key = models.CharField(max_length=45, primary_key=True)
    content = models.TextField()
    comment_count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_key', to_field='user_key')

    def __str__(self):
        return f"{self.post_key}"

    class Meta:
        db_table = 'post'


class Comment(models.Model):
    comment_key = models.CharField(max_length=45, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_key', to_field='user_key')
    content = models.CharField(max_length=45)
    is_order = models.BooleanField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_key', to_field='post_key')

    def __str__(self):
        return f"{self.user} - {self.content}"

    class Meta:
        db_table = 'comment'


class Order(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, db_column='comment_key', to_field='comment_key')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_column='item_id')
    order_count = models.IntegerField()
    is_picked = models.BooleanField(default=False)
    remarks = models.CharField(max_length=45)

    def __str__(self):
        return f"Order {self.item_type_num} - Count: {self.order_count}"

    class Meta:
        db_table = 'order'
        unique_together = (('comment', 'item'))


class PostItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_key', to_field='post_key')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_column='item_id')

    class Meta:
        db_table = 'post_items'
        unique_together = (('post', 'item'))
