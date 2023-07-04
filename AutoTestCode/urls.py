
from django.contrib import admin
from django.urls import path, include
import FacebookScreenshot
urlpatterns = [
    path('admin/', admin.site.urls),
    path("amazonWebsite/", include("TestAmazonCode.urls")),
    path("facebookWebsite/", include("FacebookScreenshot.urls")),
]
