import unittest
import pandas 
from unittest.mock import Mock, patch
from pandasai.connectors.base import AirtableConnectorConfig
from pandasai.connectors import AirtableConnector
import requests

class TestAirTableConnector(unittest.TestCase):
    def setUp(self):

        # Define your ConnectorConfig instance here
        self.config = AirtableConnectorConfig(
            token="your_token",
            baseID="your_baseid",
            table="your_table_name"
        ).dict()

        #Create an instance of Connector 
        self.connector = AirtableConnector(config=self.config)

    @patch("requests.Session")
    def test_constructor_and_properties(self,mock_request_session):
        # Test constructor and properties
        self.assertEqual(self.connector._config,self.config)
        self.assertEqual(self.connector._session,mock_request_session)
        self.assertEqual(self.connector._session.headers, {
            "Authorization" : f"Bearer {self.config['token']}"
        })

    @patch("pandas.DataFrame")
    def test_connect_load(self,mock_dataframe):
        self.connector._connect_load(self.config)
        self.assertEqual(type(self.connector._response),mock_dataframe())
    
    @patch("pandas.DataFrame")
    def test_head(self,mock_dataframe):
        response = self.connector.head()
        self.assertEqual(type(response),mock_dataframe())
        self.assertEqual(len(response),5)
        
        