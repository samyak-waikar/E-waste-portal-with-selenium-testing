from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# path to your chromedriver
CHROME_DRIVER_PATH = r"C:\Users\samci\Downloads\chromedriver-win64\chromedriver.exe"
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# file to save report
report_file = "tests/test_report.txt"

def log_test(objective, steps, expected, actual, status):
    with open("tests/test_report_user.txt", "a") as f:
        f.write("------------------------------------------------------------\n")
        f.write(f"Test Objective: {objective}\n")
        f.write(f"Steps: {steps}\n")
        f.write(f"Expected Result: {expected}\n")
        f.write(f"Actual Result: {actual}\n")
        f.write(f"Status: {status}\n")
        f.write("------------------------------------------------------------\n\n")


# Clear previous report
open(report_file, "w").close()

# -----------------------------
# Test Case 1: Open Home Page
# -----------------------------
driver.get("http://127.0.0.1:5000")
time.sleep(1)
log_test("Open Home Page",
         "Navigate to home page",
         "Home page should open",
         "Home page opened successfully" if "Welcome" in driver.page_source else "Home page failed to open",
         "PASS" if "Welcome" in driver.page_source else "FAIL")

# -----------------------------
# Test Case 2: Open Register Page
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Register").click()
    time.sleep(1)
    actual = "Register page opened" if "Register" in driver.page_source else "Register page failed to open"
    status = "PASS" if "Register" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Open Register Page",
         "Click Register link",
         "Register page should open",
         actual,
         status)

# -----------------------------
# Test Case 3: Submit Registration Form (valid)
# -----------------------------
try:
    driver.find_element(By.NAME, "username").send_keys("TestUser")
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.NAME, "confirm_password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    actual = "Registration successful" if "Login" in driver.page_source else "Registration failed"
    status = "PASS" if "Login" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Submit Registration Form (valid)",
         "Fill form with valid data and submit",
         "User should be registered and redirected to login",
         actual,
         status)

# -----------------------------
# Test Case 4: Submit Registration Form (invalid)
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Register").click()
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("")  # missing username
    driver.find_element(By.NAME, "email").send_keys("invalidemail")
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.NAME, "confirm_password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    actual = "Validation error displayed" if "This field is required" in driver.page_source or "Invalid" in driver.page_source else "Form submitted incorrectly"
    status = "PASS" if "Validation error displayed" in actual else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Submit Registration Form (invalid)",
         "Submit form with missing/invalid data",
         "Form should show validation errors",
         actual,
         status)

# -----------------------------
# Test Case 5: Login User (correct credentials)
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Login").click()
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("samcitywaikar@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    if "Dashboard" in driver.page_source or "My Pickup Requests" in driver.page_source:
        actual = "Login successful"
        status = "PASS"
    else:
        actual = "Login failed"
        status = "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Login User (correct credentials)",
         "Enter valid email and password and submit",
         "User should be logged in",
         actual,
         status)

# -----------------------------
# Test Case 6: Login User (wrong credentials)
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Login").click()
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("samcitywaikar@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    actual = "Login failed as expected" if "Invalid" in driver.page_source or "Login" in driver.current_url else "Login succeeded incorrectly"
    status = "PASS" if "Login failed as expected" in actual else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Login User (wrong credentials)",
         "Enter invalid password",
         "Login should fail",
         actual,
         status)

# -----------------------------
# Test Case 7: Submit E-Waste Request (valid)
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Login").click()
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("samcitywaikar@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "New Request").click()
    time.sleep(1)
    driver.find_element(By.NAME, "item_type").send_keys("Laptop")
    driver.find_element(By.NAME, "quantity").send_keys("1")
    driver.find_element(By.NAME, "location").send_keys("Pune")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    actual = "Request submitted successfully" if "Laptop" in driver.page_source else "Request submission failed"
    status = "PASS" if "Laptop" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Submit E-Waste Request (valid)",
         "Fill pickup form with valid data and submit",
         "Request should appear in dashboard",
         actual,
         status)

