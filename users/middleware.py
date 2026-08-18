from django.shortcuts import redirect


class BlockedUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            if hasattr(request.user, "profile"):

                if request.user.profile.is_blocked:
                    return redirect("users:login")

        return self.get_response(request)
