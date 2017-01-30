from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class RestrictAdminMiddleware(object):
    """
    Restricts access to the admin page to
    only logged-in users with a certain user-level.
    """
    def process_request(self, request):
        if request.path == reverse("admin:index"):
            if not (request.user.is_active and request.user.is_admin):
                return HttpResponseRedirect("/")
