import httpx

client = httpx.Client()


def get_http_client() -> httpx.Client:
    return client