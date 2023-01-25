from transcribe import transcribe_audio
import json
import threading


def get_languages():
    with open('languages.json') as json_file:
        data = json.load(json_file)
        return data


def show_languages(languages):
    count = 1
    for language in languages['Languages']:
        print(f"{count}. {language['LanguageName']}")
        count += 1


def show_principal_menu():
    print("1. Translate")
    print("2. Exit")

    option = int(input("\nChoose an option: "))
    if option == 1:
        pass
    elif option == 2:
        exit()
    else:
        print("Invalid option\n")
        show_principal_menu()


def principal_menu():
    print("Welcome to Live Translator by: Daniel Ayala Cantador")
    show_principal_menu()

    languages = get_languages()
    language_input, language_output = choose_languages(languages)
    threading.Thread(target=transcribe_audio(language_input, language_output)).start()
    # Exit the program when the user presses the enter key
    input("Press Enter to exit...")
    exit()


def choose_languages(languages):
    language_input, language_output = None, None
    salir = False
    option = 0

    while not salir:
        print("\nList of languages:")
        show_languages(languages)
        language_input = int(input("\nInput language, choose an option: "))
        language_output = int(input("Output language, choose an option: "))

        if language_input == language_output:
            print("The input and output languages must be different")
        elif language_input < 1 or language_output < 1 or language_input >= len(
                languages['Languages']) + 1 or language_output >= len(languages['Languages']) + 1:
            print("Invalid option")
        else:
            language_input = languages['Languages'][language_input - 1]['LanguageCode']
            language_output = languages['Languages'][language_output - 1]['LanguageCode']

            print(f"\nInput language: {language_input}")
            print(f"Output language: {language_output}")
            salir = True

    return language_input, language_output


if __name__ == '__main__':
    principal_menu()
