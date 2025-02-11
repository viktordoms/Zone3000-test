from django.urls import path

from url_managements.views import RedirectRulesView, RedirectRuleInstanceView

urlpatterns = [
    path('', RedirectRulesView.as_view()),
    path('/<str:uuid>', RedirectRuleInstanceView.as_view()),
]