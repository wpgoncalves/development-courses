import os
import shutil
import time
from datetime import datetime
from string import digits
from textwrap import dedent as textwrap_dedent
from typing import Any, Callable

WITHDRAWAL_LIMIT = 3
TERMINAL_WIDTH = shutil.get_terminal_size()[0]


def clear_screen(func: Callable[..., Any]) -> Any:
    def wrapper(*args, **kwargs):
        os.system("clear") if os.name == "posix" else os.system("cls")
        return func(*args, **kwargs)
    return wrapper


def message(msg: str, display_time: int = 4):
    print(msg)
    time.sleep(display_time)


@clear_screen
def menu() -> str:
    menu_text = """
    \n
    [cu]\tCadastrar Usuário
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair
    \n
    => """

    print(" MENU DE OPERAÇÕES ".center(TERMINAL_WIDTH, "#"))
    return input(textwrap_dedent(menu_text)).lower()


@clear_screen
def withdraw(*, balance: float, extract: str, limit: float, withdrawals_made: int) -> tuple[float, str, int]:
    print(" Operação de Saque Bancário ".center(TERMINAL_WIDTH, "#",))

    try:
        value = float(input("\nInforme o valor do saque: "))

        if value <= 0:
            raise ValueError("O valor informado deve ser positivo e diferente de zero.")
        if value > balance:
            raise ValueError(f"Saldo suficiente para realizar este saque. Saldo atual: {balance:.2f}.")
        if value > limit:
            raise ValueError(f"O valor do saque excede o limite. Limite de operação: R$ {limit:.2f}.")
        if withdrawals_made >= WITHDRAWAL_LIMIT:
            raise ValueError(f"Número máximo de saques atingido. Limite de saques: {WITHDRAWAL_LIMIT}.")

        balance -= value
        extract += f"Saque: R$ {value:.2f}\n"
        withdrawals_made += 1

        message("\nOperação realizada com sucesso!!!")
    except ValueError as exc:
        for arg in exc.args:
            if "could not convert" in arg:
                exc = "O valor informado deve ser puramente numérico."

        message(
            "\nOperação falhou! "
            f"{exc}"
        )
    finally:
        return balance, extract, withdrawals_made


@clear_screen
def deposit(balance: float, extract: str, /) -> tuple[float, str]:
    print(" Operação de Depósito Bancário ".center(TERMINAL_WIDTH, "#"))

    try:
        value = float(input("\nEntre com o valor a ser depositado: "))

        if value <= 0:
            raise ValueError

        balance += value
        extract += f"Depósito: R$ {value:.2f}\n"

        message("\nOperação realizada com sucesso!!!")
    except ValueError:
        message(
            "\nOperação falhou! O valor informado deve ser somente numérico, positivo e diferente de zero."
        )
    finally:
        return balance, extract


@clear_screen
def extract_display(balance: float, /, *, extract: str) -> None:
    print(" Extrato Bancário ".center(TERMINAL_WIDTH, "#",))

    if not extract:
        print("Não foram realizadas movimentações.")
    else:
        print(extract)

    print("-"*TERMINAL_WIDTH)
    print(f"Saldo: R$ {balance:.2f}.")

    print("#"*TERMINAL_WIDTH)
    input("\nPressione ENTER para retornar ao menu de operações.")


@clear_screen
def close() -> str:
    print(" Sair do Sistema Bancário ".center(TERMINAL_WIDTH, "#",))

    return input("\nDeseja realmente finalizar as operações? [s-sim/N-não] => ").lower()


def create_current_account(current_accounts: list, users: list):
    ...
    # TODO: Criar lógica para criação da conta corrente.
    # Composição: Agência, número da conta e usuário.
    # Regras: Número da conta é sequencial, iniciando em 1. O número da agência é fixo. O usuário pode ter
    # mais de uma conta mas uma conta pertence a somente um usuário.


@clear_screen
def create_user() -> dict:
    print(" Cadastro de Cliente - Dados Pessoais ".center(TERMINAL_WIDTH, "#",))

    try:
        name = input("\nDigite seu nome completo: ").title()

        if len(name.split()) <= 1:
            raise ValueError("O nome deve conter duas ou mais expressões.")

        birth = datetime.strptime(input("\nData de nascimento [dd/mm/yyyy]: "), "%d/%m/%Y")

        cpf = input("\nInforme seu número de CPF [apenas números]: ")

        if len(cpf) != 11:
            raise ValueError("CPF deve conter 11 dígitos.")

        for digit in cpf:
            if digit not in digits:
                raise ValueError("CPF deve conter apenas números")

        print()
        print(" Cadastro de Cliente - Endereço ".center(TERMINAL_WIDTH, "#",))

        address = (
            f"{input("\nLogradouro: ").title()}, {input("\nNúmero: ")} - {input("\nBairro: ").title()} - "
            f"{input("\nCidade: ").title()}/{input("\nUF: ").upper()}"
        )

        # TODO: Construir críticas para dados de endereço como logradouro com mais de duas expressões, número
        # contendo apenas dígitos númericos e UF apenas com 2 letras contidas em uma lista de UF's
        # brasileiras.

        return {
            "nome": name,
            "data de nascimento": birth,
            "cpf": cpf,
            "endereço": address
        }
    except ValueError as exc:
        for arg in exc.args:
            if "does not match format" in arg or "day is out of range for month" in arg:
                exc = "Data de nascimento inválida."

        message(f"\nOperação falhou! {exc}")


def main():
    users: list = [dict]
    current_accounts: list = [dict]
    balance = 0
    limit = 500
    extract = ""
    withdrawals_made = 0

    while True:
        option = menu()

        match option:
            case "d":
                balance, extract = deposit(balance, extract)
            case "s":
                balance, extract, withdrawals_made = withdraw(
                    balance=balance, extract=extract, limit=limit, withdrawals_made=withdrawals_made
                )
            case "e":
                extract_display(balance, extract=extract)
            case "q":
                response = None

                while response is None:
                    response = close()
                    if response == "s":
                        message("\nAguardamos seu retorno! Até a próxima!")
                        break
                    elif response == "n" or response == "":
                        break
                    else:
                        message("\nOpção inválida!!! Selecione apenas opções válidas.")
                        response = None

                if response == "s":
                    os.system("clear") if os.name == "posix" else os.system("cls")
                    break
            case "cc":
                current_accounts = create_current_account(current_accounts, users)
            case "cu":
                user_created = create_user()
                user_already_exist = False

                if user_created is not None:
                    if len(users) > 0:
                        for user in users:
                            if user["cpf"] == user_created["cpf"]:
                                user_already_exist = True

                    if user_already_exist:
                        message("\nOperação Falhou! Usuário já cadastrado.")
                    else:
                        users.append(user_created)
                        message("\nOperação realizada com sucesso!!!")

            case _:
                message(
                    "Operação inválida!!! "
                    "Selecione apenas operações válidas no menu de opções."
                )


if __name__ == "__main__":
    main()
