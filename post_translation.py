import getopt
import os
import polib
import shutil
import sys
from os.path import join


def replace_in_files(pot_file, module_path):
    for dirpath, dirname, files in os.walk(module_path):
        for file in files:
            file_type = file[file.rfind('.') + 1:]
            po_modified = False
            try:
                po_file = None
                result = None
                if file_type in ['po', 'pot']:
                    po_file = polib.pofile(f"{dirpath}/{file}")
                elif file_type in ['xml', 'csv']:
                    with open(join(dirpath, file), 'r') as f:
                        result = f.read()
            except Exception as e:
                print(f"ERROR: Couldn't read file {file}")
                print(e)
                continue
            else:
                for entry in pot_file:
                    if entry.msgid and entry.msgstr:
                        if file_type in ['po', 'pot']:
                            for po_entry in po_file:
                                if entry.msgstr == po_entry.msgid:
                                    po_entry.msgid = entry.msgid
                                    po_modified = True
                        elif file_type == 'csv':
                            result = result.replace(f",\"{entry.msgstr}\",", f",\"{entry.msgid}\",")
                            result = result.replace(f",{entry.msgstr},", f",{entry.msgid},")
                        elif file_type == "xml":
                            result = result.replace(f">{entry.msgstr}<", f">{entry.msgid}<")
                print(f"Scanning terms in {file}")
                if po_file and po_modified:
                    po_file.save()
                elif result:
                    with open(join(dirpath, file), 'w') as newfile:
                        newfile.write(result)


def reverse_pot(potfile):
    for entry in potfile:
        if entry.msgid and entry.msgstr:
            tmp = entry.msgid
            entry.msgid = entry.msgstr
            entry.msgstr = tmp
    potfile.save()


def create_po(pot_path, po_path):
    try:
        shutil.copyfile(pot_path, po_path)
    except Exception as e:
        print("Couldn't create .po file from .pot file.")
        print(e)
        exit(-1)


def update_po(pot_file, po_file):
    for entry_pot in pot_file:
        if entry_pot.msgid and entry_pot.msgstr:
            entry_po = po_file.find(entry_pot.msgstr)
            if entry_po:
                entry_po.msgid = entry_pot.msgid
                entry_po.msgstr = entry_pot.msgstr
            else:
                po_file.append(entry_pot)
    po_file.save()


def remove_translation_from_pot(pot_file):
    for entry in pot_file:
        entry.msgstr = ''
    pot_file.save()


def print_help():
    print('post_translation.py -p <pot_path> -m <module_path> -l <language>')
    print('You need to have a general .pot file already created. Script will only work on a well formed .pot file.')


def main(argv):
    module_path = ''
    language = ''
    try:
        opts, args = getopt.getopt(argv, "hm:l:", ["module_path", "language"])
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
    module_name = f'{module_path[module_path.rfind("/")+1:]}'
    pot_path = f'{module_path}/i18n/{module_name}.pot'
    po_lang_path = f'{module_path}/i18n/{language}.po'
    pot_file = polib.pofile(pot_path)
    reverse_pot(pot_file)
    if os.path.exists(po_lang_path):
        po_file = polib.pofile(po_lang_path)
        update_po(pot_file, po_file)
    else:
        create_po(pot_path, po_lang_path)
    replace_in_files(pot_file, module_path)
    remove_translation_from_pot(pot_file)


if __name__ == '__main__':
    main(sys.argv[1:])
