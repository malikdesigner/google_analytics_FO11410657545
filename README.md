# Enhanced Human-like Google Search Simulator

A sophisticated web automation tool that simulates realistic human browsing behavior for Google searches. The system performs searches with human-like patterns, explores search results, and visits target websites with authentic user interactions.

## Features

🎭 **Realistic User Behavior Modeling**
- Multiple persona types (researcher, casual browser, professional, student, senior, tech-savvy, bargain hunter)
- Human-like typing patterns with realistic delays and hesitations
- Natural mouse movements and hovering behavior
- Authentic scrolling and reading patterns

🖱️ **Human-like Interactions**
- Link hovering with persona-specific tendencies
- Natural page exploration patterns
- Form interaction simulation
- Cognitive fatigue modeling

🧠 **Advanced Model Integration**
- AutoWebGLM integration for intelligent page analysis
- USimAgent for cognitive state modeling
- Enhanced persona management system
- Behavioral pattern adaptation

🌐 **Dual Browser Support**
- **Browserless (Browserbase)**: Cloud-based browser automation with proxy support
- **Chromium**: Local browser automation with stealth capabilities

📊 **Comprehensive Analytics**
- Detailed session tracking and metrics
- Human-like activity logging
- Performance monitoring
- Success rate analysis

## Architecture

The system consists of several modular components:

- `main.py` - Main entry point and orchestration
- `model_integration.py` - AI model integration and persona management
- `google_activity.py` - Google search simulation and SERP interaction
- `site_activity.py` - Target site browsing and exploration
- `browserless_connection.py` - Browserless/Browserbase integration
- `utils.py` - Utility functions and logging

## Installation

### Prerequisites

```bash
# Python 3.8 or higher required
python --version
```

### Install Dependencies

```bash
# Install required packages
pip install playwright
pip install requests
pip install playwright-stealth

# Install Playwright browsers
playwright install
playwright install-deps
```

### Optional Dependencies

```bash
# For enhanced AI model integration (if available)
pip install torch
pip install transformers
pip install numpy
```

## Configuration

### Browserless Setup

The system uses Browserbase for cloud browser automation. Update credentials in `browserless_connection.py`:

```python
API_KEY = 'your_browserbase_api_key'
PROJECT_ID = 'your_project_id'
```

### ProxyJet Configuration (Optional)

For enhanced anonymity, configure proxy settings:

```python
PROXY_CONFIG = {
    'server': 'proxy-jet.io',
    'port': 1010,
    'username': 'your_username',
    'password': 'your_password'
}
```

## Usage

### Input Format

Create a `searches.json` file with search tasks:

```json
[
    {"keyword": "dental implants london", "site": "https://example-clinic.com"},
    {"keyword": "invisalign treatment", "site": "https://dental-practice.co.uk"},
    {"keyword": "teeth whitening near me", "site": "https://cosmetic-dentist.com"}
]
```

### Basic Commands

#### Using Browserless (Recommended)
```bash
python main.py searches.json browserless
```

#### Using Local Chromium
```bash
python main.py searches.json chromium
```

#### Advanced Options

```bash
# Custom delay between searches (seconds)
python main.py searches.json browserless --delay 300

# Custom output file
python main.py searches.json browserless --output results_custom.json

# Randomize search order
python main.py searches.json browserless --randomize

# Specific persona
python main.py searches.json browserless --persona researcher
```

### Single Search Mode

```bash
# Single search with Browserless
python main.py --single "keyword here" "https://target-site.com"

# Single search with Chromium
python main.py --single "keyword here" "https://target-site.com" chromium
```

### Utility Commands

```bash
# Create sample JSON file
python main.py --create-sample

# Validate Browserless configuration
python main.py --validate
```

## Persona Types

The system includes 7 distinct user personas:

