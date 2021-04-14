from django.urls import path

from .views import HomeView, SearchView, TeamBuilderView, PlayerDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('team-builder/', TeamBuilderView.as_view(), name='team-builder'),
    path('player/<pk>/', PlayerDetailView.as_view(), name='player-detail'),
]
