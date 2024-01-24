"""
Задание:

Разработать метод, на вход которого подается PDF файл
(сам файл предоставляется во вложении). Нужно прочитать всю возможную
информацию из файла и на выходе вернуть в виде словаря.
"""


def read_inner_data_from_pdf(pdf: str) -> dict:
    """Reads data from PDF file"""
    data_dict = {}

    ...

    return data_dict


if __name__ == "__main__":
    print(read_inner_data_from_pdf(r'../task_data/test_task.pdf'))

