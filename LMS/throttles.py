from rest_framework.throttling import SimpleRateThrottle


class BorrowRequestThrottle(SimpleRateThrottle):

    scope = 'borrow_request'

    def get_cache_key(self, request, view):

        # Only authenticated users
        if not request.user or not request.user.is_authenticated:
            return None

        # unique key per user
        return f"borrow_request_{request.user.id}"