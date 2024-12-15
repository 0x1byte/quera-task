from django.contrib import admin

from .models import Form, Question, Answer


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    verbose_name = "سوال"
    verbose_name_plural = "سوالات"
    fields = (
        "title",
        "question_type",
        "required",
        "min_value",
        "max_value",
        "max_length",
        "allow_decimal",
    )


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ["title", "created_at"]
    search_fields = ["title"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "form",
        "title",
        "question_type",
        "required",
        "min_value",
        "max_value",
        "max_length",
        "allow_decimal",
    ]
    list_filter = ["form", "question_type", "required"]
    search_fields = ["title"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        "question",
        "response_text",
        "response_number",
        "response_email",
        "submitted_at",
    ]
    list_filter = ["question", "submitted_at"]
