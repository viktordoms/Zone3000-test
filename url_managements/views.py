
import typing as t
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.errors import error_not_found, error_bad_request, success_response
from libs.exceptions import RedirectRulesNotFoundException
from url_managements.models import RedirectRule
from url_managements.serializers import (
    RedirectRuleSerializer,
    RedirectRuleCreateSerializer,
    RedirectRuleUpdateSerializer
)


class RedirectRulesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request) -> Response:
        try:
            rules = RedirectRule.objects.all()
            serializer = RedirectRuleSerializer(instance=rules, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return error_bad_request(error=str(e))

    def post(self, request) -> Response:
        request.data["owner"] = request.user.id
        serializer = RedirectRuleCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return error_bad_request(error=str(serializer.errors))


class RedirectRuleInstanceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_rule(self, request, uuid: str) -> t.Union[RedirectRule, Response]:
        """ Search redirect rule by uuid and owner """

        redirect_rule = RedirectRule.objects.filter(
            owner=request.user,
            id=uuid,
        ).first()

        if not redirect_rule:
            raise RedirectRulesNotFoundException(f"Not found redirect rule by UUID: {uuid}")

        return redirect_rule


    def get(self, request, uuid: str) -> Response:
        try:
            serializer = RedirectRuleSerializer(instance=self.get_rule(request, uuid))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except RedirectRulesNotFoundException as e:
            return error_not_found(error=str(e))
        except Exception as e:
            return error_bad_request(error=str(e))

    def patch(self, request, uuid: str) -> Response:
        try:
            serializer = RedirectRuleUpdateSerializer(
                instance=self.get_rule(request, uuid),
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                instance = RedirectRuleSerializer(instance=serializer.instance)
                return Response(instance.data, status=status.HTTP_200_OK)

            return error_bad_request(error=str(serializer.errors))

        except RedirectRulesNotFoundException as e:
            return error_not_found(error=str(e))

        except Exception as e:
            return error_bad_request(error=str(e))

    def delete(self, request, uuid: str) -> Response:
        try:
            redirect_rule = self.get_rule(request, uuid)
            redirect_rule.delete()
            return success_response(f"Redirect rule ({uuid}) deleted")

        except RedirectRulesNotFoundException as e:
            return error_not_found(error=str(e))
        except Exception as e:
            return error_bad_request(error=str(e))



