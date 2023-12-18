import time
from datetime import datetime, timedelta
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from booking import constants
from selenium.webdriver.common.by import By
from booking.booking_filtration import BookingFiltration


class Booking(webdriver.Chrome):
    def __init__(self,driver_path=ChromeDriverManager().install(),teardown=False):
        self.driver_path=driver_path
        self.teardown=teardown
        os.environ['PATH']+=self.driver_path
        options=webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        super(Booking,self).__init__(options=options)
        self.implicitly_wait(5)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(constants.BASE_URL)

    def change_currency(self,currency='USD'):
        currency_button = self.find_element(By.CLASS_NAME, 'e4adce92df')
        currency_button.click()
        currency_selectors = self.find_elements(By.CLASS_NAME, 'ac7953442b')
        for currency_selector in currency_selectors:
            if currency.lower() in currency_selector.text.lower().split():
                currency_selector.click()
                return True
        close=self.find_element(By.CSS_SELECTOR,'button[aria-label="Close currency selector"]')
        close.click()
        return False


    def check_place_to_go(self):
        try:
            first_option = self.find_element(By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]')
            return True
        except:
            return False

    def select_place_to_go(self,location):
        where = self.find_element(By.CSS_SELECTOR, 'input[placeholder="Where are you going?"]')
        where.clear()
        where.send_keys(location)


    def click_place_to_go(self):
        first_option = self.find_element(By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]')
        first_option.click()

    def calculate_month_difference(self,check_date):
        # Convert input string to datetime object
        input_date = datetime.strptime(check_date, '%Y-%m-%d')

        # Retrieve current date
        current_date = datetime.now()

        # Calculate the difference in months
        month_difference = (input_date.year - current_date.year) * 12 + (input_date.month - current_date.month)

        # Get the absolute value in case the input date is in the past
        month_difference = abs(month_difference)

        next_month=self.find_element(By.CLASS_NAME,'f073249358')
        for i in range(month_difference):
            next_month.click()
            time.sleep(1)

    def check_date_past(self, check_in_date, check_out_date):
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()

        # Get the current date
        current_date = datetime.now().date()

        # Calculate yesterday's date
        yesterday_date = current_date - timedelta(days=1)

        # Check if the input date is yesterday or earlier
        if check_in <= yesterday_date or check_out<=yesterday_date:
            print('Can not select past dates')
            return False
        else:
            return True

    def check_date_future(self, check_in_date, check_out_date):
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()

        # Get the current date
        current_date = datetime.now().date()

        # Calculate yesterday's date
        future_date = current_date + timedelta(days=365)

        # Check if the input date is yesterday or earlier
        if check_in >= future_date or check_out>=future_date:
            print('Can not make booking more than 1 year in advance')
            return False
        else:
            return True

    def check_date_sequence(self, check_in_date, check_out_date):
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d')

        # Check if the input date is yesterday or earlier
        if check_out <= check_in:
            print('Check in should be before check out')
            return False
        else:
            return True

    def check_days_difference(self, check_in_date, check_out_date):
        # Convert input strings to datetime objects
        start_date = datetime.strptime(check_in_date, '%Y-%m-%d')
        end_date = datetime.strptime(check_out_date, '%Y-%m-%d')

        # Calculate the difference in days
        date_difference = (end_date - start_date).days

        # Check if the difference is more than 90 days
        if date_difference > 90:
            print("Sorry, reservations for more than 90 nights aren't possible.")
            return False
        else:
            return True

    def select_date(self, check_in_date, check_out_date):

        self.calculate_month_difference(check_in_date)
        check_in_date_selector = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
        check_in_date_selector.click()
        self.calculate_month_difference(check_out_date)
        check_out_date_selector = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
        check_out_date_selector.click()

    def search(self):
        search_selector=self.find_element(By.CLASS_NAME,'cceeb8986b')
        search_selector.click()

    def setpeople(self,adults=1):

        #select people dropdown
        people_selector = self.find_element(By.CSS_SELECTOR, 'span[data-testid="searchbox-form-button-icon"]')
        people_selector.click()

        #find plus minus adults
        adult_minus = self.find_element(By.CLASS_NAME, 'e91c91fa93')
        adult_plus = self.find_element(By.CLASS_NAME, 'f4d78af12a')


        while True:

            number_of_adults = int(self.find_element(By.CLASS_NAME, 'd723d73d5f').text)

            if number_of_adults>adults:
                adult_minus.click()
            elif number_of_adults<adults:
                adult_plus.click()
            else:
                break


        # people_done=self.find_element(By.CLASS_NAME,'e4adce92df')
        # people_done.click()


    def apply_filtration(self):
        filtration=BookingFiltration(driver=self)

        filtration.lowest_prices()
        filtration.select_property_rating(3,4)


    def get_info(self,number_of_results=20):
        hotel_names=[]
        hotel_ratings=[]
        hotel_prices=[]
        hotel_reviews=[]

        while True:
            time.sleep(5)
            hotel_name,hotel_rating,hotel_price,hotel_review=self.extract_info()

            hotel_names.extend(hotel_name)
            hotel_ratings.extend(hotel_rating)
            hotel_prices.extend(hotel_price)
            hotel_reviews.extend(hotel_review)
            print(len(hotel_names))

            if len(hotel_ratings)>number_of_results:
                break

            #find next page
            try:
                next_page_button=self.find_element(By.CSS_SELECTOR,'button[aria-label="Next page"]')
            except:
                break
            next_page_button.click()


        hotel_details=[[i for i in range(1, len(hotel_names)+1)],hotel_names,hotel_ratings,hotel_reviews,hotel_prices]
        hotel_details = [list(row) for row in zip(*hotel_details)]
        hotel_details=hotel_details[:number_of_results]
        hotel_details.insert(0,['Number','Hotel Names','Hotel Ratings','Number of Reviews','Hotel Prices'])
        return hotel_details

    def close_popup(self,type,close_element):
        try:
            if type=='class':
                close_popup = self.find_element(By.CLASS_NAME, close_element)
            elif type=='id':
                close_popup = self.find_element(By.ID, close_element)

            close_popup.click()

        except:
            pass

    def extract_info(self):

        hotel_names = []
        hotel_ratings = []
        hotel_prices = []
        hotel_reviews = []

        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        property_cards = self.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        for property_card in property_cards:

            # hotel name
            try:
                hotel_name = property_card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text

            except:
                hotel_name = 'name error'


            # hotel rating
            try:
                hotel_rating = property_card.find_element(By.CSS_SELECTOR, 'div[aria-label*="Scored"]').text

            except:
                try:
                    hotel_rating = property_card.find_element(By.CSS_SELECTOR, 'div[aria-label="Exceptional"]').text

                except:
                    hotel_rating = 'unrated'

            # hotel price
            try:
                hotel_price = property_card.find_element(By.CSS_SELECTOR,'span[data-testid*="discounted-price"]').text

            except:
                hotel_price='cant find price'

            # hotel reviews
            try:
                hotel_review=property_card.find_element(By.CLASS_NAME,'d935416c47').text
            except:
                hotel_review='no review'

            hotel_names.append(hotel_name)
            hotel_ratings.append(hotel_rating)
            hotel_prices.append(hotel_price)
            hotel_reviews.append(hotel_review)


        return hotel_names,hotel_ratings,hotel_prices,hotel_reviews