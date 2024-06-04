import os
import shutil
import time

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

balance = 0
limit = 500
extract = ""
withdrawals_made = 0
WITHDRAWAL_LIMIT = 3
MESSAGE_TIME = 5
TERMINAL_WIDTH = shutil.get_terminal_size()[0]


while True:
    os.system("clear") if os.name == "posix" else os.system("cls")
    print(" MENU DE OPERAÇÕES ".center(TERMINAL_WIDTH, "#"))
    option = input(menu).lower()

    match option:
        case "d":
            os.system("clear") if os.name == "posix" else os.system("cls")
            print(
                " Operação de Depósito Bancário ".center(TERMINAL_WIDTH, "#")
            )

            value = float(input("\nEntre com o valor a ser depositado: "))

            if value <= 0:
                print(
                    "\nOperação falhou! "
                    "O valor informado deve ser positivo e diferente de zero."
                )
                time.sleep(MESSAGE_TIME)
                continue

            balance += value
            extract += f"Depósito: R$ {value:.2f}\n"

            print("\nOperação realizada com sucesso!!!")
            time.sleep(MESSAGE_TIME)
        case "s":
            os.system("clear") if os.name == "posix" else os.system("cls")
            print(" Operação de Saque Bancário ".center(TERMINAL_WIDTH, "#",))

            value = float(input("\nInforme o valor do saque: "))

            if value <= 0:
                print(
                    "\nOperação falhou! "
                    "O valor informado deve ser positivo e diferente de zero."
                )
                time.sleep(MESSAGE_TIME)
                continue

            if value > balance:
                print(
                    "\nOperação falhou! "
                    "Você não tem saldo suficiente para realizar este saque. "
                    f"Saldo atual: {balance:.2f}."
                )
                time.sleep(MESSAGE_TIME)
                continue

            if value > limit:
                print(
                    "\nOperação falhou! "
                    "O valor do saque excede o limite. "
                    f"Limite de operação: R$ {limit:.2f}."
                )
                time.sleep(MESSAGE_TIME)
                continue

            if withdrawals_made >= WITHDRAWAL_LIMIT:
                print(
                    "\nOperação falhou! "
                    "Número máximo de saques atingido. "
                    f"Limite de saques: {WITHDRAWAL_LIMIT}."
                )
                time.sleep(MESSAGE_TIME)
                continue

            balance -= value
            extract += f"Saque: R$ {value:.2f}\n"
            withdrawals_made += 1

            print("\nOperação realizada com sucesso!!!")
            time.sleep(MESSAGE_TIME)
        case "e":
            os.system("clear") if os.name == "posix" else os.system("cls")
            print(" Extrato Bancário ".center(TERMINAL_WIDTH, "#",))

            if not extract:
                print("Não foram realizadas movimentações.")
            else:
                print(extract)

            print("-"*TERMINAL_WIDTH)
            print(f"Saldo: R$ {balance:.2f}.")

            print("#"*TERMINAL_WIDTH)
            input("\nPressione ENTER para retornar ao menu de operações.")
        case "q":
            response = None

            while response is None:
                os.system("clear") if os.name == "posix" else os.system("cls")
                print(
                    " Sair do Sistema Bancário ".center(TERMINAL_WIDTH, "#",)
                )

                response = input(
                    "\nDeseja realmente finalizar as operações? "
                    "[s-sim/N-não] => "
                ).lower()

                match response:
                    case "s":
                        break
                    case "n":
                        break
                    case "":
                        break
                    case _:
                        print(
                            "\nOpção inválida!!! "
                            "Selecione apenas opções válidas."
                        )
                        time.sleep(MESSAGE_TIME)
                        response = None

            if response == "s":
                print("\nAguardamos seu retorno! Até a próxima!")
                time.sleep(MESSAGE_TIME)
                os.system("clear") if os.name == "posix" else os.system("cls")
                break
        case _:
            print(
                "Operação inválida!!! "
                "Selecione apenas operações válidas no menu de opções."
            )
            time.sleep(MESSAGE_TIME)
