class AppError(Exception):
    code = 1
class ValidInputError(AppError):
    code = 2
class DataBaseError(AppError):
    code = 3
class NotFoundError(AppError):
    code = 4
