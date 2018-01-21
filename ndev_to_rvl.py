import platform
import subprocess
import sys

def main():
    print("NDEV to RVL, by Larsenv.")

    if len(sys.argv) != 2:
        print("This tool is used to convert an NDEV")
        print("Usage: ndev_to_rvl.py <elf file>")

    wiielffix()
    error002()

def wiielffix():
    print("Running WiiElfFix so the .elf can be run through HBC...")

    subprocess.call(["cp", sys.argv[1], sys.argv[1][:-4] + "_rvl.elf"])
    
    if platform.system() == "Windows":
        subprocess.call(["WiiElfFix.exe", sys.argv[1]])
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        print("Linux/Mac detected, you need Wine to run WiiElfFix.")
        subprocess.call(["wine", "WiiElfFix.exe", sys.argv[1]])

def error002():
    print("Patching out Error 002...")

    with open(sys.argv[1][:-4] + "_rvl.elf", "rb") as f:
        read = f.read()

    if read[:4] != b"\x7fELF":
        print("Not an ELF file!")
        exit()

    read = read.replace(b"\x2C\x00\x00\x00\x40\x82\x01\xD4\x3C\x60\x80\x00",
                           b"\x2C\x00\x00\x00\x48\x00\x02\x14\x3C\x60\x80\x00")

    with open(sys.argv[1][:-4] + "_rvl.elf", "wb") as dest_file:
        dest_file.write(read)

if __name__ == "__main__":
    main()
