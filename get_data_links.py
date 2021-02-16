from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re


def fill_form_to_download(_driver, _inner_container):
    email_download_btn = _inner_container.find_element_by_css_selector("button.button.rounded.show-email-form")
    _driver.execute_script("arguments[0].click()", email_download_btn)

    email_input = _inner_container.find_element_by_css_selector("input#download-email")
    email_input.send_keys("lit1@ufl.edu")

    time.sleep(1)   # Wait for email download button to be clicked before continuing
    confirm_size = _inner_container.find_element_by_css_selector("input[name='confirmSize']")
    _driver.execute_script("arguments[0].click()", confirm_size)

    time.sleep(1)   # Wait for confirm size to be clicked before continuing
    confirm_no_identify = _inner_container.find_element_by_css_selector("input[name='confirmNoIdentify']")
    _driver.execute_script("arguments[0].click()", confirm_no_identify)


def get_lang_data_size_mb(_driver):
    facts_container = _driver.find_element_by_css_selector("ul.facts")
    facts_elements = facts_container.find_elements_by_css_selector("li")
    size_container = facts_elements[1].find_element_by_css_selector("span.value")

    size = size_container.text
    size_val = int(size[:-3])

    return size_val * 1000 if size[-2:] == "GB" else size_val


def get_lang_data(_lang_option, _inner_container, _driver):
    _lang_option.click()

    print(f'Processing {_lang_option.text}...')

    size_mb = get_lang_data_size_mb(_driver)

    time.sleep(1)   # Wait for data_link
    download_btn = _inner_container.find_element_by_css_selector("a.button.rounded.download-language")
    data_link = download_btn.get_attribute('href')

    matches = re.findall("\/(.*?)\.", data_link)
    label = matches[2]

    return [_lang_option.text, size_mb, data_link, label, False]


def get_data_link(_option, _inner_container):
    _option.click()

    print(f'Processing {_option.text}...')

    time.sleep(1)
    download_btn = _inner_container.find_element_by_css_selector("a.button.rounded.download-language")

    return download_btn.get_attribute('href')


def init_data_links(_lang_options, _inner_container, _driver):
    data_links = [get_lang_data(lang_option, _inner_container, _driver) for lang_option in _lang_options]

    return pd.DataFrame(data_links, columns=["Language", "Size (MB)", "Data Link", "Label", "Downloaded"])


def update_data_links(_lang_options, _inner_container):
    _df = pd.read_csv('data_links.csv')

    # Update download links since they expire
    for idx, lang_option in enumerate(_lang_options):
        if ~_df.iloc[idx].loc['Downloaded']:
            _df.loc[idx, 'Data Link'] = get_data_link(lang_option, _inner_container)

    return _df


data_site = "https://commonvoice.mozilla.org/en/datasets"

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

driver.get(data_site)

inner_container = driver.find_element_by_css_selector("div.inner")
fill_form_to_download(driver, inner_container)

# Find language options to iterate through
select = driver.find_element_by_css_selector("select[name='bundleLocale']")
lang_options = select.find_elements_by_css_selector("option")

# df = init_data_links(lang_options, inner_container, driver)
df = update_data_links(lang_options, inner_container)

df.to_csv('data_links.csv', index=False)

driver.quit()
