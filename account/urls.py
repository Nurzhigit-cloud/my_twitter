from django.urls import path
from account import views
from .views import UserLoginView,  ProfileUserView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.registration_user, name="register"),
    path('accounts/profile/', ProfileUserView.as_view(), name="profile"),


]