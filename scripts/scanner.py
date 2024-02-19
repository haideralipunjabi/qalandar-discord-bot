import os

# TODO: Fetch Scanner Name instead of hard coding


def scanImage(filepath, dpi=300):
    if os.path.isfile(filepath):
        os.system(f"rm {filepath}")
    os.system(
        f'scanimage --device-name="epsonscan2:EPSON L360 Series:001:006:esci2:usb:ES0114:2257" --resolution={dpi} --mode=Color --format=jpeg -o {filepath}'
    )


def scanPDF(filepath, dpi=300):
    if os.path.isfile(filepath):
        os.system(f"rm {filepath}")
    os.system(
        f'scanimage --device-name="epsonscan2:EPSON L360 Series:001:006:esci2:usb:ES0114:2257" --resolution={dpi} --mode=Color --format=pdf -o {filepath}'
    )
