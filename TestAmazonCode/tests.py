from django.test import TestCase

# Create your tests here.
import requests

data = {
    "data": [
        {
            "goods_url": "https://www.amazon.com/dp/B0C5RLRFJQ?ref=myi_title_dp",
            "code": "80D4LPOE"
        },
        {
            "goods_url": "https://www.amazon.com/promocode/A18QZBYWXY63FH",
            "code": "5019LF1U"
        },
        {
            "goods_url": "https://www.amazon.com/winees-Security-Wireless-Detection-L1/dp/B0BS8Z7GQZ/?maas=maas_adg_7DF32D6807A85CF8D5DDB54623F07D71_afap_abs&ref_=aa_maas&tag=maas",
            "code": "PG4YPOXE"
        },
    ]
}
r = requests.post(url=" http://127.0.0.1:8000/amazonWebsite/testCode/", json=data)
print(r.text)