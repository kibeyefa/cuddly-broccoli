from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('signup/', register_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:username>/', profile_view, name='profile'),
    path('<str:username>/edit', edit_profile_view, name='edit'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
