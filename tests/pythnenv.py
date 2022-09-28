import os
from dotenv import load_dotenv
load_dotenv()
#setting environment variables
#os.environ['BUYER_FILE'] = '/home/venkata/MEGAsync/Github repos/clg projects/Anonymize_buyer_and_seller/Generated_data'
#os.environ['SELLER_FILE'] = '/home/venkata/MEGAsync/Github repos/clg projects/Anonymize_buyer_and_seller/Generated_data'
#os.environ['E_COMM_FILE'] = '/home/venkata/MEGAsync/Github repos/clg projects/Anonymize_buyer_and_seller/Generated_data'

print(os.getenv("BUYER_FIL"))