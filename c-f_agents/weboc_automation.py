from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

with open("extracted_invoice.json", "r", encoding="utf-8") as f:
    invoice_data = json.load(f)

driver = webdriver.Chrome()
driver.get("https://www.weboc.gov.pk")

time.sleep(20)  # Manual login

driver.find_element(By.NAME, "invoiceNumber").send_keys(invoice_data.get("Invoice Number", ""))
driver.find_element(By.NAME, "invoiceDate").send_keys(invoice_data.get("Invoice Date", ""))
driver.find_element(By.NAME, "itemDescription").send_keys(invoice_data.get("Item Description", ""))
driver.find_element(By.NAME, "quantity").send_keys(str(invoice_data.get("Quantity", "")))
driver.find_element(By.NAME, "unitPrice").send_keys(str(invoice_data.get("Unit Value", "")))
driver.find_element(By.NAME, "totalValue").send_keys(str(invoice_data.get("Total Value", "")))
driver.find_element(By.NAME, "originCountry").send_keys(invoice_data.get("Country of Origin", ""))
driver.find_element(By.NAME, "hsCode").send_keys(invoice_data.get("HS Code", ""))


