#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA
import time
from Selenium2Library import Selenium2Library
from robot.libraries import DateTime
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from selenium.webdriver import ActionChains, FirefoxProfile, ChromeOptions, Chrome, DesiredCapabilities
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from robot_instances import *
import os
import os.path
from selenium.webdriver.common.keys import Keys
from robot.api import logger


class Selenium2LibraryKeywords(object):
    WIDTH_DEFAULT = "1366"
    HEIGHT_DEFAULT = "768"
    SELENIUM_SPEED = "0 sec"
    SELENIUM_TEST_BROWSER = "ff"
    SELENIUM_TIMEOUT = "5 s"
    # noinspection PyPep8
    XPATH2_JS = 'if(!window.jQuery){var headID = document.getElementsByTagName("head")[0]; var newScript = document.createElement(\'script\'); newScript.type=\'text/javascript\'; newScript.src=\'http://llamalab.com/js/xpath/minified/XPath.js\'; headID.appendChild(newScript);}'
    # noinspection PyPep8
    JQUERY_JS = "if(!window.jQuery){var headID = document.getElementsByTagName(\"head\")[0]; var newScript = document.createElement('script'); newScript.type='text/javascript'; newScript.src='http://code.jquery.com/jquery-2.1.4.min.js'; headID.appendChild(newScript);}"

    # noinspection PyArgumentList
    def __init__(self, **kwargs):
        super(Selenium2LibraryKeywords, self).__init__(**kwargs)
        for base in Selenium2LibraryKeywords.__bases__:
            if hasattr(base, '__init__'):
                base.__init__(self)
        print "Selenium2LibraryExtensions loaded"

    @staticmethod
    def open_new_tab(url):
        """Hack it use Control +t to open new tab"""
        driver = s2l()._current_browser()
        body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + 't')
        time.sleep(2)
        s2l().go_to(url)

    @staticmethod
    def switch_tab_by_id(id_tab):
        """Hack it use Control + 1,2,3 etc to switch tab"""
        driver = s2l()._current_browser()
        body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + id_tab)
        time.sleep(4)
        # actions = ActionChains(driver)
        # actions.key_down(Keys.CONTROL).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.CONTROL).perform()

    @staticmethod
    def press_key_python(command, locator="//body", strategy="XPATH"):
        """Hack !!!  example argument | Keys.CONTROL + 't' |Keys.TAB + Keys.SHIFT"""
        driver = s2l()._current_browser()
        element = driver.find_element(eval("By." + strategy), locator)
        element.send_keys(eval(command))

    @staticmethod
    def close_tab():
        """Hack it use Control +w to close tab"""
        driver = s2l()._current_browser()
        body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + 'w')

    @staticmethod
    def set_browser_size_and_position(width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, x=0, y=0):
        s2l().set_window_size(width, height)
        s2l().set_window_position(x, y)

    @staticmethod
    def go_to_smart(url):
        """Redirect only in on different url"""
        current_url = s2l().get_location()
        if url != current_url:
            s2l().go_to(url)

    @staticmethod
    def click_element_extended(locator, timeout=None, error_msg=None):
        """Click element proceed with following steps
        1.wait_until_page_contains_element
        2.wait_until_element_is_visible_wait_until_element_is_visible
        3.mouse_over"""
        s2l().wait_until_page_contains_element(locator, timeout, error_msg)
        s2l().wait_until_element_is_visible(locator, timeout, error_msg)
        s2l().mouse_over(locator)
        s2l().click_element(locator)

    @staticmethod
    def double_click_element_extended(locator, timeout=None, error=None):
        s2l().wait_until_page_contains_element(locator, timeout, error)
        s2l().wait_until_element_is_visible(locator, timeout, error)
        s2l().mouse_over(locator)
        s2l().double_click_element(locator)

    def click_element_extended_and_wait(self, locator, sleep, timeout=None, error_msg=None, reason=None):
        self.click_element_extended(locator, timeout, error_msg)
        bi().sleep(sleep, reason)

    @staticmethod
    def open_browser_extension(url, browser="ff", width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, x="0", y="0", alias=None, remote_url=False,
            desired_capabilities=None, ff_profile_dir=None, selenium_timeout=SELENIUM_TIMEOUT, keyword_to_run_on_failure="Capture Page Screenshot Extension"):
        s2l().open_browser("about:blank", browser, alias, remote_url, desired_capabilities, ff_profile_dir)
        s2l().set_window_position(x, y)
        s2l().set_window_size(width, height)
        s2l().set_selenium_timeout(selenium_timeout)
        s2l().register_keyword_to_run_on_failure(keyword_to_run_on_failure)
        s2l().go_to(url)

    def create_download_dir_capabilities_for_chrome(self, path_to_download, **extentionsFiles):
        chromeOptions = ChromeOptions()
        prefs = {"download.default_directory": path_to_download}
        chromeOptions.add_experimental_option("prefs", prefs)
        chromeOptions.add_argument("--disable-web-security")
        for singleExtenation in extentionsFiles:
            chromeOptions.add_extension(singleExtenation)
        return chromeOptions.to_capabilities()

    def import_xpath2(self):
        s2l().execute_javascript(self.XPATH2_JS)

    # noinspection PyPep8Naming,PyPep8Naming
    def import_jQuery(self):
        s2l().execute_javascript(self.JQUERY_JS)

    @staticmethod
    def capture_page_screenshot_extension(prefix="", postfix="", add_time_stamp=True, add_test_case_name=True, add_file_path_to_list="${list of screenshots}",
            output_dir="Screenshots"):
        output_dir_normalized = get_artifacts_dir(output_dir)

        if add_time_stamp == True:
            current_time = " " + DateTime.get_current_date(result_format="%Y.%m.%d_%H.%M.%S")
        else:
            current_time = ""
        if add_test_case_name == True:
            test_case_name = bi().get_variable_value("${TEST_NAME}")
        else:
            test_case_name = ""

        output_file = output_dir_normalized + "/" + prefix + test_case_name + postfix + current_time + ".png"
        output_file_normalized = os.path.normpath(output_file)

        s2l().capture_page_screenshot(output_file_normalized)

        results = bi().run_keyword_and_return_status("Variable Should Exist", add_file_path_to_list)

        if not results:
            list_with_files = bi().create_list(output_file_normalized)
            bi().set_test_variable(add_file_path_to_list, list_with_files)
        else:
            list_with_files = bi().create_list(output_file_normalized)
            list_with_files = bi().run_keyword("Combine Lists", add_file_path_to_list, list_with_files)
            bi().set_test_variable(add_file_path_to_list, list_with_files)

        return output_file_normalized

    @staticmethod
    def element_attribute_should_be(locator, attribute, attribute_value_expected, msg=None, values=True):
        actual_value = s2l().get_element_attribute(locator + "@" + attribute)
        actual_value, attribute_value_expected = [bi()._convert_to_string(i) for i in actual_value, attribute_value_expected]
        bi()._should_be_equal(actual_value, attribute_value_expected, msg, values)

    @staticmethod
    def create_download_dir_profile_for_firefox(path, mimeTypes_file=None, *extentionsFiles):
        fp = FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
        fp.set_preference("browser.download.dir", os.path.normpath(path))
        fp.set_preference("xpinstall.signatures.required", False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
            "application/msword,application/csv,text/csv,image/png ,image/jpeg, application/pdf, text/html,text/plain,application/octet-stream")
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.update_preferences()

        for singleExtenation in extentionsFiles:
            fp.add_extension(singleExtenation)
        if not os.path.exists(path):
            os.makedirs(path)
        if mimeTypes_file != None:
            from shutil import copy2
            copy2(os.path.normpath(mimeTypes_file), fp.profile_dir)
        return fp.profile_dir
