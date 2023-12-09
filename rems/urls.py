from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt import views as jwt_views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils import authentication
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

@csrf_exempt
def not_found_view(request,*args, **kwargs):
    return JsonResponse({'message': 'URL NOT FOUND','status':False,'status_code':404,"data":[]}, status=404)


schema_view = get_schema_view(
   openapi.Info(
      title="Real Estate Management system",
      default_version='v1',
      description="API's for Real Estate management system",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="ssasikumar4800@gmail.com"),
      license=openapi.License(name="Your License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include([
            path('user/', include('user.urls')),
            path('admin/', include('masteradmin.urls')),
            path('<path:dummy>/', not_found_view),
            path('login',authentication.Login.as_view(),name='login'),
            path('signup',authentication.SignUp.as_view(),name='signup'),
            path('logout',authentication.Logout.as_view(),name='logout'),


        ])),
        path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('login-page/', authentication.login_page, name='login_page'),
        path('dashboard/', authentication.dashboard, name='dashboard_page'),
        path('manage-property/', authentication.manage_property, name='manage-property'),
        # path('login-page/', authentication.login_page, name='login_page'),

        path('<path:dummy>/', not_found_view),


       
    ]



