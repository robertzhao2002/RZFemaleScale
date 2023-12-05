import csv
import secrets

raw_data = []
data = [['BAD', 'CUTE', 'HOT']]

FILE = open("CHICKS.csv")
READER = csv.reader(FILE, delimiter=',')

reader_list = list(READER)[1:]
NUM_LINES= len(reader_list)

def csv_to_plot(num_rows):
    rows_to_display = list(range(NUM_LINES))
    secrets.SystemRandom().shuffle(rows_to_display)
    rows_to_display = rows_to_display[0:num_rows]

    for i in rows_to_display:
        raw_data.append(reader_list[i])
    for j in raw_data:
        to_add = (j[0], [[float(j[1]), float(j[2]), float(j[3])]])
        data.append(to_add)
    
    return data
