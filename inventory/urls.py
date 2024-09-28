from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import  register_user, ItemView

urlpatterns = [
    path('register/', register_user, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('items/', ItemView.as_view(), name='create_item'), 
    path('items/<int:item_id>/', ItemView.as_view(), name='item_detail'),
]
