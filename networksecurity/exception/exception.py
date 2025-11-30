import sys


class NetworkSecurityException(Exception):

    @staticmethod
    def error_message_details(error_message, error_details):
        exc_type, exc_value, exc_tb = error_details
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return (
            f"Error occurred in script '{file_name}' at line {line_number}: "
            f"{str(error_message)}"
        )

    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = NetworkSecurityException.error_message_details(
            error_message, error_detail
        )

    def __str__(self):
        return self.error_message
