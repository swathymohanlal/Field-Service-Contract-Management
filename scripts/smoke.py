"""Check the foundation contracts against an already running local host."""

import argparse
import json
from urllib.error import HTTPError
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", nargs="?", default="http://127.0.0.1:5080")
    base_url = parser.parse_args().base_url.rstrip("/")

    def get(path):
        with urlopen(base_url + path, timeout=5) as response:
            return response.headers.get_content_type(), response.read()

    content_type, health = get("/health/live")
    if content_type != "text/plain" or health.decode().strip() != "Healthy":
        raise RuntimeError("Unexpected liveness response")

    content_type, metadata = get("/api/v1/platform")
    expected = {
        "product": "Field Service & Contract Management",
        "phase": "P00",
        "profile": "foundation",
        "version": "0.1.0",
    }
    if content_type != "application/json" or json.loads(metadata) != expected:
        raise RuntimeError("Unexpected platform metadata")

    content_type, page = get("/")
    if content_type != "text/html" or b'id="refresh"' not in page:
        raise RuntimeError("Status page is unavailable")
    for path, media_types in [
        ("/platform.css", {"text/css"}),
        ("/platform.js", {"text/javascript", "application/javascript"}),
    ]:
        content_type, asset = get(path)
        if content_type not in media_types or not asset:
            raise RuntimeError(f"Invalid asset response: {path}")

    try:
        get("/api/v1/work-orders")
    except HTTPError as error:
        if error.code != 404:
            raise
    else:
        raise RuntimeError("Expected a 404 for the work-order route")

    print("PASS: liveness, platform metadata, UI and assets, work-order route returns 404")


if __name__ == "__main__":
    main()
