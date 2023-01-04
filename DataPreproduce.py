from PIL import Image
import cv2
import fitz
import numpy as np

# convert scanned pdf file to pictures
def preproduce(book_path):
    pages = []
    with fitz.open(f'./input/{book_path}') as pdf:
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            pm = page.get_pixmap(matrix=fitz.Matrix(
                2000/pm.height, 2000/pm.height), alpha=False)
            bookpage = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
            bookpage = cv2.cvtColor(np.array(bookpage), cv2.COLOR_RGB2BGR)
            pages.append(bookpage)
    return pages

    