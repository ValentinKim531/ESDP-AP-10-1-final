from django.urls import path
from accounts.views.auth import RegisterUserView, LoginUserView, LogoutUserView
from accounts.views.profile import ProfileView, ProfileListView
from accounts.views.role import RoleListView, RoleDetailView, RoleCreateView, RoleUpdateView, RoleTransferView, RoleDeleteView

urlpatterns = [
    path('profile-list/', ProfileListView.as_view(), name="profile_list"),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='auth_logout'),
    path('roles/', RoleListView.as_view(), name='role_list'),
    path('role/create/', RoleCreateView.as_view(), name='role_create'),
    path('role/<int:pk>/', RoleDetailView.as_view(), name='role_detail'),
    path('role/update/<int:pk>/', RoleUpdateView.as_view(), name='role_update'),
    path('role/delete/<int:pk>/', RoleDeleteView.as_view(), name='role_delete'),
    path('role_transfer/user/<int:pk>/', RoleTransferView.as_view(), name='role_transfer'),
]
