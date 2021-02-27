import csv

def csv_writer(data, path):
    """
    Функция для записи данных в CSV
    """
    with open(path, "w", newline='') as csv_file:
        '''
        csv_file - объект с данными
        delimiter - разделитель
        '''
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)


data = [['num', 'freq', 'power', 'N', 'time'],
        ['1', '2000 (PRRmax)', '100', '1', '120'],
        ['2', '50 (PRRmin)', '100', '8', '120'],
        ['3', '2000 (PRRmax)', '0', '1', '15']]

path = "output.csv"
csv_writer(data, path)
