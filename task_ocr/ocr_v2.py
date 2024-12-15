import io
import requests
import json
import base64
from fpdf import FPDF
from pathlib import Path
from typing import Optional
from PIL import Image
import os
from pdf2image import convert_from_path
import pytesseract

# Funkcja do przetwarzania plików PDF
def convert_pdf_to_images(pdf_path: str) -> list:
    poppler_path = r'C:\Program Files (x86)\Release-24.08.0-0\poppler-24.08.0\Library\bin'  # Zamień na swoją ścieżkę do Poppler
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    return images

# Funkcja OCR przy użyciu OCRWebService
def ocr_ocrwebservice(image: Image) -> Optional[str]:
    LicenseCode = '4088F5E4-9D4B-415D-B2E5-D3B1C332A654'  # Podaj swój kod licencyjny
    UserName = 'OLEGR'  # Podaj swoją nazwę użytkownika

    # URL API OCRWebService
    RequestUrl = "http://www.ocrwebservice.com/restservices/processDocument?gettext=true"

    # Konwertuj obraz na tryb RGB, jeśli jest w trybie RGBA
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Zapisz obraz do bufora w formacie JPEG
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")

    # Pobierz dane obrazu
    image_data = buffered.getvalue()

    # Wysłanie żądania do OCRWebService
    response = requests.post(RequestUrl, data=image_data, auth=(UserName, LicenseCode))

    if response.status_code == 401:
        print("Nieautoryzowane żądanie. Sprawdź poprawność nazwy użytkownika i kodu licencyjnego.")
        return None

    if response.status_code == 200:
        result_json = response.json()
        if "ErrorMessage" in result_json and result_json["ErrorMessage"]:
            print("Błąd OCR:", result_json["ErrorMessage"])
            return None
        else:
            # Pobierz przetworzony tekst
            return result_json["OCRText"][0][0]
    else:
        print(f"Błąd podczas przetwarzania: {response.status_code} {response.text}")
        return None


# Funkcja OCR przy użyciu Google Cloud Vision API
def ocr_google_vision(image: Image) -> Optional[str]:
    api_key = "AIzaSyD2Kto_n6hpl-EffWs2n3IC6uMPpdi90mY"  # Wklej swój klucz API Google Vision tutaj
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"

    # Konwertujemy obraz do formatu base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_content = base64.b64encode(buffered.getvalue()).decode("utf-8")

    request_data = {
        "requests": [
            {
                "image": {"content": image_content},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }

    response = requests.post(url, json=request_data)
    if response.status_code == 200:
        try:
            text = response.json()["responses"][0]["textAnnotations"][0]["description"]
            return text
        except (IndexError, KeyError):
            print("Brak tekstu na obrazie")
    else:
        print("Błąd w odpowiedzi:", response.status_code, response.text)
    return None


# Funkcja OCR przy użyciu Microsoft Azure Computer Vision API
def ocr_azure(image: Image) -> Optional[str]:
    api_key = "7tLWhbn4whH1dRNXJssU3C91xriPTudgt8HodMzADDpdXbdCozZUJQQJ99AKACfhMk5XJ3w3AAAFACOGSKSh"  # Wpisz klucz API dla Microsoft Azure tutaj
    endpoint = "https://ocr-zadanie1.cognitiveservices.azure.com/"  # Wpisz swój endpoint dla Azure tutaj
    url = f"{endpoint}/vision/v3.2/read/analyze"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/octet-stream",
    }

    # Konwertowanie obrazu na dane binarne
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_data = buffered.getvalue()

    response = requests.post(url, headers=headers, data=image_data)
    if response.status_code == 202:
        operation_location = response.headers["Operation-Location"]
        print("Przetwarzanie dokumentu. Proszę czekać...")

        # Czekamy na zakończenie przetwarzania
        while True:
            result_response = requests.get(operation_location, headers={"Ocp-Apim-Subscription-Key": api_key})
            result_json = result_response.json()

            if result_json["status"] == "succeeded":
                # Zbieranie wyników tekstowych w jeden ciąg
                lines = [
                    line["text"]
                    for page in result_json["analyzeResult"]["readResults"]
                    for line in page["lines"]
                ]
                return "\n".join(lines)
            elif result_json["status"] == "failed":
                print("OCR nie powiodło się.")
                return None
    else:
        print("Błąd w odpowiedzi:", response.status_code, response.text)
        return None


# Funkcja OCR przy użyciu Tesseract
def ocr_tesseract(image: Image) -> Optional[str]:
    try:
        # Zakłada domyślny język angielski, można zmienić na np. 'pol' lub 'staroslowianski'
        text = pytesseract.image_to_string(image, lang='eng+pol+rus+bel+ukr')
        return text
    except Exception as e:
        print("Błąd Tesseract OCR:", e)
        return None


# Funkcja do zapisywania wyników w wybranym formacie
def save_result(result: str, filename: str, format_type: str):
    if format_type == "txt":
        with open(filename + ".txt", "w", encoding="utf-8") as f:
            f.write(result)
    elif format_type == "json":
        with open(filename + ".json", "w", encoding="utf-8") as f:
            json.dump({"result": result}, f, ensure_ascii=False, indent=4)
    elif format_type == "pdf":
        pdf = FPDF()
        pdf.add_page()
        # Podaj pełną ścieżkę do pliku DejaVuSans.ttf
        font_path = Path('DejaVuSans.ttf').as_posix()  # Zmienna zawierająca ścieżkę
        pdf.add_font('DejaVu', '', font_path, uni=True)  # Dodajemy czcionkę obsługującą Unicode
        pdf.set_font('DejaVu', size=12)
        pdf.multi_cell(0, 10, result)
        pdf.output(filename + ".pdf")
    else:
        print("Nieprawidłowy format zapisu.")


# Główna funkcja, w której użytkownik wybiera system OCR
def main():
    print("Wybierz system OCR:")
    print("1: Google Vision")
    print("2: Microsoft Azure Computer Vision")
    print("3: Tesseract")
    print("4: OCRWebService")

    choice = input("Podaj numer wyboru: ")
    file_path = input("Podaj ścieżkę do pliku z obrazem lub PDF: ")

    # Sprawdzamy, czy użytkownik podał plik PDF czy obraz
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension in [".pdf"]:
        images = convert_pdf_to_images(file_path)
    elif file_extension in [".jpg", ".jpeg", ".png", ".bmp"]:
        images = [Image.open(file_path)]
    else:
        print("Nieobsługiwany format pliku.")
        return

    if choice == "1":
        results = [ocr_google_vision(image) for image in images]
    elif choice == "2":
        results = [ocr_azure(image) for image in images]
    elif choice == "3":
        results = [ocr_tesseract(image) for image in images]
    elif choice == "4":
        results = [ocr_ocrwebservice(image) for image in images]
    else:
        print("Nieprawidłowy wybór.")
        return

    # Łączenie wyników z wielu stron
    result_text = "\n".join(filter(None, results))

    if result_text:
        print("\nWynik OCR:\n", result_text)

        # Wybór formatu zapisu
        format_choice = input("Wybierz format zapisu (txt, json, pdf): ").lower()
        filename = input("Podaj nazwę pliku (bez rozszerzenia): ")
        save_result(result_text, filename, format_choice)
        print(f"Wynik zapisano w formacie {format_choice} jako '{filename}.{format_choice}'.")
    else:
        print("Nie udało się odczytać tekstu.")


# Uruchomienie głównej funkcji
if __name__ == "__main__":
    main()
