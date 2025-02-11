from rest_framework import serializers

from url_managements.models import RedirectRule


class RedirectRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedirectRule
        fields = '__all__'


class RedirectRuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedirectRule
        fields = ("redirect_url", "is_private", "owner")


class RedirectRuleUpdateSerializer(serializers.ModelSerializer):
    is_private = serializers.BooleanField(required=True, allow_null=False)

    class Meta:
        model = RedirectRule
        fields = ("is_private",)
