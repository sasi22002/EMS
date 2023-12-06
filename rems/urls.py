from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def not_found_view(request,*args, **kwargs):
    return JsonResponse({'message': 'URL NOT FOUND','status':False,'status_code':404,"data":[]}, status=404)


urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include([
            path('user/', include('user.urls')),
            path('<path:dummy>/', not_found_view),
            # path('login',authentication.Login.as_view(),name='login'),
            # path('signup',authentication.SignUp.as_view(),name='signup'),
            # path('logout',authentication.Logout.as_view(),name='logout'),


        ])),
        path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
        path('<path:dummy>/', not_found_view),

       
    ]



