from pydantic import BaseModel


class TextAnalysisRequest(BaseModel):
    text: str


class RelationshipRequest(BaseModel):
    source: str
    target: str
    relationship: str = "ASSOCIATED_WITH"
    weight: int = 1
