import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pprint
import csv

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('^https://www.amazon.com/acer-Chromebook-Plus-Laptop-Google/dp/B0CX28KX1N/ref=sr_1_1_sspa?crid=OFZFV8HT9BTC^&dib=eyJ2IjoiMSJ9.fIWDkDG_dBxqFi8DwUMyw81lh9hU4SJEEnDBfIlL6FlovTASoD4YLwn98bbXz-t0tu8rUUMVOKtaNk2QmhcbYe_rXjPWo8jYybNDJKhvNnNr0uEoiTiWMgjkUUVEFYU0Li4D-CVj5YC6xFX2EcRcxGeiLIvYGo-oYcUBkxuYs8eX_DkMI4ok0gHBVZMAfzM8ZUCXmeh_zDK4VDpI-kfITvwd-pys3kqCe8E1zUbImGo.kZfI1OUGxYbUKN0HmTnim4qRsGY76v4I9vo_TI6pwvE^&dib_tag=se^&keywords=ordinateur^&qid=1740868218^&sprefix=ordinat^%^2Caps^%^2C542^&sr=8-1-spons^&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY^&th=1^', headers=headers, cookies=cookies)


class AmazonProduct:
    def __init__(self, output_file="products.csv"):
        self.header = {
            '^accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7^',
            '^accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7^',
            '^cache-control': 'max-age=0^',
            '^device-memory': '8^',
            '^downlink': '10^',
            '^dpr': '1^',
            '^ect': '4g^',
            '^priority': 'u=0, i^',
            '^referer': 'https://www.amazon.com/s?k=ordinateur^&crid=OFZFV8HT9BTC^&sprefix=ordinat^%^2Caps^%^2C542^&ref=nb_sb_ss_ts-doa-p_5_7^',
            '^rtt': '150^',
            '^sec-ch-device-memory': '8^',
            '^sec-ch-dpr': '1^',
            '^sec-ch-ua': '^\\^Not(A:Brand^\\^;v=^\\^99^\\^, ^\\^Google',
            '^sec-ch-ua-mobile': '?0^',
            '^sec-ch-ua-platform': '^\\^Windows^\\^^',
            '^sec-ch-ua-platform-version': '^\\^10.0.0^\\^^',
            '^sec-ch-viewport-width': '1366^',
            '^sec-fetch-dest': 'document^',
            '^sec-fetch-mode': 'navigate^',
            '^sec-fetch-site': 'same-origin^',
            '^sec-fetch-user': '?1^',
            '^upgrade-insecure-requests': '1^',
            '^user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36^',
            '^viewport-width': '1366^',
        }
        self.output_file = output_file
        self.initialize_csv()

    def initialize_csv(self):
        """Crée le fichier CSV avec les en-têtes s'il n'existe pas encore."""
        try:
            with open(self.output_file, mode='x', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["product_url", "product_title", "price", "product_rating",
                                 "nb_reviews", "nb_bought", "hard_size", "cpu_model"])
        except FileExistsError:
            pass

    mozila = webdriver.Firefox(),

    def get_urls(self, driver=mozila, nb_products=100):
        """_description_
        Args:
            driver (webdriver/selenium): votre connecteur a selenium pour aller sur le site
            search_term (str): le terme de recherche dans notre cas c'est "Ordinateur Portable"
            nb_products (int): le nombre de produits qu'on veut extraire. Par defaut c'est 100
        Returns:
            nb_linsk (list): retourne une liste des liens des products qui sont sur la page
        """
        # Configuration de WebDriver (remplace le chemin par celui de ton WebDriver)

        # Ouvrir Amazon
        driver.get("https://www.amazon.fr")

        # Rechercher un produit (remplace "ordinateur portable" par ton terme de recherche)
        search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        search_box.send_keys("ordinateur portable")
        search_box.send_keys(Keys.RETURN)

        # Attendre que la page se charge
        time.sleep(30)

        # Liste pour stocker les liens des produits
        product_links = []

        # Boucle pour extraire les liens des produits
        while len(product_links) < nb_products:
            # Trouver tous les éléments de produits sur la page
            products = driver.find_elements(By.CLASS_NAME, "a-link-normal")

            # Extraire les liens et les ajouter à la liste
            for product in products:
                link = product.get_attribute("href")
                if link not in product_links:
                    product_links.append(link)
                    if len(product_links) >= nb_products:
                        break

            # Passer à la page suivante si on n'a pas encore 100 liens
            if len(product_links) < nb_products:
                next_button = driver.find_element(
                    By.CLASS_NAME, "s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator")
                next_button.click()
                time.sleep(30)  # Attendre que la page se charge

        # Fermer le navigateur
        driver.quit()

        return product_links

    def get_product_title(self, soup):
        try:
            title = soup.find(
                "span", attrs={"id": "productTitle"}).get_text().strip()
            return title
        except:
            return None

    def get_product_price(self, soup):
        try:
            price = soup.find(
                "span", {"class": "a-price-whole"}).get_text().strip()
            return float(price)
        except:
            return None

    def get_product_rating(self, soup):
        div_avg = soup.find("div", {"id": "averageCustomerReviews"})
        if div_avg is not None:
            rating = div_avg.find(
                "span", {"class": "a-icon-alt"}).get_text().split(" ")[0]
            return float(rating)
        else:
            return None

    def get_number_reviews(self, soup):
        try:
            nb_reviews = soup.find(
                "span", {"id": "acrCustomerReviewText"}).get_text().split(" ")[0]
            return int(nb_reviews)
        except:
            return None

    def get_number_of_bought_per_month(self, soup):
        try:
            div_bought = soup.find(
                "div", {"class": "a-section a-spacing-micro social-proofing-faceout"})
            if div_bought is not None:
                nb_bought = div_bought.find(
                    "span", {"class": "a-text-bold"}).get_text().split(" ")[0]
                return nb_bought

            else:
                return None
        except:
            return None

    def get_hard_size(self, soup):
        try:
            div_caracter = soup.find(
                'div', {'class': 'a-section a-spacing-small a-spacing-top-small'})
            if div_caracter is not None:
                caracter = div_caracter.find(
                    'tr', {'class': 'a-spacing-small po-hard_disk.size'})
                hard_size = caracter.get_text().strip()
                return hard_size
            else:
                return None
        except:
            return None

    def get_pcu(self, soup):
        div_caracter = soup.find(
            'div', {'class': 'a-section a-spacing-small a-spacing-top-small'})
        if div_caracter is not None:
            caracter = div_caracter.find(
                'tr', {'class': 'a-spacing-small po-cpu_model.family'})
            cpu_moel = caracter.get_text().strip()
            return cpu_moel
        else:
            return None

    def get_product_data(self, product_url):
        response = requests.get(product_url, headers=self.header)
        if response.status_code == 200:
            soup = bs(response.content, 'html.parser')
            product_title = self.get_product_title(soup)
            # product_rating = self.get_product_rating(soup)
            # nb_reviews = self.get_number_reviews(soup)
            # nb_bought = self.get_number_of_bought_per_month(soup)
            # cpu_model = self.get_pcu(soup)
            # hard_size = self.get_hard_size(soup)
            # price = self.get_product_price(soup)
            return {
                "product_url": product_url,
                "product_title": product_title,
                # "price": price,
                # "product_rating": product_rating,
                # "nb_reviews": nb_reviews,
                # "nb_bought": nb_bought,
                # "hard_size": hard_size,
                # "cpu_model": cpu_model
            }

        else:
            return None

    def save_to_csv(self, data):
        """Ajoute les données d'un produit au fichier CSV."""
        if data:
            with open(self.output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["product_url", "product_title", "price",
                                                          "product_rating", "nb_reviews",                 "nb_bought", "hard_size", "cpu_model"])
                writer.writerow(data)

    def scrap_url(self, product_urls):
        for url in product_urls:
            product_data = self.get_product_data(url)
            # self.save_to_csv(product_data)
            pprint.pprint(product_data)
            print("==========================================================")
            return f"\n================================File product data has been created================================\n"
