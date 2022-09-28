import csv
from faker import Faker
import datetime as dt
import random
import os
from dotenv import load_dotenv
from datetime import datetime


class Generator:
    def __init__(self, records, headers):
        self.records = records
        self.headers = headers
    def open_write_file(self, filename):
        load_dotenv()
        path =os.getenv('Data_path') 
        #BUYER_FILE
        #/home/venkata/MEGAsync/Github repos/clg projects/Anonymize_buyer_and_seller
        if not os.path.exists(path):
            os.makedirs(path)
        csvFile = open(os.path.join(path, filename), "wt", newline="")
        writer = csv.DictWriter(csvFile, fieldnames=self.headers)
        writer.writeheader()
        self.writer = writer
        self.file_var = csvFile

    def close_file(self):
        self.file_var.close()

    def alpha_numeric(self, n):
        alpha = "".join(random.choice("ABCDEF") for i in range(int(n / 2)))
        res = alpha.join(random.choice("0123456789") for i in range(int(n / 2)))
        return res

    def datagenerate_buyer(self, filename):
        Faker.seed(0)
        zip_code_array=[530493,345654,234568,786565,694857, 879676, 968576,607989, 584574, 239110, 530413,355654,232568,786585,394857, 829676, 768576, 407989, 784574, 239210, 540493, 305654,234528,726565, 994857, 809676, 358576, 647989, 599574, 202110]
        fake = Faker("en_IN")
        self.open_write_file(filename)
        for i in range(self.records):
            name = fake.name()
            self.writer.writerow(
                {
                    "Id": i + 1,
                    "Customer ID": self.alpha_numeric(6),
                    "Name": name,
                    "Birth Date": fake.date(
                        pattern="%d-%m-%Y", end_datetime=dt.date(2010, 1, 1)
                    ),
                    "Phone No.": int(fake.numerify("##########")),
                    "Email Id": name.replace(" ", "").lower()
                    + "@"
                    + fake.free_email_domain(),
                    "Credit card": fake.credit_card_number(),
                    "Card Expiry": fake.credit_card_expire(),
                    "Address": fake.street_address().replace(",","-").replace("\n"," "),
                    "Zip Code": zip_code_array[random.randint(0,29)],
                    #"Zip Code": fake.postcode(),
                    "City": fake.city(),
                    "State": fake.state(),
                    "Country": fake.current_country(),
                    "Year": fake.date_between_dates(date_start=datetime(2010,1,1)).year,
                    "Aadhar":fake.aadhaar_id(),
                    "Time": fake.time(),
                }
            )
        self.close_file()

    def datagenerate_seller(self, filename):
        Faker.seed(0)
        fake = Faker(["en_US", "en_IN"])
        self.open_write_file(filename)
        for i in range(self.records):
            company_name = fake.company().replace(" ", "").replace(",","_")
            self.writer.writerow(
                {
                    "Id": i + 1,
                    "Supplier ID": self.alpha_numeric(4),
                    "Company Name": company_name
                    + " "
                    + fake.company_suffix(),
                    "Description": fake.sentence(nb_words=10),
                    "Address": fake.address(),
                    "State": fake.state(),
                    "Postal Code": fake.postcode(),
                    "Email Id": company_name.lower()
                    + "@"
                    + fake.domain_name(),
                    "URL": "www."
                    + company_name
                    + fake.domain_word()
                    + ".com",
                    "Invoice No.": int(fake.numerify("####")),
                    "Phone No.": int(fake.numerify("##########")),
                    "Time": fake.time(),
                }
            )
        self.close_file()

    def datagenerate_ECommerce(self, filename):
        Faker.seed(0)
        fake = Faker(["en_US"])
        self.open_write_file(filename)
        for i in range(records):
            self.writer.writerow(
                {
                    "Id": i + 1,
                    "Invoice No.": int(fake.numerify("####")),
                    "Stock code": self.alpha_numeric(6),
                    "Description": fake.sentence(nb_words=10),
                    "Quantity": random.randint(1, 6),
                    "Invoice date": fake.date_between_dates(
                        date_start=dt.date(2006, 1, 1)
                    ).strftime("%d-%m-%Y"),
                    "Unit price": float(fake.numerify("###.##")),
                    "Customer ID": self.alpha_numeric(6),
                }
            )
        self.close_file()


if __name__ == "__main__":
    # load_dotenv()
    load_dotenv()
    records = 100
    #int(os.getenv("record_count"))

    # SD are: Credit card, Card expiry (H,I)
    # EI are: Customer ID, Name, Email Id (B,C,G)
    # QI are: remaining attributes (D,E,F,J,K,L,M)
    headers = [
        "Id",
        "Customer ID",
        "Name",
        "Birth Date",
        "Phone No.",
        "Email Id",
        "Credit card",
        "Card Expiry",
        "Address",
        "Zip Code",
        "City",
        "State",
        "Country",
        "Year",
        "Aadhar",
        "Time",
    ]
    BUYER_DATA = Generator(records, headers)
    BUYER_DATA.datagenerate_buyer(os.getenv("BUYER_FIL"))
    print("Buyer data CSV generation complete!")

    # EI are: Supplier ID, Company Name, Email Id
    # QI are: remaining attributes
    headers = [
        "Id",
        "Supplier ID",
        "Company Name",
        "Description",
        "Address",
        "State",
        "Postal Code",
        "Email Id",
        "URL",
        "Invoice No.",
        "Phone No.",
        "Time",
    ]
    SELLER_DATA = Generator(records, headers)
    os.getenv("SELLER_FILE")
    SELLER_DATA.datagenerate_seller(os.getenv("SELLER_FILE"))
    print("Seller data CSV generation complete!")

    # SD are: Invoice No.
    # EI are: Customer ID
    # QI are: remaining attributes
    headers = [
        "Id",
        "Invoice No.",
        "Stock code",
        "Description",
        "Quantity",
        "Invoice date",
        "Unit price",
        "Customer ID",
    ]
    E_COMM_DATA = Generator(records, headers)
    
    E_COMM_DATA.datagenerate_ECommerce(os.getenv("E_COMM_FILE"))
    print("E-Commerce data CSV generation complete!")
