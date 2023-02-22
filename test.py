from PIL import Image
from pytesseract import pytesseract

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r'karuta_drop.jpg'

img = Image.open(image_path)
pytesseract.tesseract_cmd = path_to_tesseract

cards = []

card1 = img.crop((50, 65, 230, 105))
cards.append(pytesseract.image_to_string(card1))

card2 = img.crop((320, 65, 510, 105))
cards.append(pytesseract.image_to_string(card2))

card3 = img.crop((600, 65, 780, 105))
cards.append(pytesseract.image_to_string(card3))
if (img.width > 840):
    card4 = img.crop((870, 65, 1050, 105))
    cards.append(pytesseract.image_to_string(card4))

for i in cards:
    print(i)
