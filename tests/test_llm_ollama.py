from app.llm.ollama import OllamaClient


def test_ollama_generate():
    client = OllamaClient()

    response = client.generate(
        "Return only the word: SUCCESS"
    )

    assert response
    assert "SUCCESS" in response.upper()