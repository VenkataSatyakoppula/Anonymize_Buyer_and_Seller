"""
LOCAL RECODING
"""


import csv
import os
from dotenv import load_dotenv

load_dotenv()
path = os.getenv("path_anonymized")
target_path = os.getenv("path_anonymized")


def recode_zipcode(rows):
    for row in rows:
        zip_code = str(row["Zip Code"])
        zip_code = zip_code[0:3] + "00"
        row["Zip Code"] = zip_code
        yield row


def local_recode_file(filename, arg):
    source = os.path.join(path, filename)
    target = os.path.join(
        target_path, filename.split(".")[0] + os.getenv("stage3") + ".csv"
    )
    with open(source, "r") as f:
        with open(target, "w", newline="") as o:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(o, reader.fieldnames)
            writer.writeheader()
            if arg == "buyer":
                for row in recode_zipcode(reader):
                    writer.writerow(row)
        print("Writing onto CSV done! -- Locally recoded ZIP codes.")


if __name__ == "__main__":
    filename1 = (
        os.getenv("BUYER_FIL").split(".")[0]
        + os.getenv("stage1")
        + os.getenv("stage2")
        + ".csv"
    )
    local_recode_file(filename1, "buyer")
