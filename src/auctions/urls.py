from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/register/", views.register, name="register"),
    path("listings/categories/", views.listing_categories_view, name="categories"),
    path("listings/<int:id>/", views.listing_view, name="listing"),
    path("listings/new/", views.new_listing, name="new"),
    path("accounts/watchlist/", views.watchlist_view, name="watchlist"),
    path("listings/<int:listing_id>/watch/", views.watchlist_view, name="watch"),
    path("listings/<int:id>/close/", views.close_listing, name="close_listing")
]
