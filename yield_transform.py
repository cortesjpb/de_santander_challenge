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


def main():
    tsv_file_name = "datos_data_engineer.tsv"
    csv_file_name = "datos_data_engineer.csv"

    lines = (line for line in io.open(tsv_file_name, mode="r", encoding="utf-16-le"))
    lines_values = (line.rstrip().split('\t') for line in lines)

    header = next(lines_values)
    formatted_header = '|'.join(header).encode("utf-8")

    csv_file = open(csv_file_name, "wb")

    csv_file.write(formatted_header)
    csv_file.write('\n')

    row = []
    for line_values  in lines_values:
        index = 0
        for value in line_values:

            if (value == '') and (index == 0):
                continue

            row_length = len(row)

            if row_length == 5:
                final_row = '|'.join(row).encode("utf-8")
                print final_row
                csv_file.write(final_row)
                csv_file.write('\n')
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
        print final_row
        csv_file.write(final_row)
        csv_file.write('\n')
        row = []


if __name__ == "__main__":

    main()