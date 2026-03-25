class BusinessError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


class CoursesNotFoundErrorDomain(BusinessError):
    # Ném ra khi không tồn tại học phần.
    pass


class CourseDetailsNotFoundErrorDomain(BusinessError):
    # Ném ra khi không tồn tại chi tiết học phần.
    pass
