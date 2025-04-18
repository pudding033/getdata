from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector
import time

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://www.dienmayxanh.com/may-lanh")
time.sleep(5)

# --- Cuộn xuống để load toàn bộ sản phẩm ---
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",  # XAMPP mặc định user là 'root'
    password="",  # Mặc định không có password
    database="dienmay"
)

mycursor = mydb.cursor()

product_elements = driver.find_elements(By.XPATH, '//li[contains(@class,"item") and .//strong[contains(@class,"price")]]')

for product in product_elements:
    try:
        name = product.find_element(By.XPATH, './/h3').text
        price = product.find_element(By.XPATH, './/strong[contains(@class,"price")]').text
        print(f"{name}: {price}")

        sql = "INSERT INTO may_lanh (ten_san_pham, gia) VALUES (%s, %s)"
        val = (name, price)
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        print("Lỗi khi lấy dữ liệu sản phẩm:", e)

# --- Đóng trình duyệt và DB ---
driver.quit()
mycursor.close()
mydb.close()
