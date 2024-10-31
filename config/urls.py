from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="", view=include("nft.urls"),)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
