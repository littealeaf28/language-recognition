from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def get_size_mb(_driver):
    facts_container = _driver.find_element_by_css_selector("ul.facts")
    facts_elements = facts_container.find_elements_by_css_selector("li")
    size_container = facts_elements[1].find_element_by_css_selector("span.value")

    size = size_container.text
    size_val = int(size[:-3])

    if size[-2:] == "GB":
        return size_val * 1000
    else:
        return size_val


def get_data_link(option, _inner_container, _driver):
    option.click()

    print(f'Processing {option.text}...')

    # Get listed size
    size_mb = get_size_mb(_driver)

    # Get download link
    time.sleep(3)
    download_btn = _inner_container.find_element_by_css_selector("a.button.rounded.download-language")

    return [option.text, size_mb, download_btn.get_attribute('href'), False]


data_site = "https://commonvoice.mozilla.org/en/datasets"

options = Options()
options.add_argument("--headless")
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
data_links = [get_data_link(option, inner_container, driver) for option in options]
# data_links = [get_data_link(option, inner_container, driver) for idx, option in enumerate(options) if idx < 3]

df = pd.DataFrame(data_links, columns=["Language", "Size (MB)", "Data Link", "Downloaded"])
df.to_csv('data_links.csv', index=False)

print('Finished saving links')

driver.quit()
