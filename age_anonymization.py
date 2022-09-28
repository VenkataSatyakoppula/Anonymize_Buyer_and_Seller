"""
AGE ANONYMIZATION
"""



import csv
from faker import Faker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
path = os.getenv("path_anonymized")
target_path = os.getenv("path_anonymized")

def convert_to_age(rows):
    for row in rows:
        date_of_birth = row["Age"]
        date_array = date_of_birth.split("-")
        current_date = datetime.now()
        current_date = current_date.strftime("%d-%m-%Y")
        current_array = current_date.split("-")
        exact_age = int(current_array[2]) - int(date_array[2])
        row["Age"] = exact_age
        yield row

def age_anonymize(rows):
    for row in convert_to_age(rows):
        exact_age = int(row['Age'])
        if exact_age >= 0 and exact_age <= 20:
            age = "0-20"
        elif exact_age > 20 and exact_age <= 40:
            age = "21-40"
        elif exact_age > 40 and exact_age <= 60:
            age = "41-60"
        elif exact_age > 61 and exact_age <= 80:
            age = "61-80"
        else:
            age = ">80"
        exact_age = age
        row["Age"] = age

        yield row

def convert_to_age_file(filename, arg):
    path=os.getenv("path_anonymized")
    if not os.path.exists("datafly/example"):
        os.makedirs("datafly/example")
    target_path="datafly/example"
    source = os.path.join(path, filename)
    target = os.path.join(
        target_path, "Buyer_data_for_data_fly" + ".csv"
    )
    with open(source, "r") as f:
        with open(target, "w", newline="") as o:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if arg == "buyer":
                for i in range(len(fieldnames)):
                    if fieldnames[i] == "Birth Date":
                        fieldnames[i] = "Age"
                writer = csv.DictWriter(o, fieldnames=fieldnames)
                writer.writeheader()
                for row in convert_to_age(reader):
                    writer.writerow(row)
        print(
            "Writing onto CSV done! -- Converted birthdates to ages."
        )

def age_anonymize_file(filename, arg):
    source = os.path.join(path, filename)
    target = os.path.join(
        target_path, filename.split(".")[0] + os.getenv("stage4") + ".csv"
    )
    with open(source, "r") as f:
        with open(target, "w", newline="") as o:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if arg == "buyer":
                for i in range(len(fieldnames)):
                    if fieldnames[i] == "Birth Date":
                        fieldnames[i] = "Age"
                writer = csv.DictWriter(o, fieldnames=fieldnames)
                writer.writeheader()
                for row in age_anonymize(reader):
                    writer.writerow(row)
        print(
            "Writing onto CSV done! -- Anonymized date of birth and genaralized ages."
        )


if __name__ == "__main__":
    filename0=(
        os.getenv("BUYER_FIL").split(".")[0]
        +os.getenv("stage1")
        + os.getenv("stage2")
        + ".csv"
    )
    filename1 = (
        os.getenv("BUYER_FIL").split(".")[0]
        + os.getenv("stage1")
        + os.getenv("stage2")
        + os.getenv("stage3")
        + ".csv"
    )
    convert_to_age_file(filename0, "buyer")
    age_anonymize_file(filename1, "buyer")
