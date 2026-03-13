import io
import ipaddress
import socket
import typing
import urllib.parse
import urllib.request

from rfc3986 import uri_reference


def parse(url: str) -> urllib.parse.ParseResult:
    return urllib.parse.urlparse(url)


def check(scheme: str) -> bool:
    return scheme in ("http", "https")


def join(domain: str, path: str) -> str:
    return urllib.parse.urljoin(domain, path)


def download(path: str) -> io.BytesIO:
    with urllib.request.urlopen(path) as response:
        return io.BytesIO(response.read())


def safe(url: str) -> bool:
    try:
        parsed = parse(url)

        if not check(parsed.scheme):
            return False

        host = parsed.hostname

        if not host:
            return False

        ip = socket.gethostbyname(host)

        addr = ipaddress.ip_address(ip)

        if addr.is_private or addr.is_loopback:
            return False

        return True

    except Exception:
        return False


def allowed(url: str, domains: list[str]) -> bool:
    parsed = parse(url)

    host = parsed.hostname

    if not host:
        return False

    for domain in domains:
        if host == domain or host.endswith("." + domain):
            return True

    return False


def normalize(url: str) -> typing.Any:
    return uri_reference(url).normalize().unsplit()


def equal(first: str, second: str) -> typing.Any:
    return normalize(first) == normalize(second)
