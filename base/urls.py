from django.urls import path
from . import views, auth


urlpatterns = [
    path('', views.home, name='home'),

    path('account/login/', auth.login_page, name='login'),
    path('account/sign-up/', auth.sigh_up_page, name='sign-up'),
    path('account/logout/', auth.logout_page, name='logout'),
    path('account/settings/', auth.account_settings, name='account-settings'),
    path('account/settings/<str:username>/', auth.account_settings, name='account-settings'),

    path('add-offer/', views.add_offer, name='add-offer'),

    path('offer/<int:pk>/', views.OfferId.as_view(), name='offer-id'),

    path('category/', views.offer_category, name='offer-category'),
    path('category/<str:category_name>/', views.offer_category, name='offer-category'),
]
