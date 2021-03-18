import io
import re


def format_column_value(row_length, value):
    """
    Devuelve cada valor de una columna formateado
    eliminando los caracteres que no deberian estar segun el campo
    """
    # Si el campo es un ID o un account_number deben ser solo numeros
    if row_length in [0,3]:
        return re.sub('[^0-9]', '', value)
    # Si es un first_name o last_name deberian ser solo letras
    elif row_length in [1,2]:
        return re.sub('[^\w]', '', value)
    else:
        return value


def process_header(header):
    """
    Devuelve una sola linea formateada
    En este caso lo usamos para formatear el header
    """
    return '|'.join(header).encode("utf-8")


def get_tsv_data(tsv_file_name):
    """
    Devuelve un generador con las lineas del archivo TSV sin formatear
    """
    lines = (line for line in io.open(tsv_file_name, mode="r", encoding="utf-16-le"))
    lines_values = (line.rstrip().split('\t') for line in lines)
    return lines_values


def process_data(lines_values):
    """
    Devuelve un generador con cada fila procesada
    """
    row = []
    for line_values  in lines_values:
        index = 0
        for value in line_values:

            if (value == '') and (index == 0):
                continue

            row_length = len(row)

            # Si completamos una row la devolvemos
            if row_length == 5:
                final_row = '|'.join(row).encode("utf-8")
                yield final_row
                row = []
            
            '''Cuando la data tiene un salto de linea tenemos un problema
            Si la palabra en una nueva linea contiene solo letras 
            Y recientemente se cargo el first o last name
            Agregamos el nuevo valor al valor recien cargado
            Sino simplemente agregamos el valor nuevo a la row'''
            if (1 < row_length < 4) and (index == 0) and (not value.isnumeric()):
                formatted_value = format_column_value(row_length-1, value)
                row[-1] += " " + formatted_value
            else:
                formatted_value = format_column_value(row_length, value)
                row.append(formatted_value)
            index += 1

    # Aqui procesamos la ultima linea del archivo
    row_length = len(row)
    if row_length == 5:
        final_row = '|'.join(row).encode("utf-8")
        yield final_row


def write_data(csv_file, formatted_header, formatted_data):
    """
    Escribimos el header y la data formateada a nuestro CSV
    """
    csv_file.write(formatted_header)
    csv_file.write('\n')
    for row in formatted_data:
        csv_file.write(row)
        csv_file.write('\n')


def main():

    # Seteamos los nombres de nuestros archivos
    tsv_file_name = "datos_data_engineer.tsv"
    csv_file_name = "datos_data_engineer.csv"

    # Creamos el generador para nuestros datos
    unformatted_data = get_tsv_data(tsv_file_name)    

    # Formateamos la primera linea de nuestros datos, el header
    formatted_header = process_header(next(unformatted_data))

    # Creamos nuestro archivo de salida
    csv_file = open(csv_file_name, "wb")

    # Creamos un generador que formatea los datos
    formatted_data = process_data(unformatted_data)

    # Escribimos nuestros datos formateados en el CSV final
    write_data(csv_file, formatted_header, formatted_data)


if __name__ == "__main__":
    main()