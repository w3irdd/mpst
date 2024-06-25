from console_ui import raws
from scripts import fortinet


def print_main():
    print(raws.GREETING)
    print(raws.SCENARIOS)
    print(raws.GREETING_LINE, end='')


def select_script(num):
    match num:
        case '1':
            fortinet.run()
        case _:
            print(raws.WRONG_ARGS)


def start():
    print_main()

    script_num = input()

    select_script(script_num)
