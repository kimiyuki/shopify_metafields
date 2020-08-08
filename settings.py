from dotenv import load_dotenv
load_dotenv()
import os

JUDGEME_TOKEN= os.getenv("JUDGEME_TOKEN")
JUDGEME_DOMAIN= os.getenv("JUDGEME_DOMAIN")
SHOPIFY_USER= os.getenv("SHOPIFY_USER")
SHOPIFY_PW= os.getenv("SHOPIFY_PW")
SHOP_DOMAIN=os.getenv("SHOP_DOMAIN")