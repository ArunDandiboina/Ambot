import requests
import smtplib
import lxml
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Accept-Language": "en-US,en;q=0.9"
}
res = requests.get(url=URL, headers=header)
soup = BeautifulSoup(res.text, "lxml")

whole = soup.select_one(selector=".a-spacing-none .a-price-whole").getText()
fraction = soup.select_one(selector=".a-spacing-none .a-price-fraction").getText()
price = float((whole + fraction))

if price < 100:
    my_email = email
    password = password
    with smtplib.SMTP("smtp.gmail.com", port=587) as conn:
        conn.starttls()
        conn.login(user=my_email, password=password)
        conn.sendmail(from_addr=my_email, to_addrs=f"{my_email}",
                      msg=f"Subject:PRIZE ALERT!!\n\n{URL}\nBUY IT NOW!")
        conn.close()
