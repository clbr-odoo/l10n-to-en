import getopt
import os
import polib
import sys


def print_help():
    print('same_lang_diff_name.py -s <source_file> -t <target_file>')


def fill_target(src, tgt):
    for src_entry in src:
        tgt_entry = tgt.find(src_entry.msgid)
        if tgt_entry:
            if not tgt_entry.msgstr:
                tgt_entry.msgstr = src_entry.msgstr
        else:
            tgt.append(src_entry)
    tgt.save()


def main(argv):
    source_file = ''
    target_file = ''
    try:
        opts, args = getopt.getopt(argv, "hs:t:", ["source_file", "target_file"])
    except getopt.GetoptError:
        print_help()
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-s", "--source_file"):
            source_file = arg
        elif opt in ("-t", "--target_file"):
            target_file = arg
    try:
        src = polib.pofile(source_file)
        tgt = polib.pofile(target_file)
    except Exception as e:
        print("ERROR - Couldn't open po file(s).")
        print(e)
        sys.exit(-1)
    else:
        fill_target(src, tgt)


if __name__ == '__main__':
    main(sys.argv[1:])
