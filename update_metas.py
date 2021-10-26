from settings import SHOPIFY_PW, SHOPIFY_USER, SHOP_DOMAIN
import settings
import requests
import json
import logging
import http
import os
import re
import time

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
req_log = logging.getLogger("requests.packages.urllib3")
req_log.setLevel(logging.ERROR)
req_log.propagate = True


def upsertMetaInProduct(pid, dpath, reviews):
    url = f"https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/products/{pid}/metafields.json"
    print(url)
    response = requests.get(url)
    r = response.json()
    if 'metafields' not in r:
        _create_reviews_meta(pid, reviews)
    else:
        myreviews = list(filter(lambda x: x['namespace'] == "shirai" and x['key'] == "myreviews", r['metafields']))
        if len(myreviews) == 0:
            _create_reviews_meta(pid, reviews)
        else:
            mid = myreviews[0]['id']
            _update_reviews_meta(pid, mid, reviews)


def _create_reviews_meta(pid, reviews):
    # create
    url = f"https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/products/{pid}/metafields.json"
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


def _update_reviews_meta(pid, mid, reviews):
    # update
    print(f"update {mid}")
    url = f"https://{SHOPIFY_USER}:{SHOPIFY_PW}@{dpath}/products/{pid}/metafields/{mid}.json"
    meta = {"metafield": {
        "id": mid,
        "value": reviews,
        "value_type": "string"}}
    response = requests.put(
        url, data=json.dumps(meta), headers={"Content-Type": "application/json"}
    )
    print(f"udpate:{pid}-{mid}, status: {response.status_code}")


dpath = f"{SHOP_DOMAIN}/admin/api/2021-10"


def get_mid_reviews():
    files = [entry.path for entry in os.scandir("data/ld_json") if entry.is_file()]
    for file in files:
        if match := re.findall(r"\d+", file):
            yield {"pid": match[0], "reviews": (open(file, "r").read())}
    #reviews = json.load(open(f"data/products/reviews_{pid}.json", "r"))


for product in get_mid_reviews():
    print(product['pid'])
    upsertMetaInProduct(product['pid'], dpath, product['reviews'])
    time.sleep(2)
