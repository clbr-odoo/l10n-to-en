import getopt
import polib
import requests
import sys

"""
Uses: https://libretranslate.com/
"""


def translate(to_translate, lang):
    r = requests.post('http://localhost:5000/translate', json={
        'q': to_translate,
        'source': lang,
        'target': 'en',
        'format': 'text',
    })
    if r.status_code == 200:
        print(to_translate, ' -> ', r.json()['translatedText'])
        return r.json()['translatedText']
    else:
        print(f'ERROR: Couldn\'t find translation for term {to_translate}')
        return ''


def translate_pot(pot_path, language):
    pofile = polib.pofile(pot_path)
    for entry in pofile:
        to_translate = entry.msgid
        entry.msgstr = translate(to_translate, language)
    pofile.save()


def print_help():
    print('translate_to_en.py -p <pot_path>\n',
          'You need to have a general .pot file already created. Script will only work on a well formed .pot file.\n',
          'You also need to have libretranslate started and running on localhost:5000.\n',
          'This script will only translate msgid -> msgstr from provided language to english.\n',
          'Reversal and replacement will be done in post_translation script.')


def main(argv):
    pot_path = ''
    language = None
    try:
        opts, args = getopt.getopt(argv, "hp:l:", ["pot_path=", "language="])
    except getopt.GetoptError:
        print_help()
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-p", "--pot_path"):
            pot_path = arg
        elif opt in ("-l", "--language"):
            language = arg
    translate_pot(pot_path, language)


if __name__ == '__main__':
    main(sys.argv[1:])
