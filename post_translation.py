import getopt
import os
import polib
import shutil
import sys


def replace_in_files(pofile, module_path):
    path = os.listdir(module_path)
    for file in path:
        try:
            with open(module_path + file, 'r') as f:
                result = f.read()
        except Exception as e:
            print(f"ERROR: Couldn't read file {file}")
            print(e)
            continue
        else:
            for entry in pofile:
                if entry.msgid:
                    result = result.replace(f">{entry.msgstr}<", f">{entry.msgid}<")
                    result = result.replace(f",\"{entry.msgstr}\",", f",\"{entry.msgid}\",")
            print(f"Replacing translated terms in {file}")
            with open(module_path + file, 'w') as newfile:
                newfile.write(result)


def reverse_pot(pofile):
    for entry in pofile:
        if entry.msgid and entry.msgstr:
            tmp = entry.msgid
            entry.msgid = entry.msgstr
            entry.msgstr = tmp
    pofile.save()


def create_po(pot_path, language: str):
    po_path = f'{pot_path[:pot_path.rfind("/")]}/{language}.po'
    try:
        shutil.copyfile(pot_path, po_path)
    except Exception as e:
        print("Couldn't create .po file from .pot file.")
        print(e)
        exit(-1)


def remove_translation_from_pot(pofile):
    for entry in pofile:
        entry.msgstr = ''
    pofile.save()


def print_help():
    print('post_translation.py -p <pot_path> -m <module_path> -l <language>')
    print('You need to have a general .pot file already created. Script will only work on a well formed .pot file.')


def main(argv):
    pot_path = ''
    module_path = ''
    language = ''
    try:
        opts, args = getopt.getopt(argv, "hp:m:l:", ["pot_path=", "module_path", "language"])
    except getopt.GetoptError:
        print_help()
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-p", "--pot_path"):
            pot_path = arg
        elif opt in ("-m", "--module_path"):
            module_path = arg
        elif opt in ("-l", "--language"):
            language = arg
    pofile = polib.pofile(pot_path)
    reverse_pot(pofile)
    create_po(pot_path, language)
    replace_in_files(pofile, module_path)
    remove_translation_from_pot(pofile)


if __name__ == '__main__':
    main(sys.argv[1:])
