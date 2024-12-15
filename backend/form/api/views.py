from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from form.models import Form, Question, Answer

from .serializers import FormSerializer
from .serializers import FormRetrieveListSerializer
from .serializers import QuestionSerializer
from .serializers import QuestionRetrieveListSerializer
from .serializers import AnswerSerializer
from .serializers import AnswerRetrieveListSerializer


class FormViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Form.objects.prefetch_related("questions").all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return FormSerializer
        return FormRetrieveListSerializer


class QuestionViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return QuestionSerializer
        return QuestionRetrieveListSerializer


class AnswerViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Answer.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AnswerSerializer
        return AnswerRetrieveListSerializer
