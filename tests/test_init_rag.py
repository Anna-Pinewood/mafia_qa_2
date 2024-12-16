import pytest
from unittest.mock import Mock, patch
from src.database.init_rag import init_collections
import chromadb
from chromadb.config import Settings

@pytest.fixture
def mock_chroma_client():
    with patch('chromadb.HttpClient') as mock_client:
        client_instance = Mock()
        client_instance.heartbeat.return_value = "OK"
        client_instance.list_collections.return_value = []
        mock_client.return_value = client_instance
        yield mock_client

def test_successful_connection(mock_chroma_client):
    client = init_collections()
    mock_chroma_client.assert_called_once()
    assert client.heartbeat() == "OK"

def test_collections_creation(mock_chroma_client):
    client = init_collections()
    
    # Verify both collections were created
    create_collection_calls = client.create_collection.call_args_list
    assert len(create_collection_calls) == 2
    
    # Verify qna_pairs collection
    qna_call = next(call for call in create_collection_calls 
                    if call.kwargs['name'] == 'qna_pairs')
    assert qna_call.kwargs['metadata']['description'] == "QnA pairs collection"
    
    # Verify rule_fragments collection
    rules_call = next(call for call in create_collection_calls 
                     if call.kwargs['name'] == 'rule_fragments')
    assert rules_call.kwargs['metadata']['description'] == "Rule fragments collection"

def test_existing_collections_not_recreated(mock_chroma_client):
    # Create proper mock collections with name property
    qna_collection = Mock()
    qna_collection.name = 'qna_pairs'
    rules_collection = Mock()
    rules_collection.name = 'rule_fragments'
    
    existing_collections = [qna_collection, rules_collection]
    client_instance = mock_chroma_client.return_value
    client_instance.list_collections.return_value = existing_collections
    
    client = init_collections()
    
    # Verify no new collections were created
    assert not client_instance.create_collection.called

def test_connection_error(mock_chroma_client):
    mock_chroma_client.side_effect = Exception("Connection failed")
    
    with pytest.raises(Exception) as exc_info:
        init_collections()
    assert "Connection failed" in str(exc_info.value)
