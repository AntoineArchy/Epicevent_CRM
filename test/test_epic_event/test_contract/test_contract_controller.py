# import unittest
# from unittest.mock import MagicMock
#
# from epic_event_CRM.base import context
# from epic_event_CRM.contract.controller import ContractController
# from epic_event_CRM.contract.model import Contract
#
#
# class TestContractController(unittest.TestCase):
#     def test_create_contract(self):
#         # Créer un contexte simulé avec un client
#         context_instance = context.Context("", "")
#         client_mock = MagicMock()
#         client_mock.id = 1
#         context_instance.set_in_context("client", client_mock)
#
#         # Définir le formulaire simulé
#         form_data = {
#             "field1": "value1",
#             "field2": "value2",
#             # ... autres champs du formulaire ...
#         }
#
#         # Appeler la méthode create de ContractController
#         created_contract = ContractController.create(context_instance, form_data)
#
#         # Vérifier que la méthode create de BaseController a été appelée avec les bons arguments
#         ContractController.create.assert_called_once_with(context_instance, form_data)
#
#         # Vérifier que le client ID a été correctement ajouté au formulaire
#         self.assertEqual(created_contract.client_id, client_mock.id)
#
#         # Vérifier que le contrat a été correctement enregistré dans le contexte
#         self.assertEqual(context_instance.get_in_context("contract"), created_contract)
