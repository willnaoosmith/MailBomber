from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import re, requests, time

email = input("Enter your target email: ")

urls = []

newsletterLists = [	
	"https://raw.githubusercontent.com/zudochkin/awesome-newsletters/refs/heads/master/README.md",
	"https://raw.githubusercontent.com/wallies/awesome-newsletters/refs/heads/master/README.md",
	"https://raw.githubusercontent.com/learn-anything/newsletters/refs/heads/master/readme.md"
]

for newsletterList in newsletterLists:
	content = requests.get(newsletterList).text
	urls += [m.group(1) for m in re.finditer(r'- \[.*?\]\((https?://[^\s)]+)\)', content)]

urls = list(dict.fromkeys(urls))

options = Options()
driver = webdriver.Firefox(options=options)

for url in urls:
	try:
		print(f"\nAcessing url {urls.index(url) + 1} of {len(urls)}.")
		driver.get(url)
		time.sleep(3)

		inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="email"]')
		
		if not inputs:
			inputs = [i for i in driver.find_elements(By.CSS_SELECTOR, 'input') if 'mail' in (i.get_attribute('placeholder') or '').lower()]

		if inputs:
			print("Email input found! Typing the target mail.")
			inputs[-1].send_keys(email)

		else:
			input(f"No email input found! Fill it manually and press Enter...")

		submits = driver.find_elements(By.CSS_SELECTOR, 'input[type="submit"], button[type="submit"]')

		if submits:
			print("Submit button found! Pressing it.")
			submits[-1].click()

		else:
			print(f"No submit button found! Submit it manually.")
	
		input(f"solve the captcha if this newsletter has one, Once done, press Enter to progress...")

	except Exception as e:
		print(f"Error with {url}: {e}")

driver.quit()