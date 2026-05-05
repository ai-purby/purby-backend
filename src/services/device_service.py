from src.utils.pairing_code import generate_pairing_code


# 페어링 코드 발급
def issue_pairing_code():
    code = generate_pairing_code()

    print(code)