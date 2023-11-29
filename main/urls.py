from django.urls import path
from . import views

urlpatterns = [
	path('', views.SiteListView.as_view(), name='main'),
	path('site/<int:pk>/', views.SiteDetailView.as_view(), name='site'),
	path('site/comment/<int:pk>/delete', views.DeleteComment.as_view(), name='comment-delete'),
	path('user-site/<int:pk>/', views.UserSiteDetailView.as_view(), name='user-site'),
	path('user-site/new', views.UserSiteCreate.as_view(), name='user-site-create'),
	path('user-site/<int:pk>/update', views.UserSiteUpdate.as_view(), name='user-site-update'),
	path('user-site/<int:pk>/delete', views.UserSiteDelete.as_view(), name='user-site-delete'),
	path('user-site/user/<str:username>/', views.UserSiteListView.as_view(), name='user-sites'),
	path('help/', views.help_view, name='help'),
	path('about/', views.about, name='about'),
	path('contact/', views.contact, name='contact')
]
