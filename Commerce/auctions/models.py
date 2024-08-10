from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import ValidationError, StepValueValidator


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.category}'

class Auction(models.Model):
    title = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    content = models.TextField()
    value = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    date_mark = models.DateTimeField(auto_now=True)
    kinds = [('a', 'Active'), ('b','Hold'),('c','Closed')]
    state = models.CharField(max_length=1, choices=kinds, default='a')
    winner = models.CharField(max_length=64, blank=True)
    image = models.ImageField(upload_to ='images/', blank=True)

    def __str__(self):
        return f'{self.title}'#, {self.get_state_display()}'

class Comment(models.Model):
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE, related_name='auc_title')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    content = models.TextField()
    date_mark = models.DateTimeField(auto_now=True)

class WishList(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person', verbose_name='person')
    auction = models.ManyToManyField(Auction, blank=True) #, related_name='wishlist')

    def __str__(self):
        return f"{self.author}'s {self.auction.all()}"

    class Meta:
        verbose_name = 'Wishlist'

class Orders(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderer', verbose_name='orderer')
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE, related_name='order_auction')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.author}'s {self.auction}, qty: {self.quantity}"

    class Meta:
        verbose_name = 'Orders'

class Bet(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bet_auction')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    value = models.FloatField()
    date_mark = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.auction}, {self.author}, {self.value}'

    def clean(self):
        super().clean()
        test = Bet.objects.filter(auction=self.auction).last()
        if self.value == '':
            raise ValidationError('Value should be grater than previous %(value)s $!',
                                  params={'value': self.auction.value})
        else:
            if not test:
                if self.auction.value >= float(self.value):
                    raise ValidationError('Value should be grater than previous %(value)s $!',
                                          params={'value':self.auction.value})
            elif test.value >= float(self.value):
                raise ValidationError('Value should be grater than previous %(value)s $!',
                                      params={'value': test.value})

    def save(self):
        self.clean()
        super().save()