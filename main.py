import csv
import json
from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from time import sleep


class Korepetycje:
    def __init__(self):
        self.base_url = "https://www.e-korepetycje.net"
        self.url = "https://www.e-korepetycje.net/przedmioty"
        self.rating = ""
        self.address = ""
        self.phone_number = ""
        self.proxies_list = [
            ['198.71.49.163', '3128'],
            ['95.164.11.227', '8000'],
            ['199.168.148.131', '10105'],
            ['67.43.228.250', '5285'],
            ['135.125.239.212', '3128'],
            ['50.84.107.94', '8111'],
            ['142.132.234.228', '8888'],
            ['51.210.183.2', '3128'],
            ['139.180.39.200', '8080'],
            ['51.38.230.146', '443'],
            ['104.236.195.60', '10009'],
            ['212.92.23.235', '31288'],
            ['67.43.227.227', '16609'],
            ['37.120.187.59', '80'],
            ['199.188.93.217', '8000'],
            ['138.197.20.244', '10003'],
            ['67.43.227.228', '18443'],
            ['181.66.181.52', '999'],
            ['20.79.103.91', '80'],
            ['64.189.106.6', '3129'],
            ['41.33.203.234', '1975'],
            ['20.44.189.184', '3129'],
            ['192.162.69.116', '80'],
            ['41.65.236.37', '1981'],
            ['154.236.191.42', '1976'],
            ['132.248.159.223', '3128'],
            ['154.236.191.49', '1981'],
            ['142.93.72.28', '10004'],
            ['165.225.205.14', '10006'],
            ['191.243.47.206', '8080'],
            ['38.172.128.208', '999'],
            ['20.219.177.38', '3129'],
            ['20.204.214.79', '3129'],
            ['20.219.178.121', '3129'],
            ['67.43.227.228', '29187']
        ]

    def main(self):

        res = requests.get(url=self.url)

        soup = BeautifulSoup(res.text, "html.parser")

        container_of_list = soup.find('div', class_="content-wrapper")

        list_of_links_of_categories = container_of_list.findAll('div', class_="home-pop-single")

        print(len(list_of_links_of_categories))

        for link_of_category_element in list_of_links_of_categories:
            category_detail = {
                "link": link_of_category_element.find("a").get("href"),
                "total_results": link_of_category_element.find("span", class_="home-pop-nr").text.replace("(",
                                                                                                          "").replace(
                    ")", "")
            }

            self.getCategory(category_detail)

    def getCategory(self, category_detail):
        pages = int(int(category_detail["total_results"]) / 30) + 1
        link = f"{self.base_url}{category_detail['link']}"
        print(pages, link)
        i = 1
        while i <= pages:
            res = requests.get(f"{link}?p={i}")
            soup = BeautifulSoup(res.text, "html.parser")
            h3_tags = soup.findAll("h3")
            print(len(h3_tags))

            for index, h3_tag in enumerate(h3_tags):

                if index > 0:
                    self.getProfileData(url=h3_tag.findNext("a").get("href"))
            i = i + 1

    def getProfileData(self, url):

        res = requests.get(url)

        soup = BeautifulSoup(res.text, "html.parser")

        price = self.getPrice(soup)

        name = soup.find("h2", class_="xxs-hidden").text

        category = url.split("/")[-1]

        if soup.find("span", class_="rate"):

            self.rating = soup.find("span", class_="rate").text

            print(self.rating)
        else:
            if soup.find("span", class_="ratingValue"):

                self.rating = soup.find("span", class_="ratingValue").text

                print(self.rating)
            else:
                self.rating = "N/A"

        locations_divs = soup.findAll("div", class_="feat-city")

        locations = []

        for location in locations_divs:
            locations.append(location.text)
        if soup.find("div", class_="address-column"):
            address_div = soup.find("div", class_="address-column")
            self.address = address_div.text
        else:
            self.address = "N/A"
        phone_number = self.getPhoneNumber(url)

        print(phone_number)
        # print(phone_number)

        data = {
            "Link": url,
            "Name": name,
            "Category": category,
            "Price": price,
            "Rating": self.rating,
            "Locations": locations,
            "Address": self.address,
            "Phone Number": phone_number
        }
        print(data)
        self.write_data_to_csv(data)

    @staticmethod
    def getPrice(soup):

        price_of_teacher_main_span = soup.find("span", class_="cost")

        price_of_teacher_spans = price_of_teacher_main_span.find_all("span")

        last_part_of_price = price_of_teacher_spans[-1].text

        first_part_of_price = price_of_teacher_spans[0].text

        return first_part_of_price + last_part_of_price

    def getPhoneNumber(self, url):

        global phone_number
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        privacy_button_tab_container = driver.find_element(By.CLASS_NAME, "cc-nb-buttons-container")

        if privacy_button_tab_container.find_element(By.TAG_NAME, "button"):
            privacy_button_tab_container.find_element(By.TAG_NAME, "button").click()
        try:
            show_me_number_button = driver.find_element(By.CLASS_NAME, "dip")
            if show_me_number_button:
                show_me_number_button.click()

            sleep(5)
            phone_number_container = driver.find_element(By.CLASS_NAME, "contact-data")
            if phone_number_container:
                phone_number = phone_number_container.find_element(By.TAG_NAME, "div").text

            return phone_number
        except:
            return "N/A"

    # def getPhoneNumber(self, soup):
    #
    #     global data_dip, data_pid, data_dim
    #     phone_number_button = soup.find("button", class_="dip")
    #     if phone_number_button:
    #         data_dip = phone_number_button.get("data-dip")
    #         data_pid = phone_number_button.get("data-pid")
    #         data_dim = phone_number_button.get("data-dim")
    #         print(data_dip, data_pid, data_dim)
    #
    #     headers = {
    #         # "Cache-Control": "no-store, no-cache, must-revalidate",
    #         # "Connection": "keep-alive",
    #         # "Content-Encoding": "gzip",
    #         # "Content-Type": "text/html; charset=utf-8",
    #         # "Accept": "*/*",
    #         # "Accept-Encoding": "gzip, deflate, br",
    #         # "Accept-Language": "en-US,en;q=0.9",
    #
    #         # "Cookie": "cookie_consent_level=%7B%22strictly-necessary%22%3Atrue%2C%22functionality%22%3Atrue%7D; _pbjs_userid_consent_data=6683316680106290; _sharedID=1140516c-d392-42fe-8bf4-82317e9b3c93; cookie_consent_user_consent_token=7cgaPEngxWh3; cookie_consent_user_accepted=true; _ga_JEEE5Y37TD=GS1.1.1703966815.14.1.1703966828.47.0.0; _ga=GA1.2.930577901.1702668784; _fbp=fb.1.1702668784642.1544273837; _cc_id=906847e4bda5352e3dfcc5bac6018f79; cto_bundle=1JL0Al9XZTMlMkJMNU1nVFB6UlAzOXV3MkIzSld2VWtSNGhDZ0tXNGE3Z1JUcEtOYVRGeHkl…7B%22TDID%22%3A%22e4d20dbe-752d-4e68-9aae-33036264f42d%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-12-16T18%3A36%3A55%22%7D; uids=a%3A1%3A%7Bi%3A0%3Bs%3A6%3A%22534324%22%3B%7D; PHPSESSID=m7u6vareu7umgtr9ivdhkk77o2; adc=%7B%221870%22%3A3%2C%221740%22%3A1%7D; __oagr=true; _gid=GA1.2.419567565.1703963310; sh=568dd6d6301a9d5e6152f2072c7ae652; panoramaId_expiry=1704568142875; panoramaId=c3a52f73619c72ce03a8f716bc09185ca02c6e4410682205f6fa9f3cb5fd6506; panoramaIdType=panoDevice; _gat=1",
    #
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    #     }
    #
    #     url = "https://www.e-korepetycje.net/request?mod=dip"
    #
    #     payload = {
    #         'dip': data_dip,
    #         'pid': data_pid,
    #         'dim': data_dim
    #     }
    #
    #     for proxy in self.proxies_list:
    #         proxy_url = f"http://{proxy[0]}:{proxy[1]}"
    #         # proxy_url2 = f"https://{proxy.txt['ip']}:{proxy.txt['port']}"
    #
    #         proxies = {'https': proxy_url}
    #         print(proxies)
    #         try:
    #             # Send POST request with the specified proxy.txt and headers
    #             response = requests.post(url, data=payload, headers=headers, proxies=proxies, verify=False)
    #             try:
    #                 if response.text.split('"')[-2]:
    #                     return response.text.split('"')[-2]
    #                 else:
    #                     return "N/A"
    #             except:
    #                 pass
    #             # Print the proxy.txt details and response
    #             print(f"Proxy: {proxy_url}")
    #             print(f"Status Code: {response.status_code}")
    #             print(f"Response: {response.text}\n")
    #         except RequestException as e:
    #             print(f"Error with proxy.txt {proxy_url}: {e}\n")
    #
    #         # response = requests.post(url=url, data=payload, headers=headers, proxies=proxies, verify=False)

    @staticmethod
    def write_data_to_csv(data, unique_links=set()):
        # Specify the field names (header) for the CSV file
        csv_file_name = "output.csv"
        field_names = ["Link", "Name", "Category", "Price", "Rating", "Locations", "Address", "Phone Number"]

        data["Locations"] = "\n".join(data["Locations"])
        # Open the CSV file in append mode

        link = data["Link"]

        # Check if the link is not already in the set of unique links
        if link not in unique_links:
            with open(csv_file_name, mode='a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)

                # If the file is empty, write the header
                if csv_file.tell() == 0:
                    csv_writer.writeheader()

                # Write the data to the CSV file
                csv_writer.writerow(data)

            print(f'Data for link {link} has been written to {csv_file_name}')

            # Add the link to the set of unique links
            unique_links.add(link)
        else:
            print(f'Data for link {link} already exists and will not be written to {csv_file_name}')


if __name__ == "__main__":
    bot = Korepetycje()
    bot.main()
    # bot.getProfileData("https://www.e-korepetycje.net/miczar/administracja")
