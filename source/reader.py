import fitz
from pyzbar.pyzbar import decode
from PIL import Image


def read_barcodes(page: fitz.Page) -> list[dict]:
    """
    Reads the first page of PDF document and returns the list of
    dictionaries with info about decoded barcodes on the page
    :param page: fitz.Page
    :return: list[dict]
    """

    pixel_map = page.get_pixmap()
    page_image = Image.frombytes(
        "RGB", [pixel_map.width, pixel_map.height], pixel_map.samples
    )
    decoded = sorted(
        decode(page_image),
        key=lambda x: (x.rect.left, x.rect.top)
    )

    decoded_list = [
        {
            'barcode_type': barcode.type,
            'barcode_data': barcode.data.decode('utf-8')
        }
        for barcode in decoded
    ]
    return decoded_list


def read_data_from_page(page: fitz.Page) -> dict:
    """
    Reads all data from page
    :param page: fitz.Page
    :return: dict
    """

    text_data_list = [i for i in page.get_text().split('\n') if i.strip()]
    barcodes = read_barcodes(page)

    page_data_dict = {
        'LABEL': text_data_list[0],
        'BARCODE': barcodes[0] if len(barcodes) == 2 else None,
        'TAGGED BY': {
            'BARCODE': barcodes[1] if len(barcodes) == 2 else None,
            'Qty': None
        },
        'NOTES': text_data_list[-1]
    }
    for item in text_data_list[1:-1]:
        if 'TAGGED BY' in item or 'NOTES' in item:
            continue
        elif 'Qty' in item:
            page_data_dict['TAGGED BY']['Qty'] = item.split(':')[1].strip()
        else:
            items = item.split(':')
            page_data_dict[items[0]] = items[1] if len(items) == 2 else None

    return page_data_dict


def read_data_from_pdf(pdf_path: str) -> dict[dict]:
    """
    Reads all data from PDF file by page
    :param pdf_path: str
    :return: dict[dict]
    """

    pdf_data_dict = {}

    with fitz.open(pdf_path) as pdf_file:
        for page_number in range(pdf_file.page_count):
            page = pdf_file.load_page(page_number)
            pdf_data_dict[page_number] = read_data_from_page(page)

    return pdf_data_dict


if __name__ == "__main__":
    print(read_data_from_pdf(r'task_data\test_task.pdf'))

