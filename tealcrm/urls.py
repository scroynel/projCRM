from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from userprofile.forms import LoginForm

from django.contrib.auth.views import LoginView, LogoutView

from core.views import index, about


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/teams/', include('teams.urls')),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/', include('userprofile.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('login/', LoginView.as_view(template_name='userprofile/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
