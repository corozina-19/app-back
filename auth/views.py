from rest_framework_simplejwt.views import TokenViewBase

from auth.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomTokenObtainPairSerializer


token_obtain_pair = CustomTokenObtainPairView.as_view()