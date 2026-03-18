import os
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class UploadFileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("upload_file")  # имя твоего view в urls.py
        self.test_dir = os.path.join(settings.BASE_DIR, "roads", "test_files")

    def upload_test_file(self, filename):
        path = os.path.join(self.test_dir, filename)
        with open(path, "rb") as f:
            uploaded_file = SimpleUploadedFile(
                filename,
                f.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        return self.client.post(self.url, {"file": uploaded_file})

    def test_valid_file(self):
        response = self.upload_test_file("valid_roads.xlsx")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Скачать отчет")

    def test_empty_file(self):
        response = self.upload_test_file("empty_file.xlsx")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Excel файл не содержит данных")

    def test_wrong_columns(self):
        response = self.upload_test_file("wrong_columns.xlsx")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Некорректные колонки в Excel файле")

    def test_negative_length(self):
        response = self.upload_test_file("negative_length.xlsx")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Протяженность не может быть отрицательной")

    def test_bad_numbers(self):
        response = self.upload_test_file("bad_numbers.xlsx")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Некорректные значения в колонке Протяженность, км"
        )
