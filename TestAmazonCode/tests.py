from django.test import TestCase

# Create your tests here.
import requests

data = {
    "data": [
        {
            "goods_url": "https://www.amazon.com/dp/B0C149M53B?ref=myi_title_dp&th=1",
            "code": "TJJ94ZF"
        },
        {
            "goods_url": "https://www.amazon.com/dp/B0BZYSFHW9",
            "code": "407B5M68"
        },
        {
            "goods_url": "https://www.amazon.com/dp/B0C4KK497G?ref=myi_title_dp&th=1",
            "code": "60Y63XQE"
        },
        {
            "goods_url": "https://www.amazon.com/ValueMax-15PC-BBQ-Grilling-Tool/dp/B09FPL2RD4?maas=maas_adg_B289569CC93A1E55FC87670FFDE7439D_afap_abs&ref_=aa_maas&tag=maas",
            "code": "50RKZ5MR"
        }
    ]
}
r = requests.post(url=" http://127.0.0.1:8000/amazonWebsite/testCode/", json=data)
print(r.text)