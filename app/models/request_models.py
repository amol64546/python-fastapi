from pydantic import BaseModel


class Ontology(BaseModel):
    ontologyUrl: str
    file_type: str
    ontology_name: str
    tenant_id: str
