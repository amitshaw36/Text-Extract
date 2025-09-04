Invoice OCR API

An API service built with FastAPI that extracts text and key fields (Invoice Number, Date, Total Amount) from invoices using OCR (EasyOCR + Tesseract).

---

🚀 Features
- Upload an invoice image and extract text automatically
- Detects key invoice fields:
  - Invoice Number
  - Date
  - Total Amount
- Uses **EasyOCR** for text recognition with fallback to **Tesseract**
- JSON API response with structured results
- Built with **FastAPI** for high performance

---

⚙️ Tech Stack
- Python
- FastAPI – API framework
- EasyOCR – Primary OCR engine
- Tesseract (pytesseract) – Fallback OCR engine
- Pillow (PIL) – Image preprocessing
- Pydantic – Data models for API responses

---
