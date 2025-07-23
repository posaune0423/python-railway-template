# 🚀 Python Railway Template with Selenium Grid

Modern Python template for Railway deployment with **official Selenium Grid** Docker containers. No external services needed - everything runs locally with Docker Compose!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

## ✨ Features

- **🐍 Python 3.12+** with type hints and modern syntax
- **⚡ uv** for lightning-fast dependency management
- **🦀 Ruff** for blazing-fast linting and formatting
- **🐳 Lightweight Docker** builds (no browser installations needed)
- **🌐 Selenium Grid** with official Docker images
- **🚂 Railway** deployment ready with proper configuration
- **🧪 Pytest** for comprehensive testing
- **📝 Makefile** for npm-style development commands
- **🔧 Example Selenium scraper** using Grid architecture

## 🌐 Why Selenium Grid?

Traditional approaches require heavy browser installations in your application container. With **Selenium Grid**:

- ✅ **Official Support**: SeleniumHQ maintained Docker images
- ✅ **Lightweight Apps**: Your app container has no browser dependencies
- ✅ **Multiple Browsers**: Chrome, Firefox, Edge support
- ✅ **Scalable**: Easy horizontal scaling
- ✅ **Visual Debugging**: VNC access to see browser actions
- ✅ **Free & Local**: No external service dependencies
- ✅ **Production Ready**: Used by enterprises worldwide

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-username/your-project-name.git
cd your-project-name

# Install dependencies
uv sync
```

### 2. Start Selenium Grid

```bash
# Start the full stack with docker-compose
docker-compose up -d

# Check Grid status
open http://localhost:4444
```

### 3. Run the Example

```bash
# Run with Chrome (default)
make run

# Or specify Firefox
SELENIUM_BROWSER=firefox make run
```

## 🛠️ Development Workflow

### Option 1: Direct uv commands (Fastest)
```bash
uv run ruff format src/      # Format code
uv run ruff check src/       # Lint code
uv run ruff check --fix src/ # Auto-fix issues
uv run python -m pytest     # Run tests
uv run app                   # Run application
```

### Option 2: Makefile commands (npm-style)
```bash
make format      # Format code
make lint        # Lint code  
make lint-fix    # Auto-fix issues
make test        # Run tests
make run         # Run application
make help        # Show all commands
```

## 🐳 Docker & Deployment

### Local Development with Docker Compose

```bash
# Start Selenium Grid and all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down
```

### Grid Services Overview

- **Selenium Hub**: `http://localhost:4444` - Grid console
- **Chrome VNC**: `http://localhost:7900` - Watch Chrome browser
- **Firefox VNC**: `http://localhost:7901` - Watch Firefox browser
- **VNC Password**: `secret`

### Railway Deployment

#### Option 1: One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

#### Option 2: Manual Deploy
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up
```

**Note**: For Railway deployment, you might want to use a managed Selenium service or deploy Grid separately.

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `SELENIUM_HUB_URL` | Selenium Grid Hub URL | `http://localhost:4444` | Any Grid URL |
| `SELENIUM_BROWSER` | Browser to use | `chrome` | `chrome`, `firefox` |

### Docker Compose Configuration

The `docker-compose.yml` includes:
- **Selenium Hub**: Central coordination
- **Chrome Node**: Chrome browser instances
- **Firefox Node**: Firefox browser instances
- **App Container**: Your Python application

### Browser Options

```bash
# Use Chrome (default)
SELENIUM_BROWSER=chrome make run

# Use Firefox
SELENIUM_BROWSER=firefox make run

# Custom Grid URL
SELENIUM_HUB_URL=http://remote-grid:4444 make run
```

## 📁 Project Structure

```
python-railway-template/
├── src/
│   ├── __init__.py         # Package initialization
│   └── main.py             # Selenium Grid logic
├── tests/                  # Test files
├── reports/                # Screenshots and outputs
├── docker-compose.yml      # Selenium Grid setup
├── Dockerfile              # Lightweight app container
├── Makefile               # Development commands
├── railway.toml           # Railway deployment config
├── pyproject.toml         # Project configuration
├── uv.lock               # Locked dependencies
└── README.md             # This file
```

## 🧪 Example Application

The template includes a **Selenium Grid scraper** that:
- ✅ Connects to local Selenium Grid
- ✅ Supports Chrome and Firefox browsers
- ✅ Takes screenshots automatically
- ✅ Provides VNC access for debugging
- ✅ Handles errors gracefully
- ✅ Scales with Grid nodes

### Visual Debugging

