from pathlib import Path

from argostranslate import package, translate

import app.language


def boot(load_only=None):
    try:
        check_and_install_models(load_only_lang_codes=load_only)
    except Exception as e:
        print("Cannot update models (normal if you're offline): %s" % str(e))


def check_and_install_models(force=False, load_only_lang_codes=None):
    if len(package.get_installed_packages()) < 2 or force:
        # Update package definitions from remote
        print("Updating language models")
        package.update_package_index()

        # Load available packages from local package index
        available_packages = package.get_available_packages()
        print("Found %s models" % len(available_packages))

        if load_only_lang_codes is not None:
            # load_only_lang_codes: List[str] (codes)
            # Ensure the user does not use any unavailable language code.
            # unavailable_lang_codes = set(load_only_lang_codes)
            # for pack in available_packages:
            #     unavailable_lang_codes -= {pack.from_code, pack.to_code}
            # if unavailable_lang_codes:
            #     raise ValueError(
            #         "Unavailable language codes: %s."
            #         % ",".join(sorted(unavailable_lang_codes))
            #     )
            # Keep only the packages that have both from_code and to_code in our list.
            avail_p={"%s-%s" % (pack.from_code,pack.to_code) : pack  for pack in available_packages}
            selected_packages=[]
            for p in load_only_lang_codes:
                if p in avail_p:
                    selected_packages.append(avail_p[p])

            # available_packages = [
            #     pack
            #     for pack in available_packages
            #     if pack.from_code in load_only_lang_codes and pack.to_code in load_only_lang_codes
            # ]
            if not selected_packages:
                raise ValueError("no available package")
            print("Keep %s models" % len(selected_packages))

        # Download and install all available packages
        for available_package in selected_packages:
            print(
                "Downloading %s (%s) ..."
                % (available_package, available_package.package_version)
            )
            download_path = available_package.download()
            package.install_from_path(download_path)

        # reload installed languages
        app.language.languages = translate.get_installed_languages()
        print(
            "Loaded support for %s languages (%s models total)!"
            % (len(translate.get_installed_languages()), len(available_packages))
        )
