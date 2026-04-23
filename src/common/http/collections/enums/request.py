import enum


class HTTPHeader(enum.StrEnum):
    authorization = "authorization"
    cookie = "cookie"
    set_cookie = "set-cookie"
    x_api_key = "x-api-key"
    proxy_authorization = "proxy-authorization"
    www_authenticate = "www-authenticate"
    x_forwarded_for = "x-forwarded-for"
    x_real_ip = "x-real-ip"
    x_csrf_token = "x-csrf-token"
    x_xsrf_token = "x-xsrf-token"
    x_auth_token = "x-auth-token"
    x_cache_hit = "x-cache-hit"
    accept_language = "accept-language"
