#!/usr/bin/env python
import argparse
from app.init import check_and_install_models, check_and_install_transliteration

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--load_only_lang_codes", type=str, default="")
    args = parser.parse_args()
    lang_codes = args.load_only_lang_codes.split(",") or None
    check_and_install_models(force=True, load_only_lang_codes=lang_codes)
    check_and_install_transliteration(force=True)
