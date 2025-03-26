import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        self.error_message = self.get_error_message(error_message)

    @staticmethod
    def get_error_message(error_message):
        exc_type, exc_value, tb = sys.exc_info()
        if tb is not None:
            filename = tb.tb_frame.f_code.co_filename
            line_number = tb.tb_lineno
            return f"Error in {filename}, line {line_number}: {error_message}"
        return f"Error: {error_message}"

    def __str__(self):
        return self.error_message