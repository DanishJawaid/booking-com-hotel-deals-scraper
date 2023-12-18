from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BookingFiltration:
    def __init__(self,driver:WebDriver):
        self.driver=driver

    def select_property_rating(self,*star_values):

        partial_id='filter_group_class_:'
        property_rating_box= self.driver.find_element(By.CSS_SELECTOR, f"[id*='{partial_id}']")
        select_stars=property_rating_box.find_elements(By.CLASS_NAME,'bf862b4098')

        for box in select_stars:
            for star in star_values:
                if (str(star)+' star') in box.text:
                    box.click()


    def lowest_prices(self):
        sort_by_button=self.driver.find_element(By.CSS_SELECTOR,'button[data-testid="sorters-dropdown-trigger"]')
        sort_by_button.click()
        lowest_prices_button=self.driver.find_element(By.CSS_SELECTOR,'button[data-id="price"]')
        lowest_prices_button.click()