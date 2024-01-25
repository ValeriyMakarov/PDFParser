from pdfminer.high_level import extract_text, extract_pages
import re
import fitz
from pyzbar.pyzbar import decode
from PIL import Image


def read_barcodes(pdf_path: str) -> list[dict]:
    """Reads the first page of PDF document and returns the list of
    dictionaries with info about decoded barcodes on the page"""

    with fitz.open(pdf_path) as pdf_file:
        page = pdf_file.load_page(0)
        pixel_map = page.get_pixmap()
    page_image = Image.frombytes(
        "RGB", [pixel_map.width, pixel_map.height], pixel_map.samples
    )
    decoded = sorted(
        decode(page_image),
        key=lambda x: (x.rect.left, x.rect.top)
    )

    return [
        {
            'barcode_type': barcode.type,
            'barcode_data': barcode.data.decode('utf-8')
        }
        for barcode in decoded
    ]


def get_value_regexp(regexp: str, from_str: str):
    matches = re.search(regexp, from_str, re.DOTALL)
    return matches.group(1) if len(matches.groups()) else None


def read_inner_data_from_pdf(pdf: str) -> dict:
    """Reads data from PDF file"""

    text = extract_text(pdf)
    barcodes = read_barcodes(pdf)

    data_dict = {
        'LABEL': get_value_regexp(r'(^(\w+ *)*).*', text),
        'BARCODE': barcodes[0],
        'PN': get_value_regexp(r'PN: (\w+).*DESCRIPTION:', text),
        'DESCRIPTION': get_value_regexp(r'DESCRIPTION: (\w+).*LOCATION:', text),
        'LOCATION': get_value_regexp(r'LOCATION: (\d+).*RECEIVER#:', text),
        'RECEIVER#': get_value_regexp(r'RECEIVER#: (\d+).*EXP DATE:', text),
        'EXP DATE': get_value_regexp(r'EXP DATE: ((\d+\.?){3}).*CERT SOURCE:', text),
        'CERT SOURCE': get_value_regexp(r'CERT SOURCE: (\S+).*SN:', text),
        'SN': get_value_regexp(r'SN: (\d+).*CONDITION:', text),
        'CONDITION': get_value_regexp(r'CONDITION: (\w+).*UOM:', text),
        'UOM': get_value_regexp(r'UOM: (\w+).*PO:', text),
        'PO': get_value_regexp(r'PO: (\w+).*REC.DATE:', text),
        'REC.DATE': get_value_regexp(r'REC.DATE: ((\d+\.?){3}).*MFG:', text),
        'MFG': get_value_regexp(r'MFG: (\w+).*BATCH# :', text),
        'BATCH#': get_value_regexp(r'BATCH# : (\d+).*REMARK:', text),
        'REMARK': get_value_regexp(r'REMARK:(\S+)*.*TAGGED BY:', text),
        'TARGET BY': {
            'BARCODE': barcodes[1],
            'Qty': get_value_regexp(r'Qty: (\S+).*DOM:', text),
        },
        'DOM': get_value_regexp(r'DOM: ((\d+\.?){3}).*LOT# :', text),
        'LOT#': get_value_regexp(r'LOT# : (\w+).*NOTES:', text),
        'NOTES': get_value_regexp(r'NOTES:\s+((\S+ *)*).*', text),
    }

    return data_dict


if __name__ == "__main__":
    print(read_inner_data_from_pdf(r'task_data\test_task.pdf'))

