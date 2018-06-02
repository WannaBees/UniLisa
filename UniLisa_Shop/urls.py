from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^shop/', include('shopping.urls')),
    url(r'^account/', include('shopping.urls')),
    url(r'^create/', include('shopping.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

