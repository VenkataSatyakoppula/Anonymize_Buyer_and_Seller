"""
THIS CODE TOKENIZES ALL GENERATED DATA SETS
TOKENIZED ATTRIBUTES
NAME,EMAIL ID,CUSTOMER ID ---> BUYER_FILE
COMPANY NAME,EMAIL ID,SUPPLIER ID ---> SELLER_FILE
CUSTOMER_ID ---> E_COMM_FILE
"""

import csv
from faker import Faker
from collections import defaultdict
import os
from dotenv import load_dotenv
import random




def alpha_numeric(n):
    alpha = "".join(random.choice("ABCDEF") for i in range(int(n / 2)))
    res = alpha.join(random.choice("0123456789") for i in range(int(n / 2)))
    return res


load_dotenv()
path = os.getenv("Data_path")
target_path = os.getenv("path_anonymized")
if not os.path.exists(target_path):
    os.makedirs(target_path)


def tokenize_rows_buyer(rows):
    faker = Faker()
    c1 = defaultdict(faker.name)
    for row in rows:
        row["Name"] = c1[row["Name"]]
        row["Email Id"] = row["Name"].replace(" ", "") + "@" + faker.free_email_domain()
        row["Customer ID"] = alpha_numeric(6)
        yield row


def tokenize_rows_seller(rows):
    faker = Faker()
    c1 = defaultdict(faker.company)
    for row in rows:
        row["Company Name"] = c1[row["Company Name"]]
        row["Email Id"] = (
            row["Company Name"].replace(" ", "").replace(",", "").lower()
            + "@"
            + faker.free_email_domain()
        )
        row["Supplier ID"] = alpha_numeric(4)
        yield row


def tokenize_rows_ecommerce(rows):
    faker = Faker()
    for row in rows:
        row["Customer ID"] = alpha_numeric(6)
        yield row

def tokenize_file(filename, arg):
    source = os.path.join(path, filename)
    target = os.path.join(target_path, filename.split(".")[0] + "_tokenized.csv")
    with open(source, "r") as f:
        with open(target, "w", newline="") as o:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(o, reader.fieldnames)
            writer.writeheader()
            if arg == "buyer":
                for row in tokenize_rows_buyer(reader):
                    writer.writerow(row)
            elif arg == "seller":
                for row in tokenize_rows_seller(reader):
                    writer.writerow(row)
            else:
                for row in tokenize_rows_ecommerce(reader):
                    writer.writerow(row)
        print("Writing onto CSV done! -- Tokenized name, IDs and email IDs")


if __name__ == "__main__":
    filename1 = os.getenv("BUYER_FIL")
    filename2 = os.getenv("SELLER_FILE")
    filename3 = os.getenv("E_COMM_FILE")
    tokenize_file(filename1, "buyer")
    tokenize_file(filename2, "seller")
    tokenize_file(filename3, "ecommerce")
