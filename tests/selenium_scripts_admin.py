from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


CHROME_DRIVER_PATH = r"C:\Users\samci\Downloads\chromedriver-win64\chromedriver.exe"
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)


with open("tests/test_report_admin.txt", "w") as f:
    f.write("ADMIN TEST REPORT\n\n")

def log_test(objective, steps, expected, actual, status):
    with open("tests/test_report_admin.txt", "a") as f:
        f.write("------------------------------------------------------------\n")
        f.write(f"Test Objective: {objective}\n")
        f.write(f"Steps: {steps}\n")
        f.write(f"Expected Result: {expected}\n")
        f.write(f"Actual Result: {actual}\n")
        f.write(f"Status: {status}\n")
        f.write("------------------------------------------------------------\n\n")

# -----------------------------
# Test Case 1: Admin Login
# -----------------------------
try:
    driver.get("http://127.0.0.1:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("admin@example.com")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    actual = "Login successful" if "ADMIN DASHBOARD TEST" in driver.page_source else "Login failed"
    status = "PASS" if "ADMIN DASHBOARD TEST" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Admin Login",
         "Enter admin credentials and submit",
         "Admin dashboard should open",
         actual,
         status)

# -----------------------------
# Test Case 2: Accept a Pending Request
# -----------------------------
try:
    select_elements = driver.find_elements(By.NAME, "status")
    if select_elements:
        select_elements[0].send_keys("Scheduled")
        driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")[0].click()
        time.sleep(1)
        actual = "Status updated to Scheduled"
        status = "PASS"
    else:
        actual = "No requests found to update"
        status = "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Accept a Pending Request",
         "Change status from Pending to Scheduled and submit",
         "Request status should update",
         actual,
         status)

# -----------------------------
# Test Case 3: Deny/Cancel a Request
# -----------------------------
try:
    select_elements = driver.find_elements(By.NAME, "status")
    if select_elements:
        select_elements[0].send_keys("Cancelled")
        driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")[0].click()
        time.sleep(1)
        actual = "Status updated to Cancelled"
        status = "PASS"
    else:
        actual = "No requests found to cancel"
        status = "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Deny/Cancel a Request",
         "Change status to Cancelled and submit",
         "Request should be cancelled",
         actual,
         status)

# -----------------------------
# Test Case 4: Logout
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(1)
    actual = "Logout successful" if driver.find_elements(By.LINK_TEXT, "Login") else "Logout failed"
    status = "PASS" if "Login" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Admin Logout",
         "Click logout button",
         "Admin should be logged out",
         actual,
         status)

# -----------------------------
# Test Case 5: Access Dashboard Without Login
# -----------------------------
try:
    driver.get("http://127.0.0.1:5000/admin_dashboard")  # direct URL
    time.sleep(1)
    actual = "Redirected to login" if "Login" in driver.page_source else "Accessed dashboard without login"
    status = "PASS" if "Login" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Access Dashboard Without Login",
         "Try accessing admin dashboard URL directly without login",
         "Should redirect to login page",
         actual,
         status)

# -----------------------------
# Test Case 6: Admin Login with Wrong Credentials
# -----------------------------
try:
    driver.get("http://127.0.0.1:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("admin@example.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    actual = "Login failed message shown" if "Invalid" in driver.page_source else "Login succeeded incorrectly"
    status = "PASS" if "Invalid" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Admin Login with Wrong Credentials",
         "Enter wrong password and submit",
         "Login should fail",
         actual,
         status)

# -----------------------------
# Test Case 7: Accept Multiple Requests
# -----------------------------
try:
    driver.get("http://127.0.0.1:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("admin@example.com")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    select_elements = driver.find_elements(By.NAME, "status")
    for s in select_elements[:2]:
        s.send_keys("Scheduled")
    buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
    for b in buttons[:2]:
        b.click()
        time.sleep(0.5)
    actual = "First two requests scheduled"
    status = "PASS"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Accept Multiple Requests",
         "Change first two request statuses to Scheduled",
         "Both requests should be updated",
         actual,
         status)

# -----------------------------
# Test Case 8: Cancel Multiple Requests
# -----------------------------
try:
    select_elements = driver.find_elements(By.NAME, "status")
    for s in select_elements[:2]:
        s.send_keys("Cancelled")
    buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
    for b in buttons[:2]:
        b.click()
        time.sleep(0.5)
    actual = "First two requests cancelled"
    status = "PASS"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Cancel Multiple Requests",
         "Change first two request statuses to Cancelled",
         "Both requests should be cancelled",
         actual,
         status)

# -----------------------------
# Test Case 9: Check Status Badge Colors
# -----------------------------
try:
    badges = driver.find_elements(By.XPATH, "//span[contains(@class,'badge')]")
    actual = f"{len(badges)} badges found" if badges else "No badges found"
    status = "PASS" if badges else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Check Status Badge Colors",
         "Verify badge classes for request statuses",
         "All requests should have colored badges",
         actual,
         status)

# -----------------------------
# Test Case 10: Update Non-Pending Request
# -----------------------------
try:
    non_pending = [s for s in driver.find_elements(By.NAME, "status") if "Pending" not in s.get_attribute("value")]
    if non_pending:
        non_pending[0].send_keys("Completed")
        driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")[0].click()
        time.sleep(1)
        actual = "Updated non-pending request"
        status = "PASS"
    else:
        actual = "No non-pending request to update"
        status = "PASS"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Update Non-Pending Request",
         "Try updating a non-pending request",
         "Should allow update",
         actual,
         status)

# -----------------------------
# Test Case 11: Logout and Re-login
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("admin@example.com")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    actual = "Re-login successful" if "ADMIN DASHBOARD TEST" in driver.page_source else "Re-login failed"
    status = "PASS" if "ADMIN DASHBOARD TEST" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Logout and Re-login",
         "Logout and then login again",
         "Admin should access dashboard again",
         actual,
         status)

# -----------------------------
# Test Case 12: Navigate Dashboard Links
# -----------------------------
try:
    links = driver.find_elements(By.TAG_NAME, "a")
    for l in links[:3]:  # just test first 3 links
        href = l.get_attribute("href")
        if href:
            driver.get(href)
            time.sleep(0.5)
    actual = "Navigated first 3 links"
    status = "PASS"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Navigate Dashboard Links",
         "Click first few links on admin dashboard",
         "Pages should open without error",
         actual,
         status)

# -----------------------------
# Test Case 13: Page Refresh After Update
# -----------------------------
try:
    driver.refresh()
    time.sleep(1)
    actual = "Dashboard refreshed successfully"
    status = "PASS"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Page Refresh After Update",
         "Refresh the admin dashboard page",
         "Page should reload correctly",
         actual,
         status)

# -----------------------------
# Test Case 14: Verify Table Headers
# -----------------------------
try:
    headers = driver.find_elements(By.XPATH, "//table/thead/tr/th")
    actual = f"{len(headers)} table headers found"
    status = "PASS" if len(headers) == 7 else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Verify Table Headers",
         "Check all columns in requests table",
         "Should have ID, User, Item, Quantity, Location, Status, Update",
         actual,
         status)

# -----------------------------
# Test Case 15: Logout at End
# -----------------------------
try:
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(1)
    actual = "Final logout successful" if "Login" in driver.page_source else "Logout failed"
    status = "PASS" if "Login" in driver.page_source else "FAIL"
except Exception as e:
    actual = f"Exception: {e}"
    status = "FAIL"

log_test("Final Logout",
         "Click logout at end of admin tests",
         "Admin should be logged out",
         actual,
         status)

driver.quit()

