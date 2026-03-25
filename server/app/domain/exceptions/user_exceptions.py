class BusinessError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


class UserNotFoundErrorDomain(BusinessError):
    # Ném ra khi không tồn tại học phần.
    pass
