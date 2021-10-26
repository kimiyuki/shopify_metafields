import settings
import http
import requests
import json
import logging
import os
import re
import time

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
req_log = logging.getLogger("requests.packages.urllib3")
req_log.setLevel(logging.ERROR)
req_log.propagate = True

from settings import SHOPIFY_PW, SHOPIFY_USER, SHOP_DOMAIN

dpath = f"{SHOP_DOMAIN}/admin/api/2021-10"
cid = "3164927983729"  # report@spacexone.com
mid = "19509652258929"  # global, gender
pid = "4456090665073"  # 6食 喜多方ラーメン・ストレートスープ メンマ付
url = "https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/customers/{cid}/metafields/{mid}.json".format(
    **locals()
)
header = {"Content-Type": "application/json"}
# response = requests.get(url, headers=header)
# res = requests.put(url, data, headers=header)
# res = requests.get(url, headers=header)

url2 = "https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/metafields.json?metafield[owner_id]={cid}&metafield[owner_resource]=customer".format(
    **locals()
)
# res = requests.get(url2, headers=header)

data = {"metafield": {"id": mid, "value": "hello", "type": "single_line_text_field",}}
# res = requests.put(url3, data=data, headers=header)

url4 = "https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/metafields.json?metafield[owner_id]={pid}&metafield[owner_resource]=product".format(
    **locals()
)


mid2 = "19414721364081"
url3 = "https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/metafields/{mid}.json".format(
    **locals()
)
data = {"metafield": {"id": mid2, "value": "冷蔵便"}}
#res = requests.put(url3, headers=header, data=json.dumps(data))

#create metafields
url5 = "https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/customers/{cid}/metafields.json".format(
    **locals()
)
data = {"metafield": {"namespace": 'shirai', 'key':'birthday', 'value': "1971/02/31", "type":"single_line_text_field"}}
res = requests.post(url5, data=json.dumps(data), headers=header)


