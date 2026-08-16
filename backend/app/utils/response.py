"""统一接口返回格式：{ code, message, data, total? }"""


def success(data=None, message: str = "success", total=None):
    res = {"code": 200, "message": message, "data": data}
    if total is not None:
        res["total"] = total
    return res


def fail(code: int = 400, message: str = "error", data=None):
    return {"code": code, "message": message, "data": data}
