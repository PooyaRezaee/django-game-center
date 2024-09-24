from .models import SiteSettings

def site_settings(request):
    config = SiteSettings.get_solo()

    return {
        "config": config,
    }
