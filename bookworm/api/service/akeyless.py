from akeyless.rest import ApiException
from dotenv import load_dotenv

from bookworm.api.decorator.logIt import logIt

import akeyless
import os

# Load environment variables without exporting the variables explicitly by the export command
load_dotenv()


class Akeyless:
    def __init__(self, *args, **kwargs):
        from bookworm.api.service.customLog import CustomLog

        self.log = CustomLog()

        try:
            self.access_id: str = os.environ.get("AKEYLESS_ACCESS_ID")
            self.access_key: str = os.environ.get("AKEYLESS_ACCESS_KEY")

        except ApiException as e:
            self.log.logThis("Akeyless.__init__", str(e), "error")
            raise ValueError(
                ">>> Error with Akeyless. Cannot retrieve access ID and access key."
            )

        try:
            # Defining the host is optional and defaults to https://api.akeyless.io
            # default: public API Gateway
            self.config = akeyless.Configuration(host="https://api.akeyless.io")

        except ApiException as e:
            self.log.logThis("Akeyless.__init__", str(e), "error")
            raise ValueError(
                ">>> Error with Akeyless. Cannot configure host using public API endpoint."
            )

    @logIt("get_vault_secret", "Retrieving secret from vault.")
    def get_vault_secret(self, key: str, *args, **kwargs) -> str:
        """Get a secret from the vault."""

        with akeyless.ApiClient(self.config) as api_client:
            try:
                api = akeyless.V2Api(api_client)

                _res = api.auth(
                    akeyless.Auth(access_id=self.access_id, access_key=self.access_key)
                )
                _token = _res.token

                resp = api.get_secret_value(
                    akeyless.GetSecretValue(names=[key], token=_token)
                )

            except ApiException as e:
                self.log.logThis("Akeyless.get_vault_secret", str(e), "error")
                return ""

        self.log.logThis(
            "Akeyless.get_vault_secret",
            f" Key: {key}, Value: {resp[key]}",
        )
        return resp[key]
