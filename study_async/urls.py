from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Users.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('Users.urls')),
    path('', login, name='home'),
    path('flashcard/', include('flashcard.urls')),
    path('apostilas/', include('apostilas.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
