from django.conf.urls import url
from django.conf.urls import include
from taxi import views

urlpatterns = [
        url(r'^taxis/', views.get_taxis, name='all_available_taxis'),
        url(r'taxi-detail/', views.taxi_detail, name='taxi_detail'),
        url(r'taxi-choice/', views.taxi_choice, name='taxi_by_choice'),
        url(r'book-taxi/', views.book_taxi, name='book_taxi'),
]
