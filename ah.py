from difflib import SequenceMatcher
from functools import lru_cache
import argparse
import random
import click
import csv
import os


@lru_cache(maxsize=None)
def similar(s_1: str, s_2: str) -> float:
    # Misura di somiglianza tra due stringhe; memoizzato in quanto può essere oneroso
    return SequenceMatcher(None, s_1, s_2).ratio()


def isValidAsciiChar(c: int) -> bool:
    # Lettere e numeri più spazio
    return 65 <= c <= 90 or 97 <= c <= 122 or 48 <= c <= 57 or c == 32


def clearscreen(no_scroll: bool = False) -> None:
    if no_scroll:
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("\033[2J\033[1;1H", end='', flush=True)


def loadAcronymsFromFile(file_path: str, uniqueness_delimiter: str) -> dict:
    acronyms = dict()
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for (acronym, extended, description) in csv_reader:
            acronym += uniqueness_delimiter + f'{random.randint(0, 1_000_000_000):09d}'
            acronyms[acronym] = (extended, description.replace(r'\n', '\n').replace(r'\t', '\t'))

    return acronyms


def main(args) -> None:
    clearscreen(args.noscroll)

    file_name = args.file
    show_closest_n = args.show

    typed = ""

    delimiter = '_'

    acronyms = loadAcronymsFromFile(file_name, delimiter)

    while True:

        text = ''
        text_extra = ''
        k = click.getchar()

        if len(k) == 4:  # Non il miglior controllo lo so
            # tasto CANC per cancellare tutta la scritta
            text = ''
            text_extra = ''
            typed = ''

        else:
            k_ord = ord(k)

            if k_ord == 27:  # esc
                raise KeyboardInterrupt()
            elif isValidAsciiChar(k_ord) or k_ord == 127:
                if k_ord == 127:  # backspace
                    typed = typed[:-1]
                else:
                    typed += k.upper()

        if typed != '':

            close_ones = []

            for key, (value, desc) in acronyms.items():
                close_ones.append(
                    (similar(typed, key[0:len(typed)]), key, value, desc))

            closest = sorted(close_ones, reverse=True)[0][1]

            if closest != '':
                acr, description = acronyms[closest]
                text = f'{typed} -> {closest.split(delimiter)[0]}: {acr}'
                if description != "":
                    text += " (!)"
                if ord(k) == 13 and description != "":  # invio
                    text += f'\n\n{description}\n\n'

                else:

                    for close_one in sorted(close_ones, reverse=True)[1:show_closest_n + 1]:
                        close_k, close_v, close_desc = close_one[1:]
                        whitespace = ' ' * len(f'{typed} ->')
                        text_extra += f'\n{whitespace} {close_k.split(delimiter)[0]} -> {close_v}'

                        if close_desc != "":
                            text_extra += " (!)"

                    text_extra += '\n'

        clearscreen(args.noscroll)

        click.secho(text, fg=args.col, nl=False)
        click.echo(text_extra, nl=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Mostra acronimi estesi e simili.')
    parser.add_argument('--show', type=int, required=False,
                        default=6, help='Numero di acronimi simili da mostrare in coda')
    parser.add_argument('--file', type=str, required=True,
                        help='File .csv dal quale prendere gli acronimi')
    parser.add_argument('--col', type=str, required=False,
                        default='green', help='Colore della prima riga')
    parser.add_argument('--noscroll', required=False,
                        default=False, help='Pulire il terminale invece di farlo scorrere',
                        action='store_true')
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        # Per aver premuto 'esc' o Ctrl-C; esco
        clearscreen(args.noscroll)
    except TypeError as e:
        # Carattere non ASCII o altra roba strana; per caso è attivo num lock?
        click.echo(f'Carattere inaspettato: {e}')
    except EOFError as e:
        # Probabilmente per aver premuto Ctrl-D per uscire dal terminale; esco
        clearscreen(args.noscroll)
    except Exception as e:
        # Ah boh finora mai successo però
        click.echo(f'Qualcos\'altro è andato storto! Verificare: {e}')
