from django.urls import path, reverse_lazy
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter
from .views import (Permisisonlist, 
                    PermissionCreate, 
                    UserLogViewset,
                    UserListCreateView,
                    UserDetailView)

router = SimpleRouter()
router.register(r'userlog', UserLogViewset, basename='user-log')

from django.contrib.auth.views import LoginView
class LoginView(LoginView):
    template_name = 'safenews/login.html'
    def get_success_url(self) -> str:
        return reverse_lazy('user-list-create')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('permissions/', Permisisonlist.as_view(), name='permission_list'),
    path('permissions/<int:pk>/', PermissionCreate.as_view(), name='permission_create'),

    path('accounts/', UserListCreateView.as_view(), name='user-list-create'),
    path('accounts/<int:pk>/', UserDetailView.as_view(), name='user-retrieve-update'),
]

urlpatterns+=router.urls