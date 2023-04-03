class Response:
    """Universal Flask server response."""
    def __init__(self, message, data={}):
        self.message = message
        self.data = data
    
    def to_dict(self):
        return self.__dict__