Watch your automation in real-time:

1. **Start the grid**: `docker-compose up -d`
2. **Open VNC viewer**: `http://localhost:7900` (Chrome) or `http://localhost:7901` (Firefox)
3. **Password**: `secret`
4. **Run your tests**: `make run`

## 🎯 Selenium Code Example

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def setup_grid_driver():
    hub_url = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444")
    browser = os.getenv("SELENIUM_BROWSER", "chrome")
    
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        capabilities = options.to_capabilities()
        capabilities['browserName'] = 'chrome'
    
    driver = webdriver.Remote(
        command_executor=f"{hub_url}/wd/hub",
        desired_capabilities=capabilities
    )
    
    return driver

# Usage
driver = setup_grid_driver()
driver.get("https://example.com")
driver.save_screenshot("screenshot.png")
driver.quit()
```

## 💰 Cost & Resource Comparison

### Traditional Approach (Heavy containers)
- **App Container**: 1.2GB (with Chrome/Firefox)
- **Memory**: 512MB+ per container
- **Complexity**: High maintenance
- **Scaling**: Resource intensive

### Selenium Grid Approach
- **App Container**: ~100MB (no browsers)
- **Grid Containers**: Separate, optimized containers
- **Memory**: 64MB app + 256MB per browser node
- **Complexity**: Simple, standard architecture
- **Scaling**: Independent scaling of app vs browsers

## 📝 Available Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install dependencies |
| `make dev` | Install dev dependencies |
| `make format` | Format code with ruff |
| `make lint` | Lint code with ruff |
| `make lint-fix` | Auto-fix lint issues |
| `make check` | Run both lint and format check |
| `make test` | Run tests |
| `make run` | Run the application |
| `make grid-up` | Start Selenium Grid |
| `make grid-down` | Stop Selenium Grid |
| `make grid-logs` | View Grid logs |
| `make clean` | Clean cache files |
| `make docker-build` | Build app Docker image |

## 🔧 Customizing for Your Project

### 1. Update Project Metadata
```toml
# pyproject.toml
[project]
name = "your-scraper-project"
description = "Your web scraping application"
```

### 2. Add Dependencies
```bash
uv add requests beautifulsoup4 pandas
uv add --dev pytest-mock pytest-asyncio
```

### 3. Configure Grid Scaling
```yaml
# docker-compose.yml
chrome:
  # ... existing config
  deploy:
    replicas: 3  # Scale Chrome nodes
```

### 4. Custom Browser Options
```python
# Enhanced Chrome options
options = ChromeOptions()
options.add_argument("--disable-images")
options.add_argument("--disable-javascript")
options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.images": 2
})
```

## 🚨 Troubleshooting

### Common Issues

**Grid not starting**
```bash
# Check Docker
docker-compose ps

# View logs
docker-compose logs selenium-hub
```

**Connection refused**
```bash
# Verify Grid is running
curl http://localhost:4444/status

# Check Grid console
open http://localhost:4444
```

**Browser node issues**
```bash
# Check node registration
docker-compose logs chrome
docker-compose logs firefox

# Restart nodes
docker-compose restart chrome firefox
```

### Grid Health Check
```bash
# Check Grid status
curl -s http://localhost:4444/status | jq .

# View Grid console
open http://localhost:4444/ui#/sessions
```

## 🎯 Use Cases

This template is perfect for:

- **🕷️ Web scraping** at scale
- **🧪 E2E testing** with real browsers
- **📊 Data collection** from dynamic sites
- **📱 Cross-browser testing**
- **📈 Performance monitoring**
- **🤖 Browser automation**
- **📰 Content aggregation**
- **🛒 Price monitoring**

## 🚀 Getting Started Checklist

- [ ] Clone this repository
- [ ] Run `uv sync` to install dependencies
- [ ] Start Grid with `docker-compose up -d`
- [ ] Verify Grid at `http://localhost:4444`
- [ ] Test with `make run`
- [ ] Watch browser via VNC at `http://localhost:7900`
- [ ] Customize for your use case
- [ ] Deploy to Railway or your preferred platform

## 🤝 Contributing

Feel free to submit issues and enhancement requests! This template is designed to be:
- **Simple** but powerful
- **Standards-based** using official Selenium images
- **Production-ready** out of the box
- **Extensible** for any automation project

## 📄 License

This template is open source and available under the [MIT License](LICENSE).

---

**Happy automating! 🤖**

*This template provides a robust, scalable foundation for browser automation using industry-standard Selenium Grid architecture.*
# python-railway-template
