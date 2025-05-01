import contextvars

request_id_ctx_var = contextvars.ContextVar("request_id", default="-")

def get_request_id():
    return request_id_ctx_var.get()

def set_request_id(request_id: str):
    request_id_ctx_var.set(request_id)
