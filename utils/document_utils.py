def is_valid_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    def calculate_digit(cpf, digit):
        if digit == 9:
            factor = 10
        else:
            factor = 11
        total = sum(int(cpf[i]) * (factor - i) for i in range(digit))
        remainder = total % 11
        calculated_digit = 0 if remainder < 2 else 11 - remainder
        return calculated_digit

    for digit in [9, 10]:
        if calculate_digit(cpf, digit) != int(cpf[digit]):
            return False
    return True