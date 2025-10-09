# tests/test_media_routes.py
import pytest

ACCEPT = ACCEPT = {200, 201, 204, 302, 400, 401, 403, 404, 405}


@pytest.mark.usefixtures("app", "client")
def test_media_get_and_post(client, app):
    for rule in app.url_map.iter_rules():
        if not rule.endpoint.startswith("media."):
            continue
        if rule.rule.startswith("/static"):
            continue
        url = rule.rule
        if "GET" in rule.methods:
            r = client.get(url, follow_redirects=True)
            assert r.status_code in ACCEPT
        if "POST" in rule.methods:
            r = client.post(url, data={}, follow_redirects=True)
            assert r.status_code in ACCEPT
