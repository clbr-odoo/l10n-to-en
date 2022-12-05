import getopt
import polib
import requests
import sys
from os import path

"""
Uses: https://libretranslate.com/
"""


def translate(to_translate, lang):
    try:
        r = requests.post('http://localhost:5000/translate', json={
            'q': to_translate,
            'source': lang,
            'target': 'en',
            'format': 'text',
        })
    except Exception as e:
        print("Couldn't connect to libretranslate, check if server is correctly started !")
        print(e)
        exit(-1)
    else:
        if r.status_code == 200:
            print(to_translate, ' -> ', r.json()['translatedText'])
            return r.json()['translatedText']
        else:
            print(f'ERROR: Couldn\'t find translation for term {to_translate}')
            return ''


def translate_pot(module_path, language, pot_path=None):
    if not pot_path:
        pot_path = f'{module_path}/i18n/{module_path[module_path.rfind("/") + 1:]}.pot'
    po_path = f'{module_path}/i18n/{language}.po'
    print(f'DEBUG - pot_path={pot_path}, po_path={po_path}')
    potfile = polib.pofile(pot_path)
    pofile = polib.pofile(po_path) if path.exists(po_path) else None
    for entry in potfile:
        to_translate = entry.msgid
        if pofile:
            entry_in_po = pofile.find(to_translate)
            if entry_in_po and entry_in_po.msgstr:
                # if there is already a translation in po file we reverse them in pot file (they will be correctly processed later)
                entry.msgid = entry_in_po.msgstr
                entry.msgstr = entry_in_po.msgid
                continue
        entry.msgstr = translate(to_translate, language)
    potfile.save()


def print_help():
    print('translate_to_en.py -p <pot_path>\n',
          'You need to have a general .pot file already created. Script will only work on a well formed .pot file.\n',
          'You also need to have libretranslate started and running on localhost:5000.\n',
          'This script will only translate msgid -> msgstr from provided language to english.\n',
          'Reversal and replacement will be done in post_translation script.')


def main(argv):
    module_path = None
    pot_path = None
    language = None
    try:
        opts, args = getopt.getopt(argv, "hm:l:p:", ["module_path=", "language=", "pot_path="])
    except getopt.GetoptError:
        print_help()
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-m", "--module_path"):
            module_path = arg
        elif opt in ("-l", "--language"):
            language = arg
        elif opt in ("-p", "--pot_path"):
            pot_path = arg
    translate_pot(module_path, language, pot_path)


if __name__ == '__main__':
    main(sys.argv[1:])
