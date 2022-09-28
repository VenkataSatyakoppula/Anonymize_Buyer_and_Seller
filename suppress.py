"""
SUPPRESSION ATTRIBUTES
"""


import csv
import os
from dotenv import load_dotenv

load_dotenv()
path = os.getenv("path_anonymized")
target_path = os.getenv("path_anonymized")


def supress_rows_buyer(rows):
    for row in rows:
        row["Address"] = "***** ***** ***** *****"
        row["Phone No."] = "**********"
        row["Credit card"] = "**** **** ****"
        yield row


def supress_rows_seller(rows):
    for row in rows:
        row["Address"] = "***** ***** ***** *****"
        row["Phone No."] = "**********"
        yield row


def supress_file(filename, arg):
    source = os.path.join(path, filename)
    target = os.path.join(target_path, filename.split(".")[0] + os.getenv("stage2")+".csv")
    with open(source, "r") as f:
        with open(target, "w", newline="") as o:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(o, reader.fieldnames)
            writer.writeheader()
            if arg == "buyer":
                for row in supress_rows_buyer(reader):
                    writer.writerow(row)
            elif arg == "seller":
                for row in supress_rows_seller(reader):
                    writer.writerow(row)
        print(
            "Writing onto CSV done! -- Supressed address, credit card and phone numbers"
        )


if __name__ == "__main__":
    filename1 = os.getenv("BUYER_FIL").split(".")[0] + os.getenv("stage1") + ".csv"
    filename2 = os.getenv("SELLER_FILE").split(".")[0] + os.getenv("stage1") + ".csv"
    filename = os.getenv("E_COMM_FILE").split(".")[0] + os.getenv("stage1") + ".csv"
    supress_file(filename1, "buyer")
    supress_file(filename2, "seller")