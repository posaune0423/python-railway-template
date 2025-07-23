"""
Python Railway Template - Selenium Grid Example

A modern Python template for Railway deployment with uv, Ruff, and Docker.
This example demonstrates Selenium web scraping using official Selenium Grid Docker images.
"""

import logging
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def setup_logger() -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)


def setup_driver(browser: str = "chrome", hub_url: str = "http://localhost:4444") -> webdriver.Remote:
    """Initialize remote driver with Selenium Grid configuration."""

    # Set up grid connection
    grid_url = f"{hub_url}/wd/hub"

    if browser.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        # Selenium 4では options を直接使用
        driver = webdriver.Remote(command_executor=grid_url, options=options)

    elif browser.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        # Selenium 4では options を直接使用
        driver = webdriver.Remote(command_executor=grid_url, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'")

    return driver


def simple_scrape_test(driver: webdriver.Remote, logger: logging.Logger) -> dict[str, str]:
    """Perform a simple scraping test to verify functionality."""
    test_url = "https://httpbin.org/html"

    try:
        logger.info("Navigating to test page...")
        driver.get(test_url)

        # Wait for page to load and get title
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        title = driver.title
        page_source_length = len(driver.page_source)
        current_url = driver.current_url

        logger.info("Navigated to test page")

        # Try to get the h1 text
        try:
            h1_element = driver.find_element(By.TAG_NAME, "h1")
            h1_text = h1_element.text
        except Exception:
            h1_text = "N/A"

        # Get browser info
        browser_name = driver.capabilities.get("browserName", "unknown")
        browser_version = driver.capabilities.get("browserVersion", "unknown")

        result = {
            "status": "success",
            "title": title,
            "h1_text": h1_text,
            "page_source_length": str(page_source_length),
            "url": current_url,
            "browser_name": browser_name,
            "browser_version": browser_version,
            "execution_mode": "selenium_grid",
        }

        logger.info(f"Scraping successful: {result}")
        return result

    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return {"status": "error", "error": str(e), "url": test_url}


def take_screenshot(driver: webdriver.Remote, filename: str = "screenshot.png") -> str | None:
    """Take a screenshot and save it to reports directory."""
    try:
        # Ensure reports directory exists
        reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_dir, exist_ok=True)

        filepath = os.path.join(reports_dir, filename)
        driver.save_screenshot(filepath)
        return filepath
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
        return None


def main() -> None:
    """Main application entry point."""
    logger = setup_logger()

    print("🚀 Python Railway Template - Selenium Grid Example")
    print("=" * 60)

    # Get configuration from environment variables
    hub_url = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444")
    browser = os.getenv("SELENIUM_BROWSER", "chrome").lower()

    print(f"Selenium Hub URL: {hub_url}")
    print(f"Browser: {browser}")
    print(f"Grid Web UI: {hub_url.replace('/wd/hub', '').replace(':4444', ':4444')}")
    print(f"VNC Viewer: http://localhost:{'7900' if browser == 'chrome' else '7901'}")
    print("-" * 60)

    driver = None
    try:
        logger.info(f"Starting Selenium Grid test with {browser}...")
        driver = setup_driver(browser=browser, hub_url=hub_url)
        logger.info(f"Connected to Selenium Grid successfully with {browser}")

        result = simple_scrape_test(driver, logger)

        # Take a screenshot
        screenshot_path = take_screenshot(driver, f"test_{browser}_screenshot.png")

        # Display results
        if result["status"] == "success":
            print(f"✅ Status: {result['status']}")
            print(f"📄 Title: {result['title']}")
            print(f"📝 H1 Text: {result['h1_text']}")
            print(f"📊 Page source length: {result['page_source_length']}")
            print(f"🔗 URL: {result['url']}")
            print(f"🌐 Browser: {result['browser_name']} {result['browser_version']}")
            print(f"⚙️  Mode: {result['execution_mode']}")
            if screenshot_path:
                print(f"📸 Screenshot: {screenshot_path}")
            print("")
            print("🎉 Selenium Grid test completed successfully!")
            print("")
            print("🔍 To watch the browser in action:")
            print(f"   Open http://localhost:{'7900' if browser == 'chrome' else '7901'} in your browser")
            print("   Password: secret")
        else:
            print(f"❌ Test failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Application failed: {e}")
        print("")
        print("🔧 Troubleshooting:")
        print("- Check if Selenium Grid is running (docker-compose up)")
        print(f"- Verify Grid status at {hub_url.replace('/wd/hub', '')}")
        print("- Check if the specified browser node is available")
        print("- Ensure proper network connectivity")
        sys.exit(1)

    finally:
        if driver:
            try:
                driver.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.warning(f"Error closing driver: {e}")


if __name__ == "__main__":
    main()
