from django.urls import path
from . import views, auth

from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),

    path('account/login/', auth.login_page, name='login'),
    path('account/sign-up/', auth.sigh_up_page, name='sign-up'),
    path('account/logout/', auth.logout_page, name='logout'),

    path('add-offer/', views.add_offer, name='add-offer'),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

