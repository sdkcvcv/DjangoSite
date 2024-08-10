from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<int:auc_id>", views.auction, name='auction'),
    path("add_auction", views.add_auction, name='add_auction'),
    path("add_comment", views.comment, name='add_comment'),
    path("bet", views.bet, name='bet'),
    path("wishlist", views.wishlist, name='wishlist'),
    path("wishlist_remove", views.wishlist_remove, name='wishlist_remove'),
    path("edit", views.edit, name='edit'),
    path("update_auc", views.update_auc, name='update_auc'),
    path("cancel/<int:auc_id>", views.cancel, name='cancel'),
    path("resume/<int:auc_id>", views.resume, name='resume'),
    path("auction_remove",views.auction_remove, name='auction_remove'),
    path("category/<int:cat_id>", views.categories, name='category'),
    path("orders", views.orders, name='orders'),
    path('order_remove', views.order_remove, name='order_remove')
]
