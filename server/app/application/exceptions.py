class ApplicationError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


# ----------------Auth----------------
class EmailExistedError(ApplicationError):
    pass


class InvalidCredentialsError(ApplicationError):
    pass


class AccountNotFoundError(ApplicationError):
    pass

class AccoutHasBeenLocked(ApplicationError):
    pass

# ----------------User----------------
class UserNotFoundError(ApplicationError):
    pass


class UserNotAllowError(ApplicationError):
    pass


# ----------------Course----------------
class CourseNotFoundError(ApplicationError):
    pass


class CourseDetailNotFoundError(ApplicationError):
    pass


# ----------------Test----------------
class PracticeTestsNotFoundError(ApplicationError):
    pass


class QuestionNotFoundError(ApplicationError):
    pass


class OptionNotFoundError(ApplicationError):
    pass

# ----------------Result----------------
class ResultNotFoundError(ApplicationError):
    pass


class UserNotAllowThisResultError(ApplicationError):
    pass
