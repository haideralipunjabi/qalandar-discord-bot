import os
import subprocess


class Scanner:

    def __init__(self):
        self.device_name = self._getScanner()

    def _getScanner(self):
        try:
            output = str(
                subprocess.check_output("scanimage -L | grep epsonscan2", shell=True)
            )
            if output != "":
                return output[output.index("`") + 1 : output.index("'")]
        except:
            return None

    def scanImage(self, filepath, dpi=300):
        if os.path.isfile(filepath):
            os.system(f"rm {filepath}")
        os.system(
            f'scanimage --device-name="{self.device_name}" --resolution={dpi} --mode=Color --format=jpeg -o {filepath}'
        )

    def scanPDF(self, filepath, dpi=300):
        if os.path.isfile(filepath):
            os.system(f"rm {filepath}")
        os.system(
            f'scanimage --device-name="{self.device_name}" --resolution={dpi} --mode=Color --format=pdf --scan-area=A4 -o {filepath}'
        )

    def available(self):
        return device_name != None
