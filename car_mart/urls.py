
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('brand/<slug:brand_slug>/', views.home, name='brand_wise_post'),
    path('customer/', include("customer.urls")),
    path('car/', include("car.urls")),
    path('brand/', include("brand.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
