"""
Tests for Python Railway Template - Selenium Grid Example
"""

import os
from unittest.mock import Mock, patch

import pytest

from src.main import main, setup_driver, setup_logger, simple_scrape_test, take_screenshot


class TestLogger:
    """Test logger setup."""

    def test_setup_logger(self):
        """Test that logger is properly configured."""
        logger = setup_logger()
        assert logger.name == "src.main"
        # Logger should be a logging.Logger instance
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")
        assert hasattr(logger, "warning")


class TestDriverSetup:
    """Test Selenium Grid driver setup."""

    @patch("src.main.webdriver.Remote")
    def test_setup_driver_chrome_default(self, mock_remote):
        """Test driver setup with Chrome (default)."""
        mock_driver = Mock()
        mock_remote.return_value = mock_driver

        driver = setup_driver()

        # Verify webdriver.Remote was called with correct parameters
        mock_remote.assert_called_once()
        call_args = mock_remote.call_args

        # Check command_executor
        assert call_args.kwargs["command_executor"] == "http://localhost:4444/wd/hub"

        # Check options (Selenium 4)
        options = call_args.kwargs["options"]
        assert hasattr(options, "arguments")  # ChromeOptions object

    @patch("src.main.webdriver.Remote")
    def test_setup_driver_firefox(self, mock_remote):
        """Test driver setup with Firefox."""
        mock_driver = Mock()
        mock_remote.return_value = mock_driver

        driver = setup_driver(browser="firefox")

        call_args = mock_remote.call_args
        options = call_args.kwargs["options"]
        assert hasattr(options, "arguments")  # FirefoxOptions object

    @patch("src.main.webdriver.Remote")
    def test_setup_driver_custom_hub_url(self, mock_remote):
        """Test driver setup with custom hub URL."""
        mock_driver = Mock()
        mock_remote.return_value = mock_driver

        custom_hub = "http://remote-grid:4444"
        driver = setup_driver(hub_url=custom_hub)

        call_args = mock_remote.call_args
        assert call_args.kwargs["command_executor"] == f"{custom_hub}/wd/hub"

    def test_setup_driver_unsupported_browser(self):
        """Test that driver setup raises error for unsupported browser."""
        with pytest.raises(ValueError, match="Unsupported browser: edge"):
            setup_driver(browser="edge")


