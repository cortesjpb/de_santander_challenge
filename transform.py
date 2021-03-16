import re

# Intentamos abrir el archivo tsv en modo lectura
try:
    tsv_file = open("datos_data_engineer.tsv", "rb")
except IOError:
    print "El archivo que intenta leer no existe."

# Abrimos el CSV en el que vamos a escribir
csv_file = open("datos_data_engineer.csv", "wb")

data = tsv_file.read()
decoded_data = data.decode("utf-16-le")
data_formated = re.sub(r" *", "", decoded_data)
data_formated2 = re.sub(r"\t", "|", data_formated)
data_formated3 = re.sub(r"\n\|", "|", data_formated2)
first_part = ""
for line in data_formated3.split('\n'):
    delimiter_count = line.count('|')
    if delimiter_count < 4:
        if first_part == "":
            first_part = line
        else:
            complete_line = ' '.join([first_part, line])
            print complete_line
            first_part = ""
            csv_file.write(complete_line.encode("utf-8"))
            csv_file.write('\n'.encode("utf-8"))
    else:
        csv_file.write(line.encode("utf-8"))
        csv_file.write('\n'.encode("utf-8"))


tsv_file.close()
csv_file.close()
