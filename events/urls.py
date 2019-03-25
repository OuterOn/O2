from django.urls import path
from events import views

urlpatterns = [
	path(r'', views.home, name="home_page"),
    path('event/<event_id>/', views.event, name="event_page"),
    path('about', views.about, name="about_page"),
    path('contact', views.contact, name="contact_page"),
    path('subscribe', views.subscribe, name="subscribe"),
    path('gallery', views.gallery, name="gallery page")
]