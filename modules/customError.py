class GetPublickeyFailureError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.errorInfo = error_info

    def __str__(self):
        return self.errorInfo
