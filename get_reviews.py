import requests
import json
from itertools import groupby
from functools import reduce
from datetime import datetime as dt
import pytz
import os
import re
from settings import JUDGEME_DOMAIN, JUDGEME_TOKEN

def retrieve_judgeme(JUDGEME_TOKEN, JUDGEME_DOMAIN):
  reviews = []
  idx = 1
  while idx < 50:
    url = "https://judge.me/api/v1/reviews?api_token={JUDGEME_TOKEN}&shop_domain={JUDGEME_DOMAIN}&page={idx}".format( **locals())
    print(f"page:{idx}")
    response = requests.get(url)
    r = response.json()
    reviews += r['reviews']
    if(int(r['per_page']) != len(r['reviews'])):
      print(f"break at {r['current_page']}")
      break 
    idx = idx + 1

  #while idx < 50 or 
  with open("data/reviews.json", "w") as f:
    json.dump([x for x in reviews if x['curated'] != 'spam'],
               f, indent=2, ensure_ascii=False)

  str_prd = "product_external_id"
  j = json.load(open("data/reviews.json", "r"))
  j.sort(key=lambda x: x[str_prd])
  jj = groupby(j, key=lambda x: x[str_prd])
  for k, g in jj:
    with open("data/products/reviews_{}.json".format(k), "w") as f:
      json.dump(list(g), f, indent=2, ensure_ascii=False)

def write_ld_json(pid):
  ld_reviews = []
  reviews = json.load(open(f"data/products/reviews_{pid}.json"))
  count_rating = len(reviews)
  agg_rating = reduce(lambda acc, cur: acc + cur["rating"], reviews, 0) / count_rating
  jst = pytz.timezone("Japan")
  r = reviews[0]
  for r in reviews:
      ld_review = {
          "@type": "Review",
          "name": r["title"],
          "author": {
            "@type": "Person",
            "name": r["reviewer"]["name"]
          },
          "datePublished": dt.strptime(r["updated_at"], "%Y-%m-%dT%H:%M:%S+00:00")
          .replace(tzinfo=jst)
          .strftime("%Y-%m-%d"),
          "description": r["body"],
          "reviewRating": {
              "@type": "Rating",
              "bestRating": 5,
              "ratingValue": r["rating"],
              "worstRating": 1,
          },
      }
      ld_reviews.append(ld_review)

  ld_json = {
      "@context": "http://schema.org",
      "@type": "Product",
      "@id": f"https://fukushima-ichiba.com/products/{reviews[0]['product_handle']}#product",
      "name": reviews[0]["product_title"],
      "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": agg_rating,
          "reviewCount": count_rating,
      },
      "reviews": ld_reviews,
  }
  with open(f"data/ld_json/{pid}.json", "w") as f:
    json.dump(ld_json, f)


def write_for_files(files):
  for file in files:
      if match := re.findall(r"\d+", file):
        yield match[0]


retrieve_judgeme(JUDGEME_TOKEN, JUDGEME_DOMAIN)
files = [entry.path for entry in os.scandir("data/products") if entry.is_file()] 
for pid in write_for_files(files):
  print(f"write {pid}")
  write_ld_json(pid)
