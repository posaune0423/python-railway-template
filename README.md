# 🚀 Python Railway Template with Selenium Standalone Chromium

Modern Python template for Railway deployment with **Selenium Standalone Chromium** using official Docker images. Clean architecture with modular design and beautiful colored logging!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

## ✨ Features

- **🐍 Python 3.12+** with type hints and modern syntax
- **⚡ uv** for lightning-fast dependency management  
- **🦀 Ruff** for blazing-fast linting and formatting
- **🐳 Lightweight Docker** builds (no browser installations needed)
- **🌐 Selenium Standalone** with official Chromium Docker images
- **🚂 Railway** deployment ready with proper configuration
- **🧪 Pytest** for comprehensive testing
- **📝 Makefile** for npm-style development commands
- **🎨 Beautiful colored logging** with icons and formatting
- **🏗️ Clean modular architecture** with separation of concerns

## 🌐 Why Selenium Standalone?

Traditional approaches require heavy browser installations in your application container. With **Selenium Standalone Chromium**:

- ✅ **Official Support**: SeleniumHQ maintained Docker images  
- ✅ **Lightweight Apps**: Your app container has no browser dependencies
- ✅ **ARM64 Compatible**: Uses `seleniarm/standalone-chromium` for M1 Macs
- ✅ **Visual Debugging**: VNC access to see browser actions live
- ✅ **Free & Local**: No external service dependencies
- ✅ **Production Ready**: Remote WebDriver architecture
- ✅ **Easy Management**: Single container setup

## 🏗️ Project Structure

```
src/
├── main.py              # 🎯 Clean entry point
├── scraper.py           # 🕷️ Scraping logic with context manager
└── utils/
    ├── __init__.py
    └── logger.py         # 🎨 Beautiful colored logging
```

### Key Components

- **`StandaloneChromiumScraper`**: Type-safe scraper class with context manager support
- **`ColoredFormatter`**: Beautiful console output with colors and icons
- **Environment-based config**: Easy deployment and testing

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository  
git clone https://github.com/your-username/your-project-name.git
cd your-project-name

# Install dependencies
uv sync
```

### 2. Start Selenium Standalone

```bash
# Start the full stack with docker-compose
make docker-up

# Or manually:
docker-compose up -d

# Check status
make grid-status
```

### 3. Run Scraping (One Command!)

```bash
# Run scraping with logs in one command
make scrape

# This will:
# 1. Start Selenium Standalone if not running
# 2. Build and run your Python app
# 3. Stream logs in real-time
# 4. Show beautiful colored output
```

## 🎨 Beautiful Logging Output

The new colored logger provides gorgeous console output:

```
2025-01-23 10:30:15 ✅ INFO Connecting to Selenium Standalone Chrome...
2025-01-23 10:30:16 ✅ INFO Connected successfully! Browser: chrome 131.0
2025-01-23 10:30:17 ✅ INFO Navigating to test page...
2025-01-23 10:30:18 ✅ INFO Test page scraped successfully  
2025-01-23 10:30:19 ✅ INFO Screenshot saved: reports/test_screenshot_20250123_103019.png
2025-01-23 10:30:20 ✅ INFO Remote WebDriver disconnected
```

## 🛠️ Development Commands

```bash
# 🧪 Testing
make test                    # Run all tests
make test-watch             # Run tests in watch mode

# 🦀 Code Quality  
make lint                   # Run linting
make format                 # Format code

# 🐳 Docker Management
make docker-up              # Start full stack
make docker-down            # Stop all containers
make docker-logs            # View all logs

# 🕷️ Selenium Operations
make grid-up                # Start Selenium Standalone
make grid-down              # Stop Selenium
make grid-status            # Check status
make grid-logs              # View Selenium logs

