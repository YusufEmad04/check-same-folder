import os.path
import sys


def remove_crlf(text):
    return text.replace(b"\r\n", b"\n")


def check_files(f1, f2):
    with open(f1, "rb") as file1, open(f2, "rb") as file2:
        same = False
        f1 = file1.read(1024)
        f2 = file2.read(1024)
        while (f1 == f2) and f1:
            f1 = file1.read(1024)
            f2 = file2.read(1024)

            if f1 != f2:
                return False

    return f1 == f2


def check_folders(f1, f2):
    try:
        dir1 = sorted(os.listdir(f1))
        dir2 = sorted(os.listdir(f2))

        for i in dir1:
            if i[0] == "." or i[0] == "__pycache__":
                dir1.remove(i)

        for i in dir2:
            if i[0] == "." or i[0] == "__pycache__":
                dir2.remove(i)

        if dir1 == dir2:
            for i in dir1:
                if not os.path.isdir(f1 + "/" + i):
                    if not check_files(f1 + "/" + i, f2 + "/" + i):
                        print("failed on file: " + i)
                        return False
                else:
                    if not check_folders(f1 + "/" + i, f2 + "/" + i):
                        print("failed on folder: " + i)
                        print(f1 + "/" + i)
                        return False
            return True
        else:
            return False

    except Exception as e:
        print("Error in trying to check folders" + str(e))


if len(sys.argv) != 4:
    print("Usage: check-same.py <f/d> <file1/folder1> <file2/folder2>")
else:
    if sys.argv[1] == "f":
        print(check_files(sys.argv[2], sys.argv[3]))
    elif sys.argv[1] == "d":

        if "." in sys.argv[2] or "." in sys.argv[3]:
            print("Error in args")
        else:
            print(check_folders(sys.argv[2], sys.argv[3]))
