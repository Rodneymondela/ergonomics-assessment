# tests/test_smoke_post.py
import pytest

@pytest.mark.usefixtures("app", "client")
def test_all_simple_post_routes(client, app):
    """
    Try POST on routes that don't need URL params. We accept common outcomes.
    CSRF is disabled in tests by conftest, so forms won't block us.
    """
    ACCEPT = {200, 201, 204, 302, 400, 401, 403}
    for rule in app.url_map.iter_rules():
        if "POST" not in rule.methods:
            continue
        if "<" in rule.rule:
            continue
        if rule.rule.startswith("/static"):
            continue
        resp = client.post(rule.rule, data={}, follow_redirects=True)
        assert resp.status_code in ACCEPT
