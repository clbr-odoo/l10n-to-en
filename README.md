# l10n-to-en

## Intro + Disclaimer
This module was meant to speed up and ease the translation of our localizations, 
you will of course need to **check** all translations by yourself and **corrections will be needed**.

The script is in two distinct parts :
1. `translate_to_en.py` will translate the `.pot` file
2. `post_translation.py` will do all the post-processing : 
    1. Inverse terms and translation into `.pot`
    2. Create the correct `language.po` file (with both english and foreign translations)
    3. Replace the foreign terms by their english translations in source files
    4. Remove foreign language from .pot file

## Requirements
The only extra requirement if you want to use first part of the script that translate is libretranslate.

## How-to
1. Install *libretranslate*. Note it will download a lot of languages, expect it to take some time.
   ```bash
   sudo pip install libretranslate
   sudo libretranslate
   ```
2. Export .pot file
   ```bash
   ./odoo-bin --addons-path="addons/,../enterprise/" --database {DB_NAME} --modules='{MODULE_NAME}' --i18n-export='{MODULE_PATH}/
   i18n/{MODULE_NAME}.pot' --language='{LANGUAGE_CODE}'
   ```
   See [here](https://www.notion.so/Localization-101-454abcff422c4110ac3898c9b5d7da05#ad77d275215549d0923ad11789bdf138) if you need more details.
3. Use script `translate_to_en.py`
   ```bash
   python3 translate_to_en.py -p {POT_FILE_PATH} -l {LANGUAGE_CODE}
   ```
   You provide the script the .pot file created previously (as it is, don't inverse msgid and msgstr, next script will handle that for you) and the XX code of the foreign language.

   Here is the [list of supported languages](https://libretranslate.com/languages).
4. Check all translations manually
5. Use script `post_translation.py`
   ```bash
   python3 post_translation.py -p {POT_FILE_PATH} -l LANGUAGE -m {MODULE_DATA_DIRECTORY_PATH}
   ```
   Provide the .pot file with your corrections (again **don't** inverse msgid and msgstr, script will do it), the foreign language and the path of the `data` directory of your localization, in which the script will replace foreign terms by english-translated terms.
6. You're done !

Don't hesitate to message me on Discord if you have questions: Claire (clbr)#3668