import pytest
from rag_assisted_bots import GithubAssistant
import os

# Mock constants if they are not available from the package directly or just use literals for tests
GPT_MODEL_NAME = "gpt-5-mini"
TEMPERATURE = 0.5
VECTORDB_PATH = "./vector_db"
COLLECTION_NAME = "my_embeddings"

@pytest.fixture(scope="module")
def assistant():
    # Ensure environment variables are set or handled if needed for the GithubAssistant to initialize
    # For CI/CD, these should be in the environment secrets
    
    # We might need to mock the vector db path or ensure it exists
    # For now, we assume the environment where tests run has the necessary setup or we mock it
    # However, since this looks like an integration test, we try to initialize it for real
    
    return GithubAssistant(
        gpt_model_name=GPT_MODEL_NAME,
        vectordb_path=VECTORDB_PATH,
        collection_name=COLLECTION_NAME,
        temperature=TEMPERATURE,
        rag_activated=True
    )

test_question = "Tell me about a project where you worked on these skills: Flask, Python, AWS, LLM, RAG, ChromaDB, VectorDB etc."

def test_chat_response_structure(assistant):
    """
    Test if the chat_with_model method returns the expected dictionary structure.
    """
    # We might need to mock the actual LLM call if we don't want to spend tokens or if no API key in some envs
    # But usually 'workflow' implies we might want real tests or mocked tests.
    # Given the previous code called `chatWithModel`, we'll assume we checking the real output or a mocked one.
    # If we can't mock easily without more info, we'll write the test determining structure.
    
    try:
        # Note: accurate testing requires OPENAI_API_KEY.
        response_data = assistant.chat_with_model(test_question)
        
        assert isinstance(response_data, dict), "Response must be a dictionary."
        assert 'response' in response_data, "Missing 'response' key."
        assert 'rag_relevance' in response_data, "Missing 'rag_relevance' key."
        
        response_model = response_data['response']
        # Check if it has expected attributes (pydantic model or dict)
        # Based on app.py usage: response_model.response_message, etc.
        assert hasattr(response_model, 'response_message') or isinstance(response_model, dict)
        
    except Exception as e:
        pytest.fail(f"GithubAssistant chat failed: {e}")
