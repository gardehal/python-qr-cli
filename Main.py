import sys
import os
import qrcode
from dotenv import load_dotenv
load_dotenv()

from Util import *

outputDirectory = "qr"

os.system("") # Needed to "trigger" coloured text
helpFlags = ["-help", "-h"]
testFlags = ["-test", "-t"]
qrGenerateFlags = ["-generate", "-g"]
qrGenerateNormalSwitch = ["normal", "n"]
qrGenerateNetworkSwitch = ["network", "net"]

class Main:
    def main():
        argC = len(sys.argv)
        argV = sys.argv
        argIndex = 1

        if(argC < 2):
            Main.PrintHelp()

        while argIndex < argC:
            arg = sys.argv[argIndex].lower()

            if(arg in helpFlags):
                Main.PrintHelp()

            elif(arg in testFlags):
                args = Util.ExtractArgs(argIndex, argV)
                print("test")

                quit()

            elif(arg in qrGenerateFlags):
                args = Util.ExtractArgs(argIndex, argV)
                toEncode = args[0]

                primaryArgs = 1
                if(len(args) == primaryArgs or Util.arrayContains(args, qrGenerateNormalSwitch)):
                    _ = "" # No action needed
                elif(len(args) > primaryArgs and Util.arrayContains(args, qrGenerateNetworkSwitch)):
                    # "WIFI:T:WPA;S:<SSID>;P:<PASSWORD>;;"
                    split = toEncode.split(":")
                    if(len(split) == 2):
                        toEncode = f"WIFI:T:WPA;S:{split[0]};P:{split[1]};;"
                    else:
                        print("Please format SSID and password as instructed in -help.")
                        argIndex += len(args)
                        continue
                    
                outputFilename = f"{DateTimeObject().isoAsNumber}.png"
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(toEncode)
                qr.make(fit=True)
                img = qr.make_image(fill="black", back_color="white")

                Util.mkdir(outputDirectory)
                img.save(os.path.join(outputDirectory, outputFilename))

                argIndex += len(args)

            # Invalid, inform and quit
            else:
                print("Argument not recognized: \"" + arg + "\", please see documentation or run with \"-help\" for help.")

            argIndex += 1

    def PrintHelp():
        """
        A simple console print that informs user of program arguments.
        """

        print("--- Help ---")
        print("Arguments marked with ? are optional.")
        print("All arguments that triggers a function start with dash(-).")
        print("All arguments must be separated by space only.")
        print("\n")

        print(f"{str(helpFlags)}: prints this information about input arguments.")
        print(f"{str(testFlags)}: a method of calling experimental code (when you want to test if something works).")
        print(f"{str(qrGenerateFlags)} + [string to encode] +  [encoding type]: encode text to QR code.")
        print(f"\t- {str(qrGenerateNormalSwitch)}: encode the [string to encode] as normal.")
        print(f"\t- {str(qrGenerateNetworkSwitch)}:encode a string that will connect phones to networks (e.g. WIFI). Format [string to encode] as \"[SSID]:[passord]\".")

if __name__ == "__main__":
    Main.main()