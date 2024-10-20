def get_ean13(cod):
    if len(cod) < 12:
        return None
    if len(cod) > 12:
        cod = cod[:12]
    cod = cod[::-1]
    sum = 0
    for i in range(0, len(cod)):
        if i % 2 == 0:
            sum += int(cod[i])
        else:
            sum += int(cod[i]) * 3
    check_digit = 10 - (sum % 10)
    if check_digit == 10:
        check_digit = 0
    return cod[::-1] + str(check_digit)


while(True):
    cod_id = input("Ingrese identificador (7 dígitos): ")
    if (len(cod_id) != 7):
        print("Error: El identificador debe tener 7 dígitos")
        continue
    try:
        int(cod_id)
    except:
        print("Error: El identificador debe ser un número")
        continue
    break

while(True):
    cod_weight = input("Ingrese el peso (5 dígitos): ")
    if (len(cod_weight) > 5):
        print("Error: El peso debe tener menos de 5 dígitos")
        continue
    elif (len(cod_weight) < 5):
        cod_weight = cod_weight.zfill(5)
    try:
        int(cod_weight)
    except:
        print("Error: El peso debe ser un número")
        continue
    break

ean13 = get_ean13(cod_id + cod_weight)
print(f"El código EAN-13 es: {ean13}")
input("Presione cualquier tecla para continuar...")