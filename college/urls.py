from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('accounts.urls')),
    path('adminn/',include('topleveladmin.urls')),
    path('download/',include('qdownloader.urls')),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    path('dev/',include('developer.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

handler404 = 'accounts.views.handler404'
handler500 = 'accounts.views.handler500'