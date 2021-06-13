from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name = "create_listing"),
    path("listing_redirect", views.post_listing, name = "list"),
    path("product_page", views.product_page, name = "product_page"),
    path("bid", views.bid, name = "bid"),
    path("add_watchlist", views.add_watchlist, name = "add_watchlist"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("remove_watchlist", views.remove_watchlist, name = "remove_watchlist"),
    path("categories", views.categories, name =  "categories"),
    path("categories/<str:items>", views.category, name = "category"),
    path("search", views.search, name = "search"),
    path("commnet", views.comment, name = "comment")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)