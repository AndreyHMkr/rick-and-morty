from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from characters.models import Character


class RandomCharacterTests(TestCase):
    def setUp(self):
        Character.objects.create(api_id=1, name="Rick Sanchez", image="rick.png")
        Character.objects.create(api_id=2, name="Morty Smith", image="morty.png")
        Character.objects.create(api_id=3, name="Summer Smith", image="summer.png")

    def test_get_random_character(self):
        response = self.client.get(reverse("characters:character-random"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertIn(
            response.data["name"], ["Rick Sanchez", "Morty Smith", "Summer Smith"]
        )


class CharacterModelErrorTests(TestCase):
    def test_character_model_error_with_duplicate_api(self):
        Character.objects.create(api_id=1, name="Rick Sanchez")

        with self.assertRaises(IntegrityError):
            Character.objects.create(api_id=1, name="Morty Smith")
