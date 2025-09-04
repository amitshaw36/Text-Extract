import easyocr
import pytesseract
from PIL import Image
import io

reader = easyocr.Reader(['en'])

def extract_text(image_bytes: bytes) -> list[str]:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        results = reader.readtext(image)
        texts = [text for _, text, _ in results]
    except Exception as e:
        print(f"EasyOCR failed: {e}")
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            texts = text.splitlines()
        except Exception as e2:
            print(f"Tesseract also failed: {e2}")
            texts = []

    # Filter out empty or junk lines
    return [t.strip() for t in texts if len(t.strip()) > 3]