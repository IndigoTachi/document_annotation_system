import io
import requests
import base64
from typing import Optional
from PIL import Image
import pytesseract


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
        # print("Nieautoryzowane żądanie. Sprawdź poprawność nazwy użytkownika i kodu licencyjnego.")
        return None

    if response.status_code == 200:
        result_json = response.json()
        if "ErrorMessage" in result_json and result_json["ErrorMessage"]:
            # print("Błąd OCR:", result_json["ErrorMessage"])
            return None
        else:
            # Pobierz przetworzony tekst
            return result_json["OCRText"][0][0]
    else:
        # print(f"Błąd podczas przetwarzania: {response.status_code} {response.text}")
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
            # print("Brak tekstu na obrazie")
            return None
    else:
        # print("Błąd w odpowiedzi:", response.status_code, response.text)
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
        # print("Przetwarzanie dokumentu. Proszę czekać...")

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
                # print("OCR nie powiodło się.")
                return None
    else:
        # print("Błąd w odpowiedzi:", response.status_code, response.text)
        return None


# Funkcja OCR przy użyciu Tesseract
def ocr_tesseract(image: Image) -> Optional[str]:
    try:
        # Zakłada domyślny język angielski, można zmienić na np. 'pol' lub 'staroslowianski'
        text = pytesseract.image_to_string(image, lang='eng+pol+rus+bel+ukr')
        return text
    except Exception as e:
        # print("Błąd Tesseract OCR:", e)
        return None