# 🚀 Scraping
make scrape                 # Run scraping with logs (recommended!)
make scrape-build           # Force rebuild and run  
make scrape-logs            # View app logs only
```

## 🔧 Configuration

### Environment Variables

```bash
# Selenium configuration
SELENIUM_REMOTE_URL=http://selenium:4444    # Selenium server URL
SELENIUM_BROWSER=chrome                     # Browser type (chrome/firefox)
```

### Docker Compose Services

- **`selenium`**: Standalone Chromium container
  - Port 4444: WebDriver API
  - Port 7900: VNC viewer (password: `secret`)
- **`python-app`**: Your application container

## 🖥️ Visual Debugging

Watch your scraper in action with VNC:

1. **Start the stack**: `make docker-up`
2. **Open VNC viewer**: http://localhost:7900
3. **Password**: `secret`
4. **Run scraping**: `make scrape`
5. **Watch live**: See browser actions in real-time!

## 🧪 Testing

The project includes comprehensive tests for all components:

```bash
# Run all tests
make test

# Run specific test categories
uv run python -m pytest tests/test_main.py -v        # Main module tests
uv run python -m pytest tests/ -k "logger" -v       # Logger tests  
uv run python -m pytest tests/ -k "scraper" -v      # Scraper tests
```

## 📦 Usage Examples

### Basic Scraping

```python
from src.scraper import create_scraper_from_env

# Using context manager (recommended)
with create_scraper_from_env() as scraper:
    result = scraper.scrape_test_page()
    screenshot = scraper.take_screenshot("my_screenshot.png")
    print(f"Title: {result['title']}")
```

### Custom Scraper

```python
from src.scraper import StandaloneChromiumScraper

# Custom configuration
scraper = StandaloneChromiumScraper(
    browser="chrome",
    remote_url="http://localhost:4444",
    timeout=30
)

scraper.connect()
try:
    result = scraper.scrape_test_page()
finally:
    scraper.disconnect()
```

### Colored Logging

```python
from src.utils.logger import get_app_logger

logger = get_app_logger(__name__)

logger.info("✅ This will be green with an icon!")
logger.warning("⚠️ This will be yellow with an icon!")  
logger.error("❌ This will be red with an icon!")
```

## 🚂 Railway Deployment

### 1. Prepare for Deploy

```bash
# Ensure your code is committed
git add .
git commit -m "Ready for Railway deployment"
```

### 2. Deploy Options

**Option A: Use Railway Button**
1. Click the Railway button above
2. Connect your GitHub account
3. Deploy automatically

**Option B: Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 3. Environment Setup

Set these environment variables in Railway:

```
SELENIUM_REMOTE_URL=http://selenium:4444
SELENIUM_BROWSER=chrome
```

> **Note**: For Railway deployment, you might need to adjust the Selenium service configuration based on Railway's Docker support.

## 🔍 Troubleshooting

### Common Issues

**1. Selenium not connecting**
```bash
# Check if containers are running
docker ps

# Check logs
make grid-logs

# Restart services
make docker-down && make docker-up
```

**2. VNC not accessible**
```bash
# Check port mapping
docker-compose ps

# Ensure port 7900 is available
lsof -i :7900
```

**3. ARM64 (M1 Mac) Issues**
The project automatically uses `seleniarm/standalone-chromium` for ARM environments. If you encounter issues:

```bash
# Force pull ARM image
docker pull seleniarm/standalone-chromium:latest

# Clear Docker cache
docker system prune -a
```

**4. Tests failing**
```bash
# Install test dependencies
uv sync --dev

# Run with verbose output
make test
```

## 🎯 Next Steps

Ready to customize for your needs?

1. **Add more scrapers**: Create new methods in `StandaloneChromiumScraper`
2. **Custom logging**: Extend `ColoredFormatter` with your own styles
3. **Database integration**: Add SQLAlchemy or other ORMs
4. **API endpoints**: Add FastAPI for web service functionality
5. **Scheduled jobs**: Add cron or background task processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy Scraping!** 🕷️✨

> Built with ❤️ using modern Python tooling and official Selenium Docker images.
