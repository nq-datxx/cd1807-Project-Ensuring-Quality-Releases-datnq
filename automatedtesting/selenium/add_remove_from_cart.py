#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

# Start the browser and navigate to https://www.saucedemo.com/
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the specified URL using `driver.get()`.
driver.get('https://www.saucedemo.com/')

# Log in to the website
driver.find_element(By.ID, 'user-name').send_keys('standard_user')
driver.find_element(By.ID, 'password').send_keys('secret_sauce')
driver.find_element(By.ID, 'login-button').click()

# Wait for the page to load
time.sleep(2)

# Add 6 different items to the cart
# List of CSS selectors for the "Add to Cart" buttons of the first 6 items
add_to_cart_buttons = [
    "button#add-to-cart-sauce-labs-backpack",
    "button#add-to-cart-sauce-labs-bike-light",
    "button#add-to-cart-sauce-labs-bolt-t-shirt",
    "button#add-to-cart-sauce-labs-fleece-jacket",
    "button#add-to-cart-sauce-labs-onesie",
    "button#add-to-cart-test\\.allthethings\\(\\)-t-shirt-\\(red\\)"
]

# Click the "Add to Cart" button for each item
for button in add_to_cart_buttons:
    driver.find_element(By.CSS_SELECTOR, button).click()
    time.sleep(1)  # Optional: short delay to simulate human-like actions

# Check the number of items in the cart
cart_icon = driver.find_element(By.CSS_SELECTOR, "a.shopping_cart_link")
cart_item_count = cart_icon.text
print(f"Number of items in the cart: {cart_item_count}")

# Now go to the cart and remove each item
cart_icon.click()
time.sleep(2)  # Wait for the cart page to load

# Get the list of items in the cart (identified by the "remove" button for each item)
remove_buttons = driver.find_elements(By.CSS_SELECTOR, "button.cart_button")
for remove_button in remove_buttons:
    remove_button.click()
    time.sleep(1)  # Wait a second after each removal

# Verify the cart is empty
cart_item_count_after_removal = driver.find_element(By.CSS_SELECTOR, "a.shopping_cart_link").text
if not cart_item_count_after_removal: 
    cart_item_count_after_removal = "0"
print(f"Number of items in the cart after removal: {cart_item_count_after_removal}")

# Optional: Add some wait time to see the results before the browser closes
time.sleep(3)

# Close the browser
driver.quit()
