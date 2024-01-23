from django.contrib import admin
from django.urls import path, include
from home.views import *
from vegie.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', receipes, name='receipes'),
    path('add_receipe/', add_receipe, name="add_receipe"),
    path('view_receipe/<id>', view_receipe, name="view_receipe"),
    path('delete-receipe/<id>', delete_receipe, name='delete_receipe'),
    path('update-receipe/<id>', update_receipe, name='update_receipe'),
    path('register/', register, name="register"),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    
    path('api/account/', include("home.api.urls")),
    path("api/", include("vegie.api.urls"))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
