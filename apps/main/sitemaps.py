from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    
    def items(self):
        return [
            "main:home",
            "main:gallery",
            "main:contact",
            "reserve:index",
            "account:enter",
            "account:register",
            "account:login",
            ]

    def location(self, item):
        return reverse(item)