class TestScrapeTest:
    """Test scraping functionality."""

    def test_simple_scrape_test_success(self):
        """Test successful scraping."""
        # Mock driver
        mock_driver = Mock()
        mock_driver.title = "Test Page"
        mock_driver.page_source = "<html><body><h1>Test</h1></body></html>"
        mock_driver.current_url = "https://httpbin.org/html"
        mock_driver.capabilities = {"browserName": "chrome", "browserVersion": "120.0.0.0"}

        # Mock element
        mock_element = Mock()
        mock_element.text = "Test Header"
        mock_driver.find_element.return_value = mock_element

        # Mock logger
        mock_logger = Mock()

        # Mock WebDriverWait
        with patch("src.main.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = True

            result = simple_scrape_test(mock_driver, mock_logger)

        # Verify result
        assert result["status"] == "success"
        assert result["title"] == "Test Page"
        assert result["h1_text"] == "Test Header"
        assert result["url"] == "https://httpbin.org/html"
        assert result["browser_name"] == "chrome"
        assert result["browser_version"] == "120.0.0.0"
        assert result["execution_mode"] == "selenium_grid"
        assert result["page_source_length"] == "39"  # Length of mock HTML

    def test_simple_scrape_test_failure(self):
        """Test scraping failure."""
        # Mock driver that raises exception
        mock_driver = Mock()
        mock_driver.get.side_effect = Exception("Connection failed")

        # Mock logger
        mock_logger = Mock()

        result = simple_scrape_test(mock_driver, mock_logger)

        # Verify error result
        assert result["status"] == "error"
        assert "Connection failed" in result["error"]
        assert result["url"] == "https://httpbin.org/html"

    def test_simple_scrape_test_h1_not_found(self):
        """Test scraping when h1 element is not found."""
        # Mock driver
        mock_driver = Mock()
        mock_driver.title = "Test Page"
        mock_driver.page_source = "<html><body></body></html>"
        mock_driver.current_url = "https://httpbin.org/html"
        mock_driver.capabilities = {"browserName": "firefox", "browserVersion": "119.0"}
        mock_driver.find_element.side_effect = Exception("Element not found")

        # Mock logger
        mock_logger = Mock()

        # Mock WebDriverWait
        with patch("src.main.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = True

            result = simple_scrape_test(mock_driver, mock_logger)

        # Verify result with N/A h1_text
        assert result["status"] == "success"
        assert result["h1_text"] == "N/A"


class TestScreenshot:
    """Test screenshot functionality."""

    @patch("src.main.os.makedirs")
    @patch("src.main.os.getcwd")
    def test_take_screenshot_success(self, mock_getcwd, mock_makedirs):
        """Test successful screenshot capture."""
        mock_getcwd.return_value = "/app"
        mock_driver = Mock()
        mock_driver.save_screenshot.return_value = True

        result = take_screenshot(mock_driver, "test.png")

        assert result == "/app/reports/test.png"
        mock_makedirs.assert_called_once_with("/app/reports", exist_ok=True)
        mock_driver.save_screenshot.assert_called_once_with("/app/reports/test.png")

    @patch("src.main.os.makedirs")
    @patch("src.main.os.getcwd")
    def test_take_screenshot_failure(self, mock_getcwd, mock_makedirs):
        """Test screenshot failure."""
        mock_getcwd.return_value = "/app"
        mock_driver = Mock()
        mock_driver.save_screenshot.side_effect = Exception("Screenshot failed")

        result = take_screenshot(mock_driver, "test.png")

        assert result is None


class TestMain:
    """Test main function."""

    @patch.dict(os.environ, {"SELENIUM_HUB_URL": "http://test:4444", "SELENIUM_BROWSER": "firefox"})
    @patch("src.main.setup_logger")
    @patch("src.main.setup_driver")
    @patch("src.main.simple_scrape_test")
    @patch("src.main.take_screenshot")
    @patch("builtins.print")
    def test_main_success(self, mock_print, mock_screenshot, mock_scrape, mock_setup_driver, mock_setup_logger):
        """Test successful main execution."""
        # Mock setup
        mock_logger = Mock()
        mock_setup_logger.return_value = mock_logger

        mock_driver = Mock()
        mock_setup_driver.return_value = mock_driver

        mock_scrape.return_value = {
            "status": "success",
            "title": "Test",
            "h1_text": "Header",
            "page_source_length": "100",
            "url": "https://test.com",
            "browser_name": "firefox",
            "browser_version": "119.0",
            "execution_mode": "selenium_grid",
        }

        mock_screenshot.return_value = "/app/reports/test_firefox_screenshot.png"

        # Run main
        main()

        # Verify calls
        mock_setup_driver.assert_called_once_with(browser="firefox", hub_url="http://test:4444")
        mock_scrape.assert_called_once_with(mock_driver, mock_logger)
        mock_screenshot.assert_called_once_with(mock_driver, "test_firefox_screenshot.png")
        mock_driver.quit.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    @patch("src.main.setup_logger")
    @patch("src.main.setup_driver")
    @patch("src.main.simple_scrape_test")
    @patch("builtins.print")
    def test_main_default_values(self, mock_print, mock_scrape, mock_setup_driver, mock_setup_logger):
        """Test main function with default environment values."""
        # Mock setup
        mock_logger = Mock()
        mock_setup_logger.return_value = mock_logger

        mock_driver = Mock()
        mock_setup_driver.return_value = mock_driver

        mock_scrape.return_value = {
            "status": "success",
            "title": "Test",
            "h1_text": "Header",
            "page_source_length": "100",
            "url": "https://test.com",
            "browser_name": "chrome",
            "browser_version": "120.0",
            "execution_mode": "selenium_grid",
        }

        # Mock take_screenshot
        with patch("src.main.take_screenshot") as mock_screenshot:
            mock_screenshot.return_value = "/app/reports/test_chrome_screenshot.png"

            # Run main
            main()

        # Verify default values were used
        mock_setup_driver.assert_called_once_with(browser="chrome", hub_url="http://localhost:4444")

    @patch.dict(os.environ, {}, clear=True)
    @patch("src.main.setup_logger")
    @patch("src.main.setup_driver")
    @patch("src.main.simple_scrape_test")
    @patch("src.main.take_screenshot")
    @patch("builtins.print")
    def test_main_scrape_failure(self, mock_print, mock_screenshot, mock_scrape, mock_setup_driver, mock_setup_logger):
        """Test main function with scraping failure."""
        # Mock setup
        mock_logger = Mock()
        mock_setup_logger.return_value = mock_logger

        mock_driver = Mock()
        mock_setup_driver.return_value = mock_driver

        mock_scrape.return_value = {"status": "error", "error": "Test error"}

        # Run main and expect system exit
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        mock_driver.quit.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    @patch("src.main.setup_logger")
    @patch("src.main.setup_driver")
    @patch("builtins.print")
    def test_main_driver_exception(self, mock_print, mock_setup_driver, mock_setup_logger):
        """Test main function with driver setup exception."""
        # Mock setup
        mock_logger = Mock()
        mock_setup_logger.return_value = mock_logger

        mock_setup_driver.side_effect = Exception("Driver failed")

        # Run main and expect system exit
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