| Persona | Speed | Attention | Tech Comfort | Reading Pattern |
|---------|-------|-----------|--------------|-----------------|
| **Researcher** | Slow | Long | High | Thorough |
| **Casual Browser** | Fast | Short | Medium | Skimmer |
| **Professional** | Medium | Medium | High | Focused |
| **Student** | Medium | Medium | High | Thorough |
| **Senior** | Slow | Long | Low | Thorough |
| **Tech Savvy** | Fast | Medium | High | Scanner |
| **Bargain Hunter** | Fast | Short | Medium | Scanner |

## Output

The system generates comprehensive results including:

### JSON Results File
```json
{
  "total_searches": 10,
  "successful_searches": 8,
  "success_rate": 80.0,
  "total_human_activities": 156,
  "persona_distribution": {
    "researcher": 2,
    "casual_browser": 3,
    "professional": 2
  },
  "results": [...]
}
```

### Summary Report
- Performance metrics
- Human-like behavior statistics
- Persona distribution analysis
- Browser backend usage
- Detailed activity logs

## Browser Backends

### Browserless (Browserbase)
- **Advantages**: Cloud-based, proxy support, scalable, no local resources
- **Use case**: Production environments, large-scale operations
- **Requirements**: Browserbase API key and project ID

### Chromium (Local)
- **Advantages**: Full control, no external dependencies, faster for small batches
- **Use case**: Development, testing, small-scale operations
- **Requirements**: Local Playwright installation

## Human-like Behaviors

The system simulates authentic human behaviors:

### Typing Patterns
- Variable typing speed with realistic delays
- Hesitations and corrections
- Faster typing for common letter combinations
- Pauses at word boundaries

### Mouse Movements
- Natural curved paths to elements
- Human-like hovering durations
- Fidgeting and micro-movements
- Realistic click timing

### Browsing Patterns
- Persona-specific reading speeds
- Natural scrolling with pauses
- Element exploration based on user type
- Cognitive fatigue modeling

### Cognitive States
- Working memory limitations
- Attention decay over time
- Decision-making delays
- Interest level fluctuations

## Troubleshooting

### Common Issues

#### Browserless Connection Failed
```bash
# Check configuration
python main.py --validate

# Try Chromium fallback
python main.py searches.json chromium
```

#### Playwright Installation Issues
```bash
# Reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install
```

#### Module Import Errors
```bash
# Check Python path and module structure
python -c "import sys; print(sys.path)"
```

### Debug Mode

Enable detailed logging by modifying `utils.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Project Structure
```
├── main.py                     # Entry point
├── model_integration.py        # AI models and personas
├── google_activity.py         # Google search automation
├── site_activity.py           # Website interaction
├── browserless_connection.py  # Cloud browser management
├── utils.py                   # Utilities and logging
├── searches.json              # Input data
└── modals/                    # AI model implementations
    ├── AutoWebGLM/
    └── USimAgent/
```

### Extending Personas

Add new personas in `model_integration.py`:

```python
UserPersonaType.NEW_PERSONA = "new_persona"

PERSONAS[UserPersonaType.NEW_PERSONA] = UserPersona(
    persona_type=UserPersonaType.NEW_PERSONA,
    name="New Persona Name",
    # ... other attributes
)
```

### Custom Behaviors

Implement custom behaviors in the respective modules:
- Search behaviors: `google_activity.py`
- Site interactions: `site_activity.py`
- Cognitive modeling: `model_integration.py`

## Performance Optimization

### Browserless Optimization
- Use session pooling for multiple searches
- Implement request batching
- Configure appropriate timeouts
- Monitor usage quotas

### Chromium Optimization
- Limit concurrent browser instances
- Use headless mode for production
- Implement proper cleanup
- Monitor system resources

## Security Considerations

- Rotate proxy configurations regularly
- Use diverse user agents and device profiles
- Implement rate limiting between requests
- Monitor for detection patterns

## License

This project is for educational and research purposes. Ensure compliance with website terms of service and applicable laws when using this tool.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files for error details
3. Validate configuration with `--validate` flag
4. Test with single search mode first

---

**Note**: This tool simulates human browsing behavior and should be used responsibly and in compliance with website terms of service and applicable laws.
