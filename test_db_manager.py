import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import db_manager

class TestDBManager(unittest.TestCase):

    @patch('db_manager.firestore.client')
    @patch('db_manager.firebase_admin.initialize_app')
    @patch('db_manager.credentials.ApplicationDefault')
    def test_guardar_prediccion_success(self, mock_cred, mock_init, mock_firestore_client):
        # Setup mocks
        mock_db = MagicMock()
        mock_firestore_client.return_value = mock_db
        mock_collection = MagicMock()
        mock_document = MagicMock()
        mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = mock_document

        # Data to test
        sample_data = {
            "partido": "Real Madrid vs Barcelona",
            "prediccion": {
                "ganador": "Local"
            }
        }

        # Call the function
        # Mocking ValueError to simulate first initialization
        with patch('db_manager.firestore.client', side_effect=[ValueError, mock_db]):
            doc_id = db_manager.guardar_prediccion(sample_data)

        # Assertions
        fecha = datetime.now().strftime('%Y-%m-%d')
        expected_doc_id = f"Real_Madrid_vs_Barcelona_{fecha}"

        self.assertEqual(doc_id, expected_doc_id)
        mock_db.collection.assert_called_with('predicciones_partidos')
        mock_collection.document.assert_called_with(expected_doc_id)
        mock_document.set.assert_called_with(sample_data)

    @patch('db_manager.firestore.client')
    def test_guardar_prediccion_already_initialized(self, mock_firestore_client):
        # Setup mocks
        mock_db = MagicMock()
        mock_firestore_client.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = MagicMock()

        sample_data = {"partido": "Team A vs Team B"}

        # Call the function (assuming firestore.client() works immediately)
        db_manager.guardar_prediccion(sample_data)

        # Should NOT call initialize_app if firestore.client() doesn't raise ValueError
        # (Though initialize_db handles this via try/except)
        mock_firestore_client.assert_called()

if __name__ == '__main__':
    unittest.main()
