class AuthException(Exception):
    """Base auth exception"""
    pass


class InvalidCredentialsException(AuthException):
    """Invalid username or password"""
    pass


class UserAlreadyExistsException(AuthException):
    """User already exists"""
    pass


class InvalidTokenException(AuthException):
    """Invalid or expired token"""
    pass


class LogParsingException(Exception):
    """Error parsing log file"""
    pass


class DatabaseException(Exception):
    """Database operation error"""
    pass
