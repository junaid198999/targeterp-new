from django.conf import settings
from django.urls import include, path

from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    # path(settings.ADMIN_URL, admin.site.urls),

    # User management
    path("users/", include("TARGET.users.urls", namespace="users"), ),
    path("accounts/", include("allauth.urls")),

    # Your stuff: custom urls includes go here
    path("", include("TARGET.dashboard.urls", namespace="dashboard"), ),

    path("crm/", include("TARGET.crm.urls", namespace="crm"), ),

    # GL module
     path('gl/', include("gl.urls", namespace="gl")),
    # End GL Module

    # AR module
    path('ar/', include("ar.urls", namespace="ar")),
    # End AR Module

    # AP module
    path('ap/', include("ap.urls", namespace="ap")),
    # End AP Module


    # # IN module
    # path('in/', include("in.urls", namespace="in")),
    # # End IN Module

    # INV module
    path('inv/', include("inv.urls", namespace="inv")),
    # End INV Module

    # BNK module
    path('bnk/', include("bnk.urls", namespace="bnk")),
    # End BNK Module

                  
                  # System module
    path('sy/', include("sy.urls", namespace="sy")),

    # Reports module
    path('rp/', include("rp.urls", namespace="rp")),
    # End System Module

              ] + static(

    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
