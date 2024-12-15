from django.core.validators import validate_email

from rest_framework import serializers

from form.models import Form, Question, Answer


class QuestionRetrieveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "title",
            "question_type",
            "required",
            "min_value",
            "max_value",
            "max_length",
            "allow_decimal",
        ]


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ["id", "title", "created_at"]
        read_only_fields = ["created_at"]


class QuestionSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())

    class Meta:
        model = Question
        fields = [
            "id",
            "form",
            "title",
            "question_type",
            "required",
            "min_value",
            "max_value",
            "max_length",
            "allow_decimal",
        ]


class FormRetrieveListSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Form
        fields = ["id", "title", "questions", "created_at"]
        read_only_fields = ["created_at"]


class AnswerRetrieveListSerializer(serializers.ModelSerializer):
    question = QuestionRetrieveListSerializer()

    class Meta:
        model = Answer
        fields = [
            "id",
            "question",
            "response_text",
            "response_number",
            "response_email",
            "submitted_at",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = [
            "id",
            "question",
            "response_text",
            "response_number",
            "response_email",
            "submitted_at",
        ]
        read_only_fields = ["submitted_at"]

    def validate(self, attrs):
        question = attrs.get("question")
        if question.question_type == Question.SHORT_TEXT:
            if not attrs.get("response_text") or len(attrs.get("response_text")) > 200:
                raise serializers.ValidationError(
                    "پاسخ برای سوال کوتاه نباید خالی و یا بیشتر از 200 کاراکتر باشد."
                )
        elif question.question_type == Question.LONG_TEXT:
            if not attrs.get("response_text") or len(attrs.get("response_text")) > 5000:
                raise serializers.ValidationError(
                    "پاسخ برای سوال بلند نباید خالی و یا بیشتر از 5000 کاراکتر باشد."
                )
        elif question.question_type == Question.NUMERIC:
            if attrs.get("response_number") is None:
                raise serializers.ValidationError("پاسخ عددی نباید خالی باشد.")
            if (
                question.min_value is not None
                and attrs.get("response_number") < question.min_value
            ):
                raise serializers.ValidationError(
                    f"پاسخ عددی باید بیشتر از {question.min_value} باشد."
                )
            if (
                question.max_value is not None
                and attrs.get("response_number") > question.max_value
            ):
                raise serializers.ValidationError(
                    f"پاسخ عددی باید کمتر از {question.max_value} باشد."
                )
            if not question.allow_decimal:
                if attrs.get("response_number") != int(attrs.get("response_number")):
                    raise serializers.ValidationError("پاسخ عددی باید صحیح باشد.")

        elif question.question_type == Question.EMAIL:
            if not attrs.get("response_email"):
                raise serializers.ValidationError("پاسخ ایمیل نباید خالی باشد.")
            try:
                validate_email(attrs.get("response_email"))
            except Exception:
                raise serializers.ValidationError("ایمیل وارد شده معتبر نیست.")
        return attrs
