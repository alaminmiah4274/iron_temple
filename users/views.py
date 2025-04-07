from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request (passed via Authorization header)
            refresh_token = request.data.get("refresh")

            # Check if the token exists
            if refresh_token is None:
                return Response({"detail": "Refresh token is required"}, status=400)

            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()  # SimpleJWT's built-in blacklist functionality

            return Response({"detail": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
