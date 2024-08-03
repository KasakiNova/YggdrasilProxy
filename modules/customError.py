class GetPublickeyFailureError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorInfo = ErrorInfo

    def __str__(self):
        return self.errorInfo
