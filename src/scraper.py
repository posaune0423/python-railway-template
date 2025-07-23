"""
Selenium Standalone Chromium Scraper

Remote WebDriver with Standalone Chromium を使用したウェブスクレイピング機能
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from constants import (
    CHROME_USER_AGENT,
    CHROME_WINDOW_SIZE,
    CONNECTION_FAILED_MSG,
    CONNECTION_SUCCESS_MSG,
    DEFAULT_BROWSER,
    DEFAULT_REMOTE_URL_LOCAL,
    DEFAULT_SCREENSHOT_DIR,
    DEFAULT_TIMEOUT,
    ENV_SELENIUM_BROWSER,
    ENV_SELENIUM_REMOTE_URL,
    FIREFOX_WINDOW_HEIGHT,
    FIREFOX_WINDOW_WIDTH,
    SCRAPING_SUCCESS_MSG,
    SCREENSHOT_SAVED_MSG,
    SUPPORTED_BROWSERS,
    TEST_URL,
    UNSUPPORTED_BROWSER_MSG,
    WEBDRIVER_NOT_CONNECTED_MSG,
)
from utils.logger import get_app_logger


class StandaloneChromiumScraper:
    """Selenium Standalone Chromium を使用したスクレイパー"""

    def __init__(
        self, browser: str = DEFAULT_BROWSER, remote_url: str = DEFAULT_REMOTE_URL_LOCAL, timeout: int = DEFAULT_TIMEOUT
    ):
        """
        Args:
            browser: ブラウザタイプ (chrome/firefox)
            remote_url: Selenium Standalone サーバーURL
            timeout: WebDriverタイムアウト (秒)
        """
        self.browser = browser.lower()
        self.remote_url = remote_url
        self.timeout = timeout
        self.driver: webdriver.Remote | None = None
        self.logger = get_app_logger(__name__)

    def _create_chrome_options(self) -> ChromeOptions:
        """Chrome用オプションを作成"""
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={CHROME_WINDOW_SIZE}")
        options.add_argument(f"--user-agent={CHROME_USER_AGENT}")
        return options

    def _create_firefox_options(self) -> FirefoxOptions:
        """Firefox用オプションを作成"""
        options = FirefoxOptions()
        options.add_argument(f"--width={FIREFOX_WINDOW_WIDTH}")
        options.add_argument(f"--height={FIREFOX_WINDOW_HEIGHT}")
        return options

    def connect(self) -> None:
        """Remote WebDriver に接続"""
        self.logger.info(f"Connecting to Selenium Standalone {self.browser.title()}...")

        try:
            grid_url = f"{self.remote_url}/wd/hub"

            if self.browser == "chrome":
                options = self._create_chrome_options()
                self.driver = webdriver.Remote(command_executor=grid_url, options=options)

            elif self.browser == "firefox":
                options = self._create_firefox_options()
                self.driver = webdriver.Remote(command_executor=grid_url, options=options)

            else:
                supported_str = "', '".join(SUPPORTED_BROWSERS)
                raise ValueError(UNSUPPORTED_BROWSER_MSG.format(self.browser, f"'{supported_str}'"))

            # 接続確認
            browser_name = self.driver.capabilities.get("browserName", "unknown")
            browser_version = self.driver.capabilities.get("browserVersion", "unknown")

            self.logger.info(CONNECTION_SUCCESS_MSG.format(browser_name, browser_version))

        except Exception as e:
            self.logger.error(CONNECTION_FAILED_MSG.format(e))
            raise

    def disconnect(self) -> None:
        """WebDriver接続を切断"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Remote WebDriver disconnected")
            except Exception as e:
                self.logger.warning(f"Error during disconnect: {e}")
            finally:
                self.driver = None

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

    def scrape_test_page(self) -> dict[str, str]:
        """テストページをスクレイピング"""
        if not self.driver:
            raise RuntimeError(WEBDRIVER_NOT_CONNECTED_MSG)

        try:
            self.logger.info("Navigating to test page...")
            self.driver.get(TEST_URL)

            # ページロード待機
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

            # ページ情報取得
            title = self.driver.title
            page_source_length = len(self.driver.page_source)
            current_url = self.driver.current_url

            # H1テキスト取得
            try:
                h1_element = self.driver.find_element(By.TAG_NAME, "h1")
                h1_text = h1_element.text
            except Exception:
                h1_text = "N/A"

            # ブラウザ情報
            browser_name = self.driver.capabilities.get("browserName", "unknown")
            browser_version = self.driver.capabilities.get("browserVersion", "unknown")

            result = {
                "status": "success",
                "title": title,
                "h1_text": h1_text,
                "page_source_length": str(page_source_length),
                "url": current_url,
                "browser_name": browser_name,
                "browser_version": browser_version,
                "execution_mode": "selenium_standalone_chromium",
            }

            self.logger.info(SCRAPING_SUCCESS_MSG)
            self.logger.debug(f"Scraping result: {result}")

            return result

        except Exception as e:
            self.logger.error(f"Scraping failed: {e}")
            raise

    def take_screenshot(self, filename: str = "screenshot.png", directory: str = DEFAULT_SCREENSHOT_DIR) -> str:
        """スクリーンショットを保存"""
        if not self.driver:
            raise RuntimeError(WEBDRIVER_NOT_CONNECTED_MSG)

        # ディレクトリ作成
        os.makedirs(directory, exist_ok=True)

        filepath = os.path.join(directory, filename)

        try:
            self.driver.save_screenshot(filepath)
            self.logger.info(SCREENSHOT_SAVED_MSG.format(filepath))
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save screenshot: {e}")
            raise


def create_scraper_from_env() -> StandaloneChromiumScraper:
    """環境変数からスクレイパーを作成"""
    browser = os.getenv(ENV_SELENIUM_BROWSER, DEFAULT_BROWSER)
    remote_url = os.getenv(ENV_SELENIUM_REMOTE_URL, DEFAULT_REMOTE_URL_LOCAL)

    return StandaloneChromiumScraper(browser=browser, remote_url=remote_url)
