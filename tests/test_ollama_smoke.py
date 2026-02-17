import pytest

pytestmark = pytest.mark.integration

DEFAULT_MODEL = "qwen2-math:7b"


def test_ollama_smoke():
    """
    Smoke test: Ollama is usable and the configured model returns a non-empty response.
    Skips if Ollama isn't running or the model isn't available.
    """
    # Import inside the test so unit test runs don't fail if ollama isn't installed.
    try:
        from ollama import chat
    except Exception as e:
        pytest.skip(f"ollama Python package not available: {e}")

    try:
        resp = chat(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer in English only."
                    "Do not use any non-English characters.",
                },
                {
                    "role": "user",
                    "content": "Compute 37*13. Reply with only the number.",
                },
            ],
            options={"temperature": 0.0, "num_predict": 16},
        )
    except Exception as e:
        # Covers: Ollama server not running, model not pulled, connection errors, etc.
        pytest.skip(f"Ollama not available or model not pulled ({DEFAULT_MODEL}): {e}")

    text = (getattr(resp, "message", None) and resp.message.content) or ""
    text = text.strip()

    assert text, "Empty model response"
    assert "481" in text, f"Unexpected response: {text!r}"
