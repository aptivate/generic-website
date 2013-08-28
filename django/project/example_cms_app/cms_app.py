from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ExampleCmsApp(CMSApp):
    name = _("Example CMS App")
    urls = ["example_cms_app.urls"]

apphook_pool.register(ExampleCmsApp)
