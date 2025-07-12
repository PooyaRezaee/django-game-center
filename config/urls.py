"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.main.sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from debug_toolbar.toolbar import debug_toolbar_urls

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("admin/", admin.site.urls),
    path("ckeditor/", include("django_ckeditor_5.urls")),
    path("", include("apps.main.urls","main")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

    path("reserve/", include("apps.reservation.urls","reserve")),
    path("account/", include("apps.account.urls","account")),
    path("blog/", include("apps.blog.urls","blog")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=  debug_toolbar_urls()
