class BusinessError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


class ResultNotFoundErrorDomain(BusinessError):
    pass

class UserNotAllowThisResultErrorDomain(BusinessError):
    pass

class PracticeTestsNotFoundErrorDomain(BusinessError):
    # Ném ra khi không tồn tại học phần.
    pass


class QuestionNotFoundErrorDomain(BusinessError):
    pass


class OptionNotFoundErrorDomain(BusinessError):
    pass
