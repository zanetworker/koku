#
# Copyright 2020 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Sources Error Message."""
import logging

from rest_framework.serializers import ValidationError

from providers.provider_errors import ProviderErrors

LOG = logging.getLogger(__name__)


class SourcesErrorMessage:
    """Sources Error Message for Sources API service."""

    def __init__(self, error):
        """Initialize the message generator."""
        self._error = error

    @property
    def error_msg(self):
        err_msg = None
        if isinstance(self._error, ValidationError):
            _, err_msg = self._extract_from_validation_error()
        else:
            err_msg = str(self._error)
        return err_msg

    def azure_client_errors(self, message):
        """Azure client error messages."""
        message = ProviderErrors.AZURE_GENERAL_CLIENT_ERROR_MESSAGE
        if "http error: 401" in message:
            message = ProviderErrors.AZURE_INCORRECT_CLIENT_SECRET_MESSAGE
        if "http error: 400" in message:
            message = ProviderErrors.AZURE_INCORRECT_CLIENT_ID_MESSAGE
        if "ResourceGroupNotFound" in message:
            message = ProviderErrors.AZURE_INCORRECT_RESOURCE_GROUP_MESSAGE
        if "ResourceNotFound" in message:
            message = ProviderErrors.AZURE_INCORRECT_STORAGE_ACCOUNT_MESSAGE
        if "SubscriptionNotFound" in message:
            message = ProviderErrors.AZURE_INCORRECT_SUBSCRIPTION_ID_MESSAGE
        return message

    def aws_client_errors(self, message):
        """AWS client error messages."""
        return ProviderErrors.AWS_RESOURCE_NAME_UNREACHABLE_MESSAGE

    def aws_no_billing_source(self, message):
        """AWS no bucket message."""
        return ProviderErrors.AWS_BILLING_SOURCE_NOT_FOUND_MESSAGE

    def _display_string_function(self, key):
        """Return function to get user facing string."""
        ui_function_map = {
            ProviderErrors.AZURE_CLIENT_ERROR: self.azure_client_errors,
            ProviderErrors.AWS_RESOURCE_NAME_UNREACHABLE: self.aws_client_errors,
            ProviderErrors.AWS_BILLING_SOURCE_NOT_FOUND: self.aws_no_billing_source,
        }
        string_function = ui_function_map.get(key)
        return string_function

    def _extract_from_validation_error(self):
        """Extract key and message from ValidationError."""
        err_key = None
        err_msg = None
        if isinstance(self._error, ValidationError):
            err_dict = self._error.detail
            err_key = list(err_dict.keys()).pop()
            err_body = err_dict.get(err_key).pop()
            err_msg = err_body.encode().decode("UTF-8")
        return err_key, err_msg

    def display(self):
        """Generate user friendly message."""
        if isinstance(self._error, ValidationError):
            key, msg = self._extract_from_validation_error()
            LOG.info(f"Error Status key: {str(key)} msg: {str(msg)}")
            display_fn = self._display_string_function(key)
            if display_fn:
                msg = display_fn(msg)
        else:
            msg = str(self._error)
        return msg
