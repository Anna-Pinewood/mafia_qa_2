# Sports Mafia Assistant - Technical Specification
The Sports Mafia Presenter Assistant is a Telegram bot designed to help game presenters quickly resolve rule questions during live games. 

## 1. Core Components & Technology Stack

### 1.1 LLM Integration (src/llm_interface.py)
- **Primary Technology**: RunPod API / Mistral api
- **Key Dependencies**: 
  - runpod-python (API client)
  - langchain for prompt management
- **Core Functionality**:
  - API calls handling
  - Error handling and retries
  - Prompt templating

### 1.2 Vector Database Layer (src/database/)
- **Primary Technology**: ChromaDB
- **Embedding Model**: multilingual-e5-large (supports Russian well)
- **Key Dependencies**:
  - chromadb
  - sentence-transformers
- **Core Functionality**:
  - Similarity search for QnA pairs
  - Context retrieval for rules fragments
  - Batch document processing
  - Collection management

### 1.3 History Storage (src/database/)
- **Primary Technology**: SQLite
- **Key Dependencies**: 
  - SQLAlchemy for ORM
  - alembic for migrations
- **Core Functionality**:
  - Store user interactions
  - Basic analytics queries

### 1.4 Telegram Interface (src/main.py)
- **Primary Technology**: python-telegram-bot
- **Key Dependencies**:
  - python-telegram-bot[job-queue]
- **Core Functionality**:
  - Message handling
  - Command processing
  - Error reporting

### 1.5 Configuration Management
- **Primary Technology**: OmegaConf
- **Core Functionality**:
  - Environment-based configuration
  - Secrets management
  - Runtime configuration updates

## 2. Data Models (src/database/models/)

### 2.1 QnAPair
```python
class QnAPair(BaseModel):
    question: str
    answer: str
    embedding: Optional[List[float]]
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

### 2.2 RuleFragment
```python
class RuleFragment(BaseModel):
    text: str
    section: str  # Rule section identifier
    embedding: Optional[List[float]]
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

### 2.3 UserInteraction
```python
class UserInteraction(BaseModel):
    question: str
    response_type: Literal["qna", "rag"]
    timestamp: datetime
    response: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

## 3. Development Environment
- docker based development