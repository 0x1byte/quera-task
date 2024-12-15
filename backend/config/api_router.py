from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from google_forms_clone.users.api.views import UserViewSet
from form.api.views import FormViewSet
from form.api.views import QuestionViewSet
from form.api.views import AnswerViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("forms", FormViewSet)
router.register("questions", QuestionViewSet)
router.register("answers", AnswerViewSet)


app_name = "api"
urlpatterns = router.urls
