"""Script to automate sign-in and sign-out functionality."""

from os import path
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from api.exceptions import EmployeeDoesNotExists
from api.model.employee import Employee
from api.modules.logger import init_logger
from api.service.employee import decrypt

logger = init_logger(__name__, "GREYTHR_AUTOMATION_HELPER")

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62"  # pylint: disable=C0301
URL = "https://sarvaha.greythr.com/home.do"

SIGN_OPTIONS = {
    "SignIn": "Sign In",
    "SignOut": "Sign Out",
}


def init_chrome_web_driver():
    """Create a new instance of Chrome driver for scrapping."""
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={USER_AGENT}")
    options.headless = True
    return webdriver.Chrome(
        executable_path=path.abspath("/usr/bin/chromedriver"), options=options
    )


def get_interactive_element(selenium_driver: webdriver, value, is_list=True):
    """Find web elements from web which are interactive."""
    return (
        selenium_driver.find_elements(By.XPATH, value)
        if is_list
        else selenium_driver.find_element(By.XPATH, value)
    )


def execute_sign_operation(
    eid: str = "", employee: Employee = None, action: str = ""
):  # sourcery skip: extract-method
    """Perform automated GreytHR signin.

    Args:
        eid (str): Employee ID
        employee (Employee): Employee object
        action (str): Sign In or Sign Out?
    """

    if employee is None:
        employee = Employee.query.filter(Employee.eid == eid).first()

        if not employee:
            raise EmployeeDoesNotExists()

    driver = init_chrome_web_driver()
    logger.debug(f"[{employee.eid}] Driver Initialized")

    driver.get(URL)
    sleep(2)
    logger.debug(f"[{employee.eid}] Login page loaded")

    username, password = get_interactive_element(driver, value="//input")
    username.send_keys(employee.eid)
    password.send_keys(decrypt(employee.password))

    get_interactive_element(driver, value="//button", is_list=False).click()
    sleep(5)
    logger.debug(f"[{employee.eid}] Logged in")
    driver.set_window_size(1920, 1080)

    sign_action_button = get_interactive_element(
        driver, value="//gt-button[1]", is_list=False
    )

    logger.debug(
        f"[{employee.eid}] Current SignIn Status: '{sign_action_button.text}' | Action: '{action}'"
    )

    if not action or SIGN_OPTIONS[action] == sign_action_button.text:
        sign_action_button.click()
        sleep(5)

    logger.debug(f"[{employee.eid}] Done! Exiting!")
    driver.quit()
