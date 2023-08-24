"""Script to automate sign-in and sign-out functionality."""

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.exceptions import AutoSignFailedError, EmployeeDoesNotExists

from api.model.employee import Employee
from api.service.employee import decrypt

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62"  # pylint: disable=C0301
URL = "https://sarvaha.greythr.com/home.do"


def init_chrome_web_driver():
    """Create a new instance of Chrome driver for scrapping."""
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={USER_AGENT}")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def get_interactive_element(selenium_driver: webdriver, value, is_list=True):
    """Find web elements from web which are interactive."""
    return (
        selenium_driver.find_elements(By.XPATH, value)
        if is_list
        else selenium_driver.find_element(By.XPATH, value)
    )


def execute_sign_operation(eid: str):  # sourcery skip: extract-method
    """Perform automated GreytHR signin.

    Args:
        employee (Employee): Employee object
    """
    employee = Employee.query.filter(Employee.eid == eid).first()

    if not employee:
        raise EmployeeDoesNotExists()

    driver = init_chrome_web_driver()

    try:
        driver.get(URL)
        sleep(2)

        username, password = get_interactive_element(driver, value="//input")
        username.send_keys(employee.eid)
        password.send_keys(decrypt(employee.password))

        get_interactive_element(driver, value="//button", is_list=False).click()
        sleep(5)

        get_interactive_element(driver, value="//gt-button[2]", is_list=False).click()
        sleep(5)

    except Exception as err:
        raise AutoSignFailedError(str(err)) from err
    finally:
        print("Exiting...")
        driver.quit()
