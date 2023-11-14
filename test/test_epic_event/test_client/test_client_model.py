import unittest
from datetime import datetime
from epic_event_CRM.client.model import Client


class TestClient(unittest.TestCase):
    def test_instance_creation(self):
        client = Client(
            full_name="John Doe",
            company_name="ABC Corp",
            email="john.doe@example.com",
            phone="123456789",
        )
        self.assertEqual(client.full_name, "John Doe")
        self.assertEqual(client.company_name, "ABC Corp")
        # Ajoutez des assertions similaires pour les autres champs

    def test_properties(self):
        client = Client(
            full_name="John Doe",
            company_name="ABC Corp",
            email="john.doe@example.com",
            phone="123456789",
        )
        self.assertEqual(client.id, -1)
        self.assertEqual(client.id_name, "client_id")
        self.assertEqual(client.name_display, client.__repr__())

    def test_equality(self):
        client1 = Client(
            full_name="John Doe",
            company_name="ABC Corp",
            email="john.doe@example.com",
            phone="123456789",
        )
        client2 = Client(
            full_name="John Doe",
            company_name="ABC Corp",
            email="john.doe@example.com",
            phone="123456789",
        )
        self.assertEqual(client1, client2)
