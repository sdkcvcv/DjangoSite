from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'content','value', 'author', 'date_mark', 'state')

admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bet)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(WishList)
admin.site.register(Orders)
