# tests/test_smoke_post.py
import pytest

ACCEPT = {200, 201, 204, 302, 400, 401, 403}

@pytest.mark.usefixtures("app", "client")
def test_all_simple_post_routes(client, app):
    """
    Try POST on routes that don't need URL params.
    CSRF is disabled in tests (see conftest), so this will reach views that
    accept POST without complex payloads.
    """
    for rule in app.url_map.iter_rules():
        if "POST" not in rule.methods:
            continue
        if "<" in rule.rule:
            continue                      # skip parameterized routes
        if rule.rule.startswith("/static"):
            continue

        resp = client.post(rule.rule, data={}, follow_redirects=True)
        assert resp.status_code in ACCEPT
