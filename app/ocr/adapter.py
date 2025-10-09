from typing import Protocol
class OcrEngine(Protocol):
    def image_to_text(self, path: str) -> str: ...
class DummyOcr:
    def image_to_text(self, path: str) -> str:
        return "(OCR disabled)"
try:
    import pytesseract  # type: ignore
    from PIL import Image  # type: ignore
    class TesseractOcr:
        def image_to_text(self, path: str) -> str:
            return pytesseract.image_to_string(Image.open(path))
    current_engine: OcrEngine = TesseractOcr()
except Exception:
    current_engine: OcrEngine = DummyOcr()
