# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import time
import logging

# Initialize the Chrome browser using `webdriver.Chrome()`.
logging.basicConfig(filename='selenium.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logging.info('Starting the browser...')
options = ChromeOptions()
options.add_argument("--headless") 
driver = webdriver.Chrome(options=options)

# Navigate to the specified URL using `driver.get()`.
logging.info('Browser started. Access to the demo page to login.')
driver.get('https://www.saucedemo.com/')

# Log in to the website
user = 'standard_user'
driver.find_element(By.ID, 'user-name').send_keys(user)
driver.find_element(By.ID, 'password').send_keys('secret_sauce')
driver.find_element(By.ID, 'login-button').click()
logging.info("Successfully logged in as " + user)

# Wait for the page to load
time.sleep(2)  # Wait for 2 seconds

# Find the search input element
# Writing a CSS Selector for the "Add to cart" button for the first product displayed
add_to_cart_buttons = {
    "button#add-to-cart-sauce-labs-backpack"                        : "Sauce Labs Backpack",
    "button#add-to-cart-sauce-labs-bike-light"                      : "Sauce Labs Bike Light",
    "button#add-to-cart-sauce-labs-bolt-t-shirt"                    : "Sauce Labs Bolt T-Shirt",
    "button#add-to-cart-sauce-labs-fleece-jacket"                   : "Sauce Labs Fleece Jacket",
    "button#add-to-cart-sauce-labs-onesie"                          : "Sauce Labs Onesie",
    "button#add-to-cart-test\\.allthethings\\(\\)-t-shirt-\\(red\\)": "Test.allTheThings() T-Shirt (Red)"
}

# Locate the "Add to cart" button using `By.CSS_SELECTOR` and click it.
for button, label in add_to_cart_buttons.items():
    driver.find_element(By.CSS_SELECTOR, button).click()
    logging.info("Succesfully added to cart: " + label)
    time.sleep(1)  # Optional: short delay to simulate human-like actions

# Locate the cart icon using `By.CSS_SELECTOR`.
# Validate that the product is added to the cart by checking the cart icon
cart_icon = driver.find_element(By.CSS_SELECTOR, "a.shopping_cart_link")
cart_item_count = cart_icon.text
## Print the number of items in the cart
logging.info(f"Number of items in the cart: {cart_item_count}")

# Get the list of items in the cart (identified by the "remove" button for each item)
remove_buttons = driver.find_elements(By.CSS_SELECTOR, "button.cart_button")
for remove_button in remove_buttons:
    remove_button.click()
    time.sleep(1)  # Wait a second after each removal
logging.info("Succesfully removed all items from shopping cart.")

# Verify the cart is empty
cart_item_count_after_removal = driver.find_element(By.CSS_SELECTOR, "a.shopping_cart_link").text
if not cart_item_count_after_removal: 
    cart_item_count_after_removal = "0"
logging.info(f"Number of items in the cart after removal: {cart_item_count_after_removal}")

# Optional: Add some wait time to see the results before the browser closes
time.sleep(5)  # Wait for 5 seconds

# Close the browser
driver.quit()