# tests/test_smoke.py
import pytest
from app import create_app

def test_app_factory_smoke():
    app = create_app()              # no keyword arg
    app.config.update(TESTING=True)
    assert app is not None
    assert app.testing is True

@pytest.mark.usefixtures("app", "client")
def test_all_simple_get_routes(client, app):
    """
    Auto-discover GET routes that don't need URL params and try to load them.
    Accept 200/302/401/403 to account for auth redirects.
    """
    for rule in app.url_map.iter_rules():
        if "GET" not in rule.methods:
            continue
        if "<" in rule.rule:              # skip param routes
            continue
        if rule.rule.startswith("/static"):
            continue

        resp = client.get(rule.rule, follow_redirects=True)
        assert resp.status_code in (200, 302, 401, 403)
