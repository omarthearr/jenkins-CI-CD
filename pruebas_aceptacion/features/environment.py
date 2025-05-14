# -- FILE: features/environment.py
from behave import fixture, use_fixture
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


@fixture
def selenium_browser_chrome(context):
    chrome_options = Options()
    chrome_options.set_capability("browserName", "chrome")

    context.driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=chrome_options
    )
    yield context.driver
    context.driver.quit()


def before_all(context):
    use_fixture(selenium_browser_chrome, context)
    # -- HINT: CLEANUP-FIXTURE is performed after after_all() hook is called.
