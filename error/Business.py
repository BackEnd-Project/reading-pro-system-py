import error
class Business(Exception):
    def __init__(self, code, message = ""):
        self.code = code
        self.message = error.get_error_message(code)