from typing import List
from datetime import datetime
import re
from dateutil import parser

from datetime import datetime
from typing import List, Dict

def extract_invoice_data(texts: List[str]) -> Dict[str, str]:
    invoice_number = None
    date_str = "Not found"
    total_amount = None

    # OCR correction mapping
    ocr_map = {
        'k': '1',
        'K': '1',
        'o': '0',
        'O': '0',
        'z': '2',
        'Z': '2',
        'e': '2',
        'E': '2',
        'l': '1',
        'L': '1',
        's': '5',
        'S': '5'
    }

    def fix_ocr(text: str) -> str:
        return ''.join(ocr_map.get(c, c) for c in text)

    for i, line in enumerate(texts):
        clean_line = line.strip()

        # Invoice number
        if invoice_number is None and "invoice no" in clean_line.lower():
            if i + 1 < len(texts):
                invoice_number = texts[i + 1].strip()

        # D












def extract_invoice_number(texts: List[str]) -> str:
    for i, line in enumerate(texts):
        if "invoice" in line.lower() and "no" in line.lower():
            # Look at next line for number
            if i + 1 < len(texts):
                candidate = texts[i + 1].strip()
                if candidate.isdigit():
                    return candidate
        # Inline match
        match = re.search(r"(?:invoice\s*no\.?\s*[:\-]?\s*)(\d{3,})", line, re.IGNORECASE)
        if match:
            return match.group(1)
    return "Not found"

def extract_date(texts: List[str]) -> str:
    for line in texts:
        if "dated" in line.lower():
            raw = (
                line.lower()
                .replace("dated", "")
                .replace(":", "")
                .replace("_", "")
                .replace("k", "8")
                .replace("z", "2")
                .replace("e", "2")
                .replace("o", "0")
                .replace(" ", "")
            )
            digits = ''.join(c if c.isdigit() or c in "/-." else "" for c in raw)
            for fmt in ["%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%y", "%d/%m/%y", "%d-%m-%y"]:
                try:
                    parsed = datetime.strptime(digits, fmt)
                    return parsed.strftime("%d/%m/%Y")  # Indian format
                except ValueError:
                    continue
    return "Not found"

def extract_total_amount(texts: List[str]) -> str:
    for i, line in enumerate(texts):
        if "total" in line.lower():
            # Look ahead for numeric value
            for j in range(i + 1, min(i + 5, len(texts))):
                candidate = texts[j].replace(" ", "").replace(",", "")
                if candidate.replace(".", "").isdigit():
                    return candidate
        # Inline match
        match = re.search(r"total\s*[:\-]?\s*\₹?\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", line, re.IGNORECASE)
        if match:
            return match.group(1)
    # Fallback: detect spaced digits like "1 8 88"
    for line in texts:
        parts = line.strip().split()
        if len(parts) >= 2 and all(p.isdigit() for p in parts):
            combined = ''.join(parts)
            if combined.isdigit():
                return combined
    return "Not found"

def extract_fields(texts: List[str]) -> dict:
    return {
        "invoice_number": extract_invoice_number(texts),
        "date": extract_date(texts),
        "total_amount": extract_total_amount(texts)
    }