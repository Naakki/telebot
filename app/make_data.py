from openpyxl import load_workbook
import collections

wb = load_workbook('..\Combo.xlsx')
# Страховка | Телефон | Combo sheets
telephones = wb['Телефон']
insurance = wb['Страховка']
sim = wb['Combo']

def parse_excel_file(sheet, start='A1', end='A1') -> list:
    '''
    Функция парсит данные таблицы и возвращает их в списке
    Входные данные: 
    sheet - Лист таблицы
    start - Начальные координаты ячейки
    end - Последние координаты ячейки (Если не указана строка, до последней)
    '''
    if len(end) < 2:
        # Получаем последний элемент через коллекцию deque()
        # Вывод: >> (354, <Cell 'Телефон'.C355>)
        [last] = collections.deque(enumerate(sheet['C']), maxlen=1)

        end = str(end) + str(last[0] + 1)

    phones = list()

    for row in sheet[start:end]:
        phone_list = list()

        for cell in row:
            if cell.value == 'Apple' or \
                cell.value == 'Huawei':
                break
            elif cell.value == None:
                pass
            elif cell.value:
                phone_list.append(cell.value)
        
        if (phone_list != []) and (phone_list not in phones): 
            phones.append(phone_list)
    
    return phones

telephones = parse_excel_file(telephones, end='F')
insurance = parse_excel_file(insurance, end='F')
sim = parse_excel_file(sim, end='F')