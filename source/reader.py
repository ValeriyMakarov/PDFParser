"""
Задание:

Разработать метод, на вход которого подается PDF файл
(сам файл предоставляется во вложении). Нужно прочитать всю возможную
информацию из файла и на выходе вернуть в виде словаря.
"""
from pdfminer.high_level import extract_text
import re


def get_value_regexp(regexp: str, from_str: str):
    matches = re.search(regexp, from_str, re.DOTALL)
    return matches.group(1) if len(matches.groups()) else None


def read_inner_data_from_pdf(pdf: str) -> dict:
    """Reads data from PDF file"""
    text = extract_text(pdf)
    data_dict = {
        'LABEL': get_value_regexp(r'(^(\w+ *)*).*', text),
        'BARCODE': None,
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
            'BARCODE': None,
            'Qty': get_value_regexp(r'Qty: (\S+).*DOM:', text),
        },
        'DOM': get_value_regexp(r'DOM: ((\d+\.?){3}).*LOT# :', text),
        'LOT#': get_value_regexp(r'LOT# : (\w+).*NOTES:', text),
        'NOTES': get_value_regexp(r'NOTES:\s+((\S+ *)*).*', text),

    }
    # res = re.search(r'EXP DATE: ((\d+\.?){3}).*CERT SOURCE: '
    #                 r'(\w+).*SN: (\w+).*CONDITION: (\w+).*UOM: (\w+).*PO: (\w+).*REC.DATE: '
    #                 r'((\d+\.?){3}).*MFG: (\w+).*BATCH# : (\w+).*REMARK:.*TAGGED BY:.*Qty: '
    #                 r'(\w+).*DOM: ((\d+\.?){3}).*LOT# : (\w+).*NOTES:.*(\w+).*', text, re.DOTALL)
    # print(res)

    return data_dict


if __name__ == "__main__":
    print(read_inner_data_from_pdf(r'task_data\test_task.pdf'))

