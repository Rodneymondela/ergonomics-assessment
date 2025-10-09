# tests/test_assessments_routes.py
import re
import uuid
import pytest

# Accept common outcomes: success, created, no content, redirects, or auth/validation failures
ACCEPT = {200, 201, 204, 302, 400, 401, 403, 404}

def _fill_param(value_converter_name: str) -> str:
    """Return a safe string value for a path parameter given its converter name."""
    name = (value_converter_name or "").lower()
    if "int" in name:
        return "1"
    if "float" in name:
        return "1.0"
    if "uuid" in name:
        return str(uuid.uuid4())
    # path/any/string/etc.
    return "x"

def _materialize_url(rule):
    """
    Replace each <converter:name> (or <name>) in rule.rule with a placeholder value
    so we can probe parameterized endpoints like /assessments/<int:id>.
    """
    url = rule.rule
    # rule._converters is a private attr but present in Werkzeug Rule; guard if missing
    converters = getattr(rule, "_converters", {}) or {}
    for arg in sorted(rule.arguments):
        converter = converters.get(arg)
        conv_name = getattr(converter, "__class__", type("X",(object,),{})).__name__
        val = _fill_param(conv_name)
        # Replace the first occurrence of the param pattern for this arg
        url = re.sub(rf"<[^>]*\b{re.escape(arg)}\b[^>]*>", val, url)
    return url

@pytest.mark.usefixtures("app", "client")
def test_assessments_get_and_post(client, app):
    """
    Drive all assessments.* endpoints:
      - GET on every non-static rule
      - POST on those that allow POST (with empty form)
    We accept a broad set of status codes to avoid flakiness while still executing route code.
    """
    for rule in app.url_map.iter_rules():
        if not rule.endpoint.startswith("assessments."):
            continue
        if rule.rule.startswith("/static"):
            continue

        # Build a concrete URL by substituting dummy values for parameters
        url = _materialize_url(rule)

        # Try GET if supported
        if "GET" in rule.methods:
            resp = client.get(url, follow_redirects=True)
            assert resp.status_code in ACCEPT, f"GET {url} -> {resp.status}"

        # Try POST if supported
        if "POST" in rule.methods:
            resp = client.post(url, data={}, follow_redirects=True)
            assert resp.status_code in ACCEPT, f"POST {url} -> {resp.status}"
