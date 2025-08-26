# browserless_connection.py - FIXED VERSION
"""
Browserless Connection Module - Fixed Authentication
Matches the working Selenium authentication pattern
"""

import requests
import logging
import time
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright

class BrowserlessConnection:
    """Manages Browserless (Browserbase) connections with corrected authentication"""
    
    # Your Browserbase credentials
    API_KEY = 'bb_live_0023b70-H7IN0Os28_64CFdxD_w'
    PROJECT_ID = '971fa12e-7c28-4d3d-93e1-deaa71c3a54e'
    
    # ProxyJet configuration
    PROXY_CONFIG = {
        'server': 'proxy-jet.io',  # Note: using 'server' key like working code
        'port': 1010,
        'username': '250711x85UA',
        'password': '7XFTkTMop6RqdNP'
    }
    
    def __init__(self, use_proxy: bool = True):
        self.use_proxy = use_proxy
        self.session_data = None
        self.session_id = None
        self.connect_url = None
        
        logging.info(f"🌐 Initializing Browserless connection (Proxy: {'ON' if use_proxy else 'OFF'})")
    
    def create_session(self) -> bool:
        """Create a new Browserbase session using WORKING authentication method"""
        url = "https://api.browserbase.com/v1/sessions"
        
        # Use the SAME headers format as your working Selenium code
        headers = {
            "Content-Type": "application/json",
            "X-BB-API-Key": self.API_KEY  # Changed from Bearer to X-BB-API-Key
        }
        
        # Use EXACT payload structure as working Selenium code
        payload = {
            "projectId": self.PROJECT_ID
        }
        
        # Add proxy configuration if enabled (using EXACT working format)
        if self.use_proxy:
            payload["browserSettings"] = {
                "proxy": {
                    "server": f"http://{self.PROXY_CONFIG['username']}:{self.PROXY_CONFIG['password']}@{self.PROXY_CONFIG['server']}:{self.PROXY_CONFIG['port']}"
                }
            }
            logging.info(f"🔗 Using proxy: {self.PROXY_CONFIG['server']}:{self.PROXY_CONFIG['port']}")
        
        try:
            logging.info("🚀 Creating Browserbase session with corrected authentication...")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code in [200, 201]:
                self.session_data = response.json()
                self.session_id = self.session_data.get('id')
                self.connect_url = self.session_data.get('connectUrl')
                
                logging.info(f"✅ Browserbase session created successfully")
                logging.info(f"📋 Session ID: {self.session_id}")
                logging.info(f"🔗 Status: {self.session_data.get('status', 'active')}")
                
                return True
            else:
                logging.error(f"❌ Failed to create Browserbase session")
                logging.error(f"Status: {response.status_code}")
                logging.error(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            logging.error("❌ Browserbase session creation timed out")
            return False
        except requests.exceptions.ConnectionError:
            logging.error("❌ Connection error to Browserbase")
            return False
        except Exception as e:
            logging.error(f"❌ Browserbase session creation failed: {e}")
            return False
    
    async def connect_browser(self, playwright=None):
        """Connect to the created Browserbase session"""
        if not self.connect_url:
            logging.error("❌ No connect URL available. Create session first.")
            return None, None, None
        
        if not playwright:
            playwright = await async_playwright().start()
        
        try:
            logging.info("🔌 Connecting to Browserbase session...")
            browser = await playwright.chromium.connect_over_cdp(self.connect_url)
            
            # Get existing context or create new one
            contexts = browser.contexts
            if contexts:
                context = contexts[0]
            else:
                context = await browser.new_context()
            
            # Get or create page
            pages = context.pages
            if pages:
                page = pages[0]
            else:
                page = await context.new_page()
            
            # Navigate to Google as starting point
            await page.goto("https://www.google.com", wait_until='networkidle', timeout=30000)
            
            logging.info("✅ Successfully connected to Browserbase session")
            return page, browser, playwright
            
        except Exception as e:
            logging.error(f"❌ Failed to connect to Browserbase session: {e}")
            if playwright:
                await playwright.stop()
            return None, None, None
    
    def close_session(self) -> bool:
        """Close the Browserbase session using corrected authentication"""
        if not self.session_id:
            logging.warning("⚠️ No session to close")
            return True
        
        url = f"https://api.browserbase.com/v1/sessions/{self.session_id}"
        headers = {
            "X-BB-API-Key": self.API_KEY  # Changed from Authorization Bearer
        }
        
        try:
            logging.info(f"🛑 Closing Browserbase session: {self.session_id}")
            response = requests.delete(url, headers=headers, timeout=10)
            
            if response.status_code in [200, 204]:
                logging.info("✅ Browserbase session closed successfully")
                self.session_data = None
                self.session_id = None
                self.connect_url = None
                return True
            else:
                logging.warning(f"⚠️ Failed to close session: {response.status_code}")
                return False
                
        except Exception as e:
            logging.warning(f"⚠️ Error closing session: {e}")
            return False
    
    def is_session_active(self) -> bool:
        """Check if session is active using corrected authentication"""
        if not self.session_id:
            return False
        
        url = f"https://api.browserbase.com/v1/sessions/{self.session_id}"
        headers = {
            "X-BB-API-Key": self.API_KEY  # Changed from Authorization Bearer
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "").lower()
                return status in ["running", "active"]
            return False
        except:
            return False
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        if not self.session_data:
            return {}
        
        return {
            "session_id": self.session_id,
            "status": self.session_data.get("status"),
            "connect_url": self.connect_url,
            "proxy_enabled": self.use_proxy,
            "proxy_server": self.PROXY_CONFIG['server'] if self.use_proxy else None,
            "created_at": self.session_data.get("createdAt"),
            "project_id": self.PROJECT_ID
        }
    
    def __enter__(self):
        """Context manager entry"""
        if self.create_session():
            return self
        else:
            raise ConnectionError("Failed to create Browserbase session")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_session()
    
    def __del__(self):
        """Destructor - ensure session is closed"""
        if self.session_id:
            try:
                self.close_session()
            except:
                pass

# Configuration validation using corrected method
def validate_configuration() -> bool:
    """Validate Browserless configuration using corrected authentication"""
    connection = BrowserlessConnection()
    
    print("🔍 BROWSERLESS CONFIGURATION VALIDATION (FIXED)")
    print("=" * 50)
    
    print(f"📋 API Key: {connection.API_KEY[:20]}...")
    print(f"🆔 Project ID: {connection.PROJECT_ID}")
    print(f"🔗 Proxy Server: {connection.PROXY_CONFIG['server']}")
    print(f"🔢 Proxy Port: {connection.PROXY_CONFIG['port']}")
    print(f"👤 Proxy User: {connection.PROXY_CONFIG['username']}")
    print(f"🔐 Authentication: X-BB-API-Key (Fixed)")
    
    # Test session creation
    print("\n🧪 Testing session creation...")
    if connection.create_session():
        print("✅ Session creation: SUCCESS")
        
        info = connection.get_session_info()
        print(f"🆔 Session ID: {info['session_id']}")
        print(f"📊 Status: {info['status']}")
        
        connection.close_session()
        print("✅ Session cleanup: SUCCESS")
        print("\n🎉 Configuration is now FIXED and valid!")
        return True
    else:
        print("❌ Session creation: STILL FAILED")
        print("\n⚠️ Check if API key has expired or account has issues")
        return False

if __name__ == "__main__":
    # Run configuration validation with fix
    print("🚀 Testing FIXED Browserbase authentication...")
    validate_configuration()