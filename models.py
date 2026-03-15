from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ContentBlock(BaseModel):
    title: Optional[str] = None
    content: str
    page: Optional[int] = None


class ExtractedData(BaseModel):
    full_text: str
    blocks: List[ContentBlock] = []
    metadata: Dict[str, Any] = {}
