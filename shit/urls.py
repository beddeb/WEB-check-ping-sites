from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('register/', include('users.urls')),
    path('profile/', users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="users/password-reset.html"), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password-reset-done.html"), name='password-reset-done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password-reset-confirm.html"), name='password_reset_confirm'),
    path('password-reset-complete/ ', auth_views.PasswordResetCompleteView.as_view(template_name="users/password-reset-complete.html"), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
