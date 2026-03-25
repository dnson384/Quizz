class BusinessError(Exception):
    # Lỗi nghiệp vụ cơ sở (base class)
    pass


class EmailAlreadyExistsError(BusinessError):
    # Ném ra khi email đăng ký đã tồn tại.
    pass


class AccountNotFoundError(BusinessError):
    # Ném ra khi tìm kiếm một tài khoản không tồn tại.
    pass


class InvalidCredentialsError(BusinessError):
    # Ném ra khi sai email hoặc mật khẩu lúc đăng nhập.
    pass


class WrongAuthMethodError(BusinessError):
    # Ném ra khi người dùng cố đăng nhập bằng phương thức sai (vd: email thay vì Google).
    pass