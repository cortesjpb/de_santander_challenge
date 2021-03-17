import io
import re


def format_column_value(row_length, value):
    """
    Formatea los valores de cada columna excluyendo 
    caracteres que no tienen sentido segun el campo
    """
    if row_length in [0,3]:
        return re.sub('[^0-9]', '', value)
    elif row_length in [1,2]:
        return re.sub('[^\w]', '', value)
    else:
        return value


def process_header(header):
    return '|'.join(header).encode("utf-8")


def get_tsv_data(tsv_file_name):

    lines = (line for line in io.open(tsv_file_name, mode="r", encoding="utf-16-le"))
    lines_values = (line.rstrip().split('\t') for line in lines)
    return lines_values


def process_data(lines_values):

    row = []
    for line_values  in lines_values:
        index = 0
        for value in line_values:

            if (value == '') and (index == 0):
                continue

            row_length = len(row)

            if row_length == 5:
                final_row = '|'.join(row).encode("utf-8")
                yield final_row
                row = []
            
            if (1 < row_length < 4) and (index == 0) and (not value.isnumeric()):
                formatted_value = format_column_value(row_length-1, value)
                row[-1] += " " + formatted_value
            else:
                formatted_value = format_column_value(row_length, value)
                row.append(formatted_value)
            index += 1

    row_length = len(row)
    if row_length == 5:
        final_row = '|'.join(row).encode("utf-8")
        yield final_row

def write_data(csv_file, formatted_header, formatted_data):

    csv_file.write(formatted_header)
    csv_file.write('\n')
    for row in formatted_data:
        csv_file.write(row)
        csv_file.write('\n')


def main():

    tsv_file_name = "datos_data_engineer.tsv"
    csv_file_name = "datos_data_engineer.csv"

    unformatted_data = get_tsv_data(tsv_file_name)    

    formatted_header = process_header(next(unformatted_data))

    csv_file = open(csv_file_name, "wb")

    formatted_data = process_data(unformatted_data)

    write_data(csv_file, formatted_header, formatted_data)


if __name__ == "__main__":

    main()