# tests/test_blueprint_sweeps.py
import pytest

ACCEPT = {200, 201, 204, 302, 400, 401, 403}
BLUEPRINTS = ("api", "org", "jobs", "auth", "media", "assessments")

def _probe(client, app, prefix, verbs):
    for rule in app.url_map.iter_rules():
        if not rule.endpoint.startswith(prefix + "."):
            continue
        if "<" in rule.rule or rule.rule.startswith("/static"):
            continue
        for v in verbs:
            if v not in rule.methods:
                continue
            resp = client.get(rule.rule, follow_redirects=True) if v == "GET" \
                else client.post(rule.rule, data={}, follow_redirects=True)
            assert resp.status_code in ACCEPT

@pytest.mark.usefixtures("app", "client")
@pytest.mark.parametrize("bp", BLUEPRINTS)
def test_blueprints_get_post(client, app, bp):
    _probe(client, app, bp, ("GET", "POST"))
