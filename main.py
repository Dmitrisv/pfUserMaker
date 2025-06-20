from selenium import webdriver
from selenium.webdriver.common.by import By
import slugify
import string
import time
import secrets


BASE_URL = ""
USER_NAME = ""
PASSWORD = ""

def generate_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(12))
    return password

def generate_slug(fullname: str):

    parts = fullname.split(" ")
    username = parts[0] + parts[1][0] + parts[2][0]

    return slugify.slugify(username)

def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless=new") 
    options.add_experimental_option("prefs",{
        "safebrowsing.enabled": True,
    })
    return options



def automation(fullname: str):
    user_pass = generate_password()
    options = get_default_chrome_options()
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options)
    driver.get(f"{BASE_URL}")
    user = driver.find_element(By.ID,"usernamefld")
    password = driver.find_element(By.ID,"passwordfld")
    enter = driver.find_element(By.CLASS_NAME, "btn-success")
    user.send_keys(USER_NAME)
    password.send_keys(PASSWORD)
    enter.click()
    time.sleep(5)
    driver.get(f"{BASE_URL}system_usermanager.php?act=new")
    driver.find_element(By.ID,"usernamefld").send_keys(generate_slug(fullname))
    driver.find_element(By.ID,"passwordfld1").send_keys(user_pass)
    driver.find_element(By.ID,"passwordfld2").send_keys(user_pass)
    driver.find_element(By.ID,"descr").send_keys(fullname)
    driver.find_element(By.ID,"showcert").click()
    driver.find_element(By.ID,"name").send_keys(fullname)
    driver.find_element(By.ID,"save").click()
    time.sleep(5)
    print(f"""
        Login: {generate_slug(fullname)}
        Pass: {user_pass}
        """)
    

def main():
    automation(input("Full name: "))

if __name__ == "__main__":
    main()
