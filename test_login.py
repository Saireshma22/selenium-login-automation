from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
import time

# Create clean temporary Chrome profile
temp_profile = tempfile.mkdtemp()

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={temp_profile}")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-notifications")

chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False
})

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

try:
    print("Running Positive Test Case...")
    driver.get("https://the-internet.herokuapp.com/login")

    username = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password = driver.find_element(By.ID, "password")

    username.send_keys("tomsmith")
    password.send_keys("SuperSecretPassword!")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    success_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    )

    if "You logged into a secure area!" in success_message.text:
        print("✅ Positive Test Passed")
    else:
        print("❌ Positive Test Failed")

    time.sleep(3)

    print("Running Negative Test Case...")
    driver.get("https://the-internet.herokuapp.com/login")

    username = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password = driver.find_element(By.ID, "password")

    username.send_keys("wronguser")
    password.send_keys("wrongpassword")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    error_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
    )

    if "Your username is invalid!" in error_message.text:
        print("✅ Negative Test Passed")
    else:
        print("❌ Negative Test Failed")

    print("\n🎉 All Tests Completed Successfully")

except Exception as e:
    print("❌ Test Failed:", e)

finally:
    time.sleep(5)
    driver.quit()