headers = {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}
class AppError(Exception):
    code = 500
class ValidInputError(AppError):
    code = 400
class DataBaseError(AppError):
    code = 502
class NotFoundError(AppError):
    code = 404
class ExpiredError(AppError):
    code = 200