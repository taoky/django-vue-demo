from django.http.response import JsonResponse


def response(code=0, msg="", **kwargs):
    if code == 1:
        msg = "User already exists!"
    elif code == 2:
        msg = "Please logout first!"
    elif code == 3:
        msg = "Wrong username or password!"
    elif code == 4:
        msg = "Please login first!"
    return JsonResponse({**{"code": code, "msg": msg}, **kwargs})
