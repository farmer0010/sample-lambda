class ApplicationError(Exception):
    pass


class AuthenticationError(ApplicationError):
    pass


class AuthDeviceFlowError(AuthenticationError):
    pass
