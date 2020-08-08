import settings
import requests
import json
import logging
import http
import os
import re
import time

http.client.HTTPConnection.debuLevel = 2
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger("requests.packages.urllib3")
req_log.setLevel(logging.DEBUG)
req_log.propagate = True

from settings import SHOPIFY_PW, SHOPIFY_USER, SHOP_DOMAIN


def upsertMetaInProduct(pid, SHOPIFY_USER, SHOPIFY_PW, dpath, reviews):
    url = "https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/products/{pid}/metafields.json".format(
        **locals()
    )
    response = requests.get(url)
    r = response.json()
    myreviews = list(filter(lambda x: x['namespace'] =="shirai" and x['key']=="myreviews", r['metafields']))
        # update
    if len(myreviews) > 0:
        mid = myreviews[0]['id']
        print(f"update {mid}") 
        url = "https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/products/{pid}/metafields/{mid}.json".format(
            **locals()
        )
        meta = { "metafield": {
                    "id": mid,
                    "value": reviews,
                    "value_type": "string" } }
        response = requests.put(
            url, data=json.dumps(meta), headers={"Content-Type": "application/json"}
        )
        print(f"udpate:{pid}-{mid}, status: {response.status_code}")
    else:
        # create
        url = "https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/products/{pid}/metafields.json".format(
            **locals()
        )
        meta = {
            "metafield": {
                "namespace": "shirai",
                "key": "myreviews",
                "value": reviews,
                "value_type": "string"
            }
        }
        response = requests.post(
            url, data=json.dumps(meta), headers={"Content-Type": "application/json"}
        )
        print(f"created: {pid}, status: {response.status_code}")


dpath = f"{SHOP_DOMAIN}/admin/api/2020-07"
def get_mid_reviews():
    files = [entry.path for entry in os.scandir("data/ld_json") if entry.is_file()] 
    for file in files:
        if match := re.findall(r"\d+", file):
            yield {"pid": match[0], "reviews": (open(file, "r").read())}
    #reviews = json.load(open(f"data/products/reviews_{pid}.json", "r"))

for product in get_mid_reviews():
    print(product['pid'])
    upsertMetaInProduct(product['pid'], SHOPIFY_USER, SHOPIFY_PW, dpath, product['reviews'])
    time.sleep(2)

