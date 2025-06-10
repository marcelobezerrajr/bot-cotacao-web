def screenshot_error(driver, error_message):
    """
    Takes a screenshot of the current browser window and saves it with the error message as part of the filename.

    Args:
        driver: The Selenium WebDriver instance.
        error_message: A string containing the error message to include in the screenshot filename.
    """
    import time

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_error_message = "".join(c if c.isalnum() else "_" for c in error_message)
    screenshot_filename = f"screenshot_{timestamp}_{safe_error_message}.png"
    driver.save_screenshot(screenshot_filename)

    print(f"Screenshot saved as {screenshot_filename}")
