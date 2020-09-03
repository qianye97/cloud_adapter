class ResponseData(dict):
    def __init__(self, status, message, data):
        super().__init__()
        self['status'] = status
        self['message'] = message
        self['data'] = data
