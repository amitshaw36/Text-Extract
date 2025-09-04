from pydantic import BaseModel
from typing import List

class InvoiceResponse(BaseModel):
    texts: List[str]
    invoice_number: str
    date: str
    total_amount: str