from typing import TypedDict, List, Optional

class RetrievedDocument(TypedDict):
    id: int
    title: str
    content: str
    score: float


class AgentState(TypedDict):
    query: str
    intent: Optional[str]
    documents: List[dict]
    answer: Optional[str]
    use_web: Optional[bool]

