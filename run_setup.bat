# run_setup.bat (Windows batch file)
@echo off
echo Setting up AI-Enhanced Search Simulator...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Installing Playwright browsers...
python -m playwright install

echo.
echo Running setup script...
python setup_models.py

echo.
echo Setup complete!
echo Run: python fixed_integrated_agent.py --check-integration
pause

# run_setup.sh (Unix shell script)
#!/bin/bash
echo "Setting up AI-Enhanced Search Simulator..."
echo

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo
echo "Installing Playwright browsers..."
python -m playwright install

echo
echo "Running setup script..."
python setup_models.py

echo
echo "Setup complete!"
echo "Run: python fixed_integrated_agent.py --check-integration"