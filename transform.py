import re

def append_to_line(formatted_data, complete_line, column_value, value_index):
    """
    Se formatea un valor de una columna y se agrega a la fila que se esta procesando
    para ser escrita en el CSV.
    En caso de estar completa la fila (tener 5 campos) escribe en el archivo CSV
    """

    index = len(complete_line)
    if (index == 5):
        append_line(formatted_data, complete_line)
        complete_line = []

    if (value_index == 0) and (0 < index < 4):
        formated_value = format_column_value(index-1, column_value)
        complete_line[-1] += " " + formated_value
    else:
        formated_value = format_column_value(index, column_value)
        complete_line.append(formated_value)

    return complete_line


def format_column_value(index, value):
    """
    Formatea los valores de cada columna excluyendo 
    caracteres que no tienen sentido segun el campo
    """

    if index in [0,3]:
        return re.sub('[^0-9]', '', value)
    elif index in [1,2]:
        return re.sub('[^\w]', '', value)
    else:
        return value


def get_csv(file_name):
    return open(file_name, "wb")


def get_preformatted_data(file_name):
    """
    La funcion realizara el primer formateo general al archivo TSV
    Quitaremos los espacios, reemplazaremos las tabulaciones por un pipe
    y finalmente reemplazaremos las ocurrencias de salto de linea seguido de
    un pipe por un pipe unicamente, en el orden citado

    """
    try:
        tsv_file = open(file_name, "rb")
    except IOError:
        print "El archivo que intenta leer no existe."

    data = tsv_file.read()
    decoded_data = data.decode("utf-16-le")
    data_spaces_deleted = re.sub(r" *", "", decoded_data)
    data_tab_to_pipe = re.sub(r"\t", "|", data_spaces_deleted)
    data_newline_to_pipe = re.sub(r"\n\|", "|", data_tab_to_pipe)
    tsv_file.close()
    header, data = data_newline_to_pipe.split('\n')[0], data_newline_to_pipe.split('\n')[1:]
    return header, data


def process_values(data):

    formatted_data = []
    complete_line = []
    for line in data:
        for value_index, column_value in enumerate(line.split('|')):
            complete_line = append_to_line(formatted_data, complete_line, column_value, value_index)

    append_to_line(formatted_data, complete_line, "", 0)

    return formatted_data


def append_line(formatted_data, complete_line):
    """
    Agregamos la linea formateada a nuestros datos formateados
    """
    formatted_data.append('|'.join(complete_line).encode("utf-8"))
    return formatted_data


def write_lines(csv_file, formatted_data):
    """
    Escribimos en el archivo CSV
    """
    for line in formatted_data:
        csv_file.write(line)
        csv_file.write('\n'.encode("utf-8"))


def write_header(csv_file, header):
    csv_file.write(header.encode("utf-8"))
    csv_file.write('\n'.encode("utf-8"))


def main():

    # Formateamos y conseguimos el header y la data por separado
    header, data = get_preformatted_data("datos_data_engineer.tsv")

    # Creamos nuestro CSV y escribimos el header
    csv_file = get_csv("datos_data_engineer.csv")

    write_header(csv_file, header)

    # Procesamos y formateamos la data
    formatted_data = process_values(data)

    # Escribimos en nuestro CSV
    write_lines(csv_file, formatted_data)

    csv_file.close()

if __name__ == "__main__":

    main()
