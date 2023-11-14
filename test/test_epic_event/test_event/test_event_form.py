# import unittest
# from datetime import datetime
# from epic_event_CRM.event.form import EventCreationForm
#
#
# class TestEventCreationForm(unittest.TestCase):
#     def setUp(self):
#         self.form = EventCreationForm()
#
#     def test_init(self):
#         self.assertEqual(
#             self.form.fields_display,
#             ["Nom", "Début", "Fin", "Emplacement", "Participants", "Remarques"],
#         )
#         self.assertEqual(len(self.form.questions), 6)
#
#     def test_validate_input_text(self):
#         question = {
#             "type": "text",
#             "name": "test_field",
#             "message": "Test message",
#         }
#
#         user_input = "Test value"
#         result = self.form.validate_input(question, user_input)
#         self.assertEqual(result, {"test_field": "Test value"})
#
#     def test_validate_input_invalid_text(self):
#         question = {
#             "type": "text",
#             "name": "test_field",
#             "message": "Test message",
#         }
#
#         # Simulate invalid user input (empty string)
#         user_input = ""
#         result = self.form.validate_input(question, user_input)
#         self.assertIsNone(result)
#
#     def test_validate_input_date(self):
#         question = {
#             "type": "text",
#             "name": "test_date",
#             "message": "Test date message",
#         }
#
#         # Simulate valid date input
#         user_input = "2023-11-10 15:30"
#         result = self.form.validate_input(question, user_input)
#         expected_date = datetime.strptime("2023-11-10 15:30", "%Y-%m-%d %H:%M")
#         self.assertEqual(result, {"test_date": expected_date})
#
#     def test_validate_input_invalid_date(self):
#         question = {
#             "type": "text",
#             "name": "test_date",
#             "message": "Test date message",
#         }
#
#         # Simulate invalid date input
#         user_input = "invalid_date"
#         result = self.form.validate_input(question, user_input)
#         self.assertIsNone(result)
