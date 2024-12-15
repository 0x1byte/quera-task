from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class Form(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در")

    def __str__(self):
        return self.title


class Question(models.Model):
    SHORT_TEXT = "short_text"
    LONG_TEXT = "long_text"
    EMAIL = "email"
    NUMERIC = "numeric"
    QUESTION_TYPES = (
        (SHORT_TEXT, "متن کوتاه پاسخ"),
        (LONG_TEXT, "متن بلند پاسخ"),
        (EMAIL, "ایمیل"),
        (NUMERIC, "پاسخ عددی"),
    )
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    title = models.CharField(max_length=300, verbose_name="متن سوال")
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        verbose_name="نوع سوال",
    )
    required = models.BooleanField(default=False, verbose_name="اجباری است؟")
    min_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="کمترین مقدار (برای سوال عددی)",
    )
    max_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="بیشترین مقدار (برای سوال عددی)",
    )
    max_length = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="حداکثر طول (برای متن)"
    )
    allow_decimal = models.BooleanField(
        default=True, verbose_name="مجاز به اعشار (برای عددی)"
    )

    def clean(self):
        if self.question_type == self.SHORT_TEXT and (
            self.max_length is None or self.max_length > 200
        ):
            raise ValidationError(
                "طول مجاز برای سوالات کوتاه نباید بیش از 200 کاراکتر باشد."
            )
        if self.question_type == self.LONG_TEXT and (
            self.max_length is None or self.max_length > 5000
        ):
            raise ValidationError(
                "طول مجاز برای سوالات بلند نباید بیش از 5000 کاراکتر باشد."
            )
        if self.question_type == self.NUMERIC and (
            self.min_value is not None
            and self.max_value is not None
            and self.min_value > self.max_value
        ):
            raise ValidationError("کمترین مقدار باید کمتر از بیشترین مقدار باشد.")
        if self.question_type == self.NUMERIC and (
            self.min_value is not None and self.min_value < 0
        ):
            raise ValidationError("کمترین مقدار باید بزرگتر از 0 باشد.")
        if self.question_type == self.NUMERIC and (
            self.max_value is not None and self.max_value < 0
        ):
            raise ValidationError("بیشترین مقدار باید بزرگتر از 0 باشد.")

        super().clean()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="answers",
        on_delete=models.CASCADE,
        verbose_name="سوال",
    )
    response_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="متن پاسخ",
    )
    response_number = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="پاسخ عددی",
    )
    response_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="پاسخ ایمیل",
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ارسال پاسخ"
    )

    def clean(self):
        if self.question.question_type == Question.SHORT_TEXT:
            if not self.response_text or len(self.response_text) > 200:
                raise ValidationError(
                    "پاسخ برای سوال کوتاه نباید خالی و یا بیشتر از 200 کاراکتر باشد."
                )
        elif self.question.question_type == Question.LONG_TEXT:
            if not self.response_text or len(self.response_text) > 5000:
                raise ValidationError(
                    "پاسخ برای سوال بلند نباید خالی و یا بیشتر از 5000 کاراکتر باشد."
                )
        elif self.question.question_type == Question.NUMERIC:
            if self.response_number is None:
                raise ValidationError("پاسخ عددی نباید خالی باشدد.")
            elif self.question.min_value is not None and self.response_number < self.question.min_value:
                raise ValidationError(
                    "پاسخ عددی باید بزرگتر از کمترین مقدار باشد."
                )
            elif self.question.max_value is not None and self.response_number > self.question.max_value:
                raise ValidationError(
                    "پاسخ عددی باید کمتر از بیشترین مقدار باشد."
                )
            elif not self.question.allow_decimal and "." in str(self.response_number):
                raise ValidationError("پاسخ عددی باید بدون اعشار باشد.")
        elif self.question.question_type == Question.EMAIL:
            if not self.response_email:
                raise ValidationError("پاسخ ایمیل نباید خالی باشد.")
            try:
                validate_email(self.response_email)
            except ValidationError:
                raise ValidationError("ایمیل وارد شده معتبر نیست.")
        super().clean()

    def __str__(self):
        return f"پاسخ به سوال: {self.question.title}"
