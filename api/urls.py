from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token
from exam.views import error404
from django.conf.urls import handler500
handler500 = 'exam.views.error500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exam.urls')),
    path('', include('student.urls')),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^.*$', error404)
]
