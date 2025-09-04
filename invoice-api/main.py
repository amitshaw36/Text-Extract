from fastapi import FastAPI, UploadFile, File
from schemas import InvoiceResponse
from ocr_engine import extract_text
from field_extractor import extract_invoice_number, extract_date, extract_total_amount
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/extract", response_model=InvoiceResponse)
async def extract_invoice_fields(file: UploadFile = File(...)):
    image_bytes = await file.read()
    texts = extract_text(image_bytes)
    logging.info(f"OCR TEXTS: {texts}")

    invoice_number = extract_invoice_number(texts)
    date = extract_date(texts)
    total_amount = extract_total_amount(texts)

    logging.info(f"Extracted: invoice_number={invoice_number}, date={date}, total_amount={total_amount}")

    return InvoiceResponse(
        texts=texts,
        invoice_number=invoice_number,
        date=date,
        total_amount=total_amount
    )