from django.urls import path

from redirects.views import RedirectPublicView, RedirectPrivateView

urlpatterns = [
    path('/public/<str:redirect_identifier>', RedirectPublicView.as_view()),
    path('/private/<str:redirect_identifier>', RedirectPrivateView.as_view()),
]