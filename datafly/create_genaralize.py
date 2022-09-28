import os

if not os.path.exists(os.path.dirname(__file__) + "/conf"):
    os.makedirs(os.path.dirname(__file__) + "/conf")

ATTNAME = [
    "Id",
    "Customer ID",
    "Name",
    "Age",
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

AGECONFFILE = "age_hierarchy.csv"
ZIPCODECONFFILE = "zip_hierarchy.csv"

def readdata(filepath, filename):
    records = []
    try:
        with open(os.path.join(filepath, filename), "r") as rf:
            i = 0
            for line in rf:
                line = [a.strip() for a in line.split(",")]
                if i != 0:
                    records.append(line)
                i += 1
        return records
    except Exception as e:
        print(e)


def generate_hierarchy_for_age(records):
    youngest, oldest = float("inf"), -float("inf")
    ageidx = ATTNAME.index("Age")
    for record in records:
        if int(record[ageidx]) > oldest:
            oldest = int(record[ageidx])
        if int(record[ageidx]) < youngest:
            youngest = int(record[ageidx])
    print("Age max: %d min: %d" % (oldest, youngest))
    with open(
        os.path.join(os.path.dirname(__file__) + "/conf", AGECONFFILE), "w+"
    ) as wf:
        for i in range(youngest, oldest + 1):
            h = []
            h.append(str(i))
            h.append("%s-%s" % (i // 18 * 18, (i // 18 + 1) * 18))
            h.append("%s-%s" % (i // 25 * 25, (i // 25 + 1) * 25))
            h.append("%s-%s" % (i // 45 * 45, (i // 45 + 1) * 45))
            h.append("%s-%s" % (i // 75 * 75, (i // 75 + 1) * 75))
            h.append("%s-%s" % (i // 100 * 100, (i // 100 + 1) * 100))
            wf.write(",".join(h))
            wf.write("\n")


    

def generate_hierarchy_for_zip(records):
    zipset = set()
    zipudx = ATTNAME.index("Zip Code")
    for record in records:
        if record[zipudx] != "*" and record[zipudx] not in zipset:
            zipset.add(record[zipudx])
    with open(
        os.path.join(os.path.dirname(__file__) + "/conf", ZIPCODECONFFILE), "w+"
    ) as wf:
        for zip in zipset:
            wf.write(
                zip
                + ","
                + zip[0:5]
                + "0"
                + ","
                + zip[0:4]
                + "00"
                + ","
                + zip[0:3]
                + "000"
                + ","
                + zip[0:2]
                + "0000"
                + ","
                + zip[0:1]
                + "00000"
            )
            wf.write("\n")


if __name__ == "__main__":
    records = readdata(
        os.path.dirname(__file__) + "/example", "Buyer_data_for_data_fly.csv"
    )
    generate_hierarchy_for_age(records)
    print("Generated hierarchy for all possible generalized ages")
    generate_hierarchy_for_zip(records)
    print("Generated hierarchy for all possible generalized zipcodes")
