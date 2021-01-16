from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def get_data_link(option, _inner_container):
    option.click()

    # Get download link
    time.sleep(3)
    download_btn = _inner_container.find_element_by_css_selector("a.button.rounded.download-language")
    return [option.text, download_btn.get_attribute('href')]


data_site = "https://commonvoice.mozilla.org/en/datasets"

options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                          options=options)

driver.get(data_site)

# Clicks on appropriate buttons to start retrieving download links
inner_container = driver.find_element_by_css_selector("div.inner")
email_download_btn = inner_container.find_element_by_css_selector("button.button.rounded.show-email-form")
driver.execute_script("arguments[0].click()", email_download_btn)

confirm_size = inner_container.find_element_by_css_selector("input[name='confirmSize']")
driver.execute_script("arguments[0].click()", confirm_size)

email_input = inner_container.find_element_by_css_selector("label.labeled-form-control.for-input")
email_input.send_keys("lit1@ufl.edu")

confirm_no_identify = inner_container.find_element_by_css_selector("input[name='confirmNoIdentify']")
driver.execute_script("arguments[0].click()", confirm_no_identify)

# Find options to iterate through
select = driver.find_element_by_css_selector("select[name='bundleLocale']")
options = select.find_elements_by_css_selector("option")

# Get download links for each option
data_links = [get_data_link(option, inner_container) for option in options]

df = pd.DataFrame(data_links, columns=["Language", "Data Link"])
df.to_csv('data_links.csv')
