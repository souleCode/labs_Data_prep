
from AmazonProduct import AmazonProduct
import pprint


# Maintenant, je vais ouvrir chaque lien et extraire les informations du produit
# eessaiee avec un seul lien

product_urls = "https://www.amazon.com/acer-Chromebook-Plus-Laptop-Google/dp/B0CX28KX1N/ref=sr_1_1_sspa?crid=OFZFV8HT9BTC&dib=eyJ2IjoiMSJ9.fIWDkDG_dBxqFi8DwUMyw81lh9hU4SJEEnDBfIlL6FlovTASoD4YLwn98bbXz-t0tu8rUUMVOKtaNk2QmhcbYe_rXjPWo8jYybNDJKhvNnNr0uEoiTiWMgjkUUVEFYU0Li4D-CVj5YC6xFX2EcRcxGeiLIvYGo-oYcUBkxuYs8eX_DkMI4ok0gHBVZMAfzM8ZUCXmeh_zDK4VDpI-kfITvwd-pys3kqCe8E1zUbImGo.kZfI1OUGxYbUKN0HmTnim4qRsGY76v4I9vo_TI6pwvE&dib_tag=se&keywords=ordinateur&qid=1740868218&sprefix=ordinat%2Caps%2C542&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"

bot = AmazonProduct()
product_data = bot.get_product_data(product_urls)
pprint.pprint(product_data)
# list_urls = bot.get_urls(nb_products=3)
# print(type(list_urls), len(list_urls))
# print(list_urls)
# bot.scrap_url(product_urls)
