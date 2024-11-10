class ErrorInGettingPublickeysFromMojang(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.errorInfo = error_info

    def __str__(self):
        return self.errorInfo

class ErrorInGettingPublickeysFromLittleSkin(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.errorInfo = error_info

    def __str__(self):
        return self.errorInfo

class FailureToFetchProfile(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.errorInfo = error_info

    def __str__(self):
        return self.errorInfo


class ProxyError(Exception):
    def __init__(self):
        super().__init__(self)
        self.errorInfo = "Proxy Error"

    def __str__(self):
        return self.errorInfo
