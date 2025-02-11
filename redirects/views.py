
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.errors import error_not_found, error_bad_request
from url_managements.models import RedirectRule
from url_managements.serializers import RedirectRuleSerializer


class RedirectPublicView(APIView):

    def get(self, request, redirect_identifier: str) -> Response:
        try:
            redirect = RedirectRule.objects.filter(
                redirect_identifier=redirect_identifier,
                is_private=False
            ).first()
            if not redirect:
                return error_not_found(
                    f"Public URL rule not found with identifier: {redirect_identifier}"
                )
            serializer = RedirectRuleSerializer(redirect)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        except Exception as e:
            return error_bad_request(str(e))


class RedirectPrivateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, redirect_identifier: str) -> Response:
        try:
            redirect = RedirectRule.objects.filter(
                redirect_identifier=redirect_identifier,
                is_private=True
            ).first()
            if not redirect:
                return error_not_found(
                    f"Private URL rule not found with identifier: {redirect_identifier}"
                )
            serializer = RedirectRuleSerializer(redirect)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        except Exception as e:
            return error_bad_request(str(e))