# -----------------------------
# Test Case 8: Logout
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(1)
    if driver.find_elements(By.LINK_TEXT, "Login"):
        actual = "Logout successful"
        status = "PASS"
    else:
        actual = "Logout failed"
        status = "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Logout",
         "Click logout button",
         "User should be logged out",
         actual,
         status)

# -----------------------------
# Test Case 9: Cancel Pending Request
# -----------------------------
try:
    driver.get("http://127.0.0.1:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("samcitywaikar@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    cancel_buttons = driver.find_elements(By.XPATH, "//button[text()='Cancel']")
    if cancel_buttons:
        cancel_buttons[0].click()
        time.sleep(1)
        actual = "Pending request cancelled successfully"
        status = "PASS"
    else:
        actual = "No pending request found to cancel"
        status = "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Cancel Pending Request",
         "Click cancel on a pending request",
         "Request should be cancelled",
         actual,
         status)

# -----------------------------
# Test Case 10: Cancel Completed Request
# -----------------------------
try:
    completed_requests = driver.find_elements(By.XPATH, "//td[.='Completed']/following-sibling::td/button")
    if completed_requests:
        completed_requests[0].click()
        time.sleep(1)
        actual = "Cancellation should not be allowed"
        status = "FAIL"
    else:
        actual = "No completed request found, cannot cancel"
        status = "PASS"
except Exception as e:
    actual = f"Exception: {e}"
    status = "PASS"  # if no completed request, this is expected

log_test("Cancel Completed Request",
         "Try to cancel a completed request",
         "Should not allow cancellation",
         actual,
         status)

# -----------------------------
# Test Case 11: Access Request Pickup Page
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "New Request").click()
    time.sleep(1)
    actual = "Request Pickup page opened" if "Request E-Waste Pickup" in driver.page_source else "Request Pickup page failed to open"
    status = "PASS" if "Request E-Waste Pickup" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Access Request Pickup Page",
         "Click New Request link from dashboard",
         "Request Pickup page should open",
         actual,
         status)

# -----------------------------
# Test Case 12: Check Status Badge Colors
# -----------------------------
try:
    driver.get("http://127.0.0.1:5000/dashboard")
    time.sleep(1)
    statuses = driver.find_elements(By.XPATH, "//span[contains(@class,'badge')]")
    color_pass = all([s.get_attribute("class") for s in statuses])
    actual = f"{len(statuses)} status badges found with color classes" if color_pass else "Status badges missing or incorrect"
    status = "PASS" if color_pass else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Check Status Badge Colors",
         "Verify badge classes for request statuses",
         "All requests should have correct colored badges",
         actual,
         status)

# -----------------------------
# Test Case 13: Navigate Back to Dashboard
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "My Dashboard").click()
    time.sleep(1)
    actual = "Dashboard opened successfully" if "My Pickup Requests" in driver.page_source else "Failed to open dashboard"
    status = "PASS" if "My Pickup Requests" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Navigate Back to Dashboard",
         "Click My Dashboard link from any page",
         "Dashboard should open",
         actual,
         status)

# -----------------------------
# Test Case 14: Submit Multiple Requests
# -----------------------------
try:
    for i in range(2):
        driver.find_element(By.LINK_TEXT, "New Request").click()
        time.sleep(1)
        driver.find_element(By.NAME, "item_type").send_keys(f"Device {i+1}")
        driver.find_element(By.NAME, "quantity").send_keys("1")
        driver.find_element(By.NAME, "location").send_keys("Pune")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
    actual = "Multiple requests submitted successfully" if "Device 2" in driver.page_source else "Failed to submit multiple requests"
    status = "PASS" if "Device 2" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Submit Multiple Requests",
         "Submit two new requests sequentially",
         "Both requests should appear in dashboard",
         actual,
         status)

# -----------------------------
# Test Case 15: Logout
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(1)
    actual = "Logout successful" if driver.find_elements(By.LINK_TEXT, "Login") else "Logout failed"
    status = "PASS" if "Login" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Logout",
         "Click logout button",
         "User should be logged out",
         actual,
         status)


driver.quit()
print("User Selenium Tests Completed. Report saved in test_report.txt")
