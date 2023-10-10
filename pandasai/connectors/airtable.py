"""
Airtable connectors are used to connect airtable records.
"""

from .base import AirtableConnectorConfig, BaseConnector
from typing import Union, Optional
import requests
import pandas as pd
from abc import abstractmethod


class AirtableConnector(BaseConnector):
    """
    Airtable connector to retrieving record data.
    """

    def __init__(
        self,
        baseid: Optional[str] = None,
        bearer_token: Optional[str] = None,
        table_name: Optional[str] = None,
        config: Optional[Union[AirtableConnectorConfig, dict]] = None,
    ):
        if not bearer_token and not config:
            raise ValueError(
                """You must specify bearer token for 
                authentication or a config object."""
            )
        if not baseid and not config["baseID"]:
            raise ValueError(
                """You must specify baseId or
                  a proper config object."""
            )

        if not isinstance(config, AirtableConnectorConfig):
            if not config:
                config = {}
                if table_name:
                    config["table"] = table_name
                if bearer_token:
                    config["token"] = bearer_token
                if baseid:
                    config["baseID"] = baseid

            self.config = AirtableConnectorConfig(**config)
        elif isinstance(config, AirtableConnectorConfig):
            self.config = config

        else:
            raise ValueError(
                """Invalid config parameter. 
                Expected a dict or an AirtableConnectorConfig instance."""
            )

        self._session = requests.Session()
        self._root_url = "https://api.airtable.com/v0/"

        self._session.headers = {"Authorization": f"Bearer {self.config['token']}"}

        self._response: str = None

        super().__init__(self.config)

    def _connect_load(self):
        """
        Authenticate and connect to the instance
        """
        url = f"{self._root_url}{self.config['baseID']}/{self.config['table']}"
        _response = self._session.get(url)
        if _response.status_code == 200:
            self._response = pd.read_json(_response.json())
        else:
            raise ValueError(
                f"""Failed to connect to Airtable. 
                Status code: {_response.status_code}, 
                message: {_response.text}"""
            )

    def head(self):
        """
        Return the head of the table that
          the connector is connected to.

        Returns :
            DatFrameType: The head of the data source
                 that the conector is connected to .
        """
        if self._response:
            return self._response.head()
        else:
            raise ValueError("No data loaded. Please call _connect_load first.")
