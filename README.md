# judge.me reviews for upsert to metafields

1. get my site's reviews from Judge.me.
2. group reveiws by product and write those in json format.
3. transform the json to ld+json format for the microdata for SEO.
4. upsert ld+json data as metafields data to each product.
5. (not here) edit the liquid code(might be microdata.liquid file).

It requires to 
 - write .env file for your environment. 
 - set up your private app. https://help.shopify.com/en/manual/apps/private-apps
