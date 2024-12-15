from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase

from form.models import Form, Question


class FormTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.form_data = {
            "title": "Test Form",
        }

    def test_create_form(self):
        response = self.client.post("/api/forms/", self.form_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.form_data["title"])

        form_id = response.data["id"]
        self.assertIsInstance(form_id, int)


class QuestionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.form_data = {
            "title": "Test Form",
        }
        self.form = Form.objects.create(**self.form_data)
        self.question_data = {
            "form": self.form.id,
            "title": "Test Question",
            "question_type": Question.SHORT_TEXT,
            "max_length": 100,
        }

    def test_create_question(self):
        response = self.client.post("/api/questions/", self.question_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.question_data["title"])
        self.assertEqual(
            response.data["question_type"], self.question_data["question_type"]
        )

        question_id = response.data["id"]
        self.assertIsInstance(question_id, int)


class AnswerTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.form_data = {
            "title": "Test Form",
        }
        self.form = Form.objects.create(**self.form_data)
        self.question_data = {
            "form": self.form,
            "title": "Test Question",
            "question_type": Question.SHORT_TEXT,
            "max_length": 100,
        }
        self.question = Question.objects.create(**self.question_data)
        self.answer_data = {
            "question": self.question.id,
            "response_text": "Test Answer",
        }

    def test_create_answer(self):
        response = self.client.post("/api/answers/", self.answer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["response_text"], self.answer_data["response_text"]
        )

        answer_id = response.data["id"]
        self.assertIsInstance(answer_id, int)
