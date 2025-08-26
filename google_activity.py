#google_activity.py
"""
GOOGLE ACTIVITY MODULE
Handles Google search interactions with human-like behavior
Now supports both Chromium and Browserless backends
"""

import asyncio
import random
import time
import logging
import requests
from datetime import datetime
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from typing import Dict, Any, Optional

try:
    from playwright_stealth import stealth_async
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False

from model_integration import UserPersona

class BrowserlessManager:
    """Manages Browserless session creation and configuration"""
    
    def __init__(self, api_key: str, project_id: str, proxy_config: Dict = None):
        self.api_key = api_key
        self.project_id = project_id
        self.proxy_config = proxy_config
        self.session_data = None
    
    def create_session(self) -> bool:
        """Create Browserless session with enhanced configuration"""
        url = "https://api.browserbase.com/v1/sessions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "projectId": self.project_id,
            "browser": "chrome",
            "viewport": {"width": 1280, "height": 800}
        }
        
        # Add proxy configuration if provided
        if self.proxy_config:
            payload["proxy"] = {
                "type": "http",
                "host": self.proxy_config['host'],
                "port": self.proxy_config['port'],
                "username": self.proxy_config['username'],
                "password": self.proxy_config['password']
            }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code in [200, 201]:
                self.session_data = response.json()
                logging.info(f"✅ Browserless session created: {self.session_data.get('id')}")
                logging.info(f"Status: {self.session_data.get('status', 'active')}")
                
                # Log proxy usage
                if self.proxy_config:
                    logging.info(f"🔗 Using proxy: {self.proxy_config['host']}:{self.proxy_config['port']}")
                
                return True
            else:
                logging.error(f"❌ Failed to create Browserless session: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logging.error(f"❌ Browserless session creation exception: {e}")
            return False
    
    def get_connect_url(self) -> str:
        """Get the WebSocket URL for connecting to the session"""
        if self.session_data:
            return self.session_data.get('connectUrl', '')
        return ''
    
    def close_session(self) -> bool:
        """Close the Browserless session"""
        if not self.session_data:
            return True
        
        session_id = self.session_data.get('id')
        url = f"https://api.browserbase.com/v1/sessions/{session_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.delete(url, headers=headers)
            if response.status_code in [200, 204]:
                logging.info(f"✅ Browserless session closed: {session_id}")
                return True
            else:
                logging.warning(f"⚠️ Failed to close Browserless session: {response.status_code}")
                return False
        except Exception as e:
            logging.warning(f"⚠️ Exception closing Browserless session: {e}")
            return False

class GoogleSearchSimulator:
    """Google Search Simulator with enhanced human-like behavior and Browserless support"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.use_browserless = self.config.get('use_browserless', True)
    
    async def create_enhanced_browser(self, persona: UserPersona):
        """Create browser with enhanced persona-specific configuration (Chromium only)"""
        
        if self.use_browserless:
            logging.warning("⚠️ create_enhanced_browser called for Browserless - should use separate connection")
        
        return await self._create_chromium_browser(None, persona)
    
    async def _create_browserless_browser(self, playwright, persona: UserPersona):
        """Create browser using Browserless"""
        
        logging.info("🌐 Creating Browserless browser session")
        
        # Initialize Browserless manager
        self.browserless_manager = BrowserlessManager(
            api_key=self.browserless_api_key,
            project_id=self.browserless_project_id,
            proxy_config=self.proxy_config
        )
        
        # Create session
        if not self.browserless_manager.create_session():
            logging.error("❌ Failed to create Browserless session, falling back to Chromium")
            return await self._create_chromium_browser(playwright, persona)
        
        # Get connection URL
        connect_url = self.browserless_manager.get_connect_url()
        if not connect_url:
            logging.error("❌ No Browserless connect URL, falling back to Chromium")
            return await self._create_chromium_browser(playwright, persona)
        
        try:
            # Connect to existing browser
            browser = await playwright.chromium.connect_over_cdp(connect_url)
            
            # Enhanced device configurations
            device_configs = self._get_device_configs()
            preferred_device = random.choice(persona.device_preferences)
            config = random.choice(device_configs[preferred_device])
            
            # Enhanced user agent generation
            user_agent = self._generate_realistic_user_agent(persona, preferred_device)
            
            # Create context with persona-specific settings
            context = await browser.new_context(
                viewport=config["viewport"],
                user_agent=user_agent,
                device_scale_factor=config["device_scale_factor"],
                locale="en-US",
                timezone_id="America/New_York"
            )
            
            page = await context.new_page()
            
            if STEALTH_AVAILABLE:
                await stealth_async(page)
            
            logging.info("✅ Browserless browser created successfully")
            return page, browser, playwright
            
        except Exception as e:
            logging.error(f"❌ Browserless connection failed: {e}, falling back to Chromium")
            return await self._create_chromium_browser(playwright, persona)
    
    async def _create_chromium_browser(self, playwright, persona: UserPersona):
        """Create browser using local Chromium"""
        
        if not playwright:
            playwright = await async_playwright().start()
        
        logging.info("🖥️ Creating local Chromium browser")
        
        # Enhanced device configurations
        device_configs = self._get_device_configs()
        preferred_device = random.choice(persona.device_preferences)
        config = random.choice(device_configs[preferred_device])
        
        # Enhanced user agent generation
        user_agent = self._generate_realistic_user_agent(persona, preferred_device)
        
        # Browser launch with human-like settings
        browser = await playwright.chromium.launch(
            headless=False,  # Set to True for production
            slow_mo=self._calculate_slow_mo(persona),
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-automation',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding'
            ]
        )
        
        context = await browser.new_context(
            viewport=config["viewport"],
            user_agent=user_agent,
            device_scale_factor=config["device_scale_factor"],
            locale="en-US",
            timezone_id="America/New_York"
        )
        
        page = await context.new_page()
        
        if STEALTH_AVAILABLE:
            await stealth_async(page)
        
        logging.info("✅ Chromium browser created successfully")
        return page, browser, playwright
    
    def _get_device_configs(self) -> Dict:
        """Get device configurations"""
        return {
            "desktop": [
                {"viewport": {"width": 1920, "height": 1080}, "device_scale_factor": 1},
                {"viewport": {"width": 1366, "height": 768}, "device_scale_factor": 1},
                {"viewport": {"width": 1440, "height": 900}, "device_scale_factor": 1}
            ],
            "laptop": [
                {"viewport": {"width": 1366, "height": 768}, "device_scale_factor": 1},
                {"viewport": {"width": 1440, "height": 900}, "device_scale_factor": 1}
            ],
            "mobile": [
                {"viewport": {"width": 375, "height": 667}, "device_scale_factor": 2},
                {"viewport": {"width": 414, "height": 896}, "device_scale_factor": 3}
            ]
        }
    
    def _calculate_slow_mo(self, persona: UserPersona) -> int:
        """Calculate slow motion delay based on persona"""
        if persona.browsing_speed == "fast":
            return random.randint(50, 100)
        elif persona.browsing_speed == "slow":
            return random.randint(150, 300)
        else:
            return random.randint(100, 200)
    
    def _generate_realistic_user_agent(self, persona: UserPersona, device: str) -> str:
        """Generate realistic user agent based on persona and device"""
        
        if persona.tech_comfort == "high":
            chrome_versions = ["120.0.0.0", "119.0.0.0", "121.0.0.0"]
        else:
            chrome_versions = ["118.0.0.0", "117.0.0.0", "119.0.0.0"]
        
        version = random.choice(chrome_versions)
        
        if device == "mobile":
            return f"Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{version} Mobile/15E148 Safari/604.1"
        else:
            os_options = [
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
            ]
            return random.choice(os_options)
    
    async def navigate_to_google(self, page, session_data: Dict):
        """Navigate to Google with human-like behavior"""
        
        logging.info("Navigating to Google with human-like timing")
        
        await page.goto("https://www.google.com", wait_until='networkidle', timeout=30000)
        
        # Human-like pause after page load
        await asyncio.sleep(random.uniform(1.5, 4.0))
        
        session_data["steps"].append({
            "action": "navigate_to_google",
            "timestamp": datetime.now().isoformat(),
            "browser_type": "browserless" if self.use_browserless else "chromium",
            "success": True
        })
    
    async def perform_enhanced_search(self, page, keyword: str, session_data: Dict):
        """Perform search with enhanced human-like typing behavior"""
        
        logging.info(f"Performing enhanced search for: '{keyword}'")
        
        # Find search box with multiple strategies
        search_box = await self._find_search_box_enhanced(page)
        if not search_box:
            raise Exception("Search box not found")
        
        # Human-like approach to search box
        await self._human_like_element_approach(page, search_box)
        
        # Click search box
        await search_box.click()
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Enhanced typing behavior
        await self._enhanced_typing_behavior(page, keyword)
        
        # Human-like pause before submitting
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Submit search
        await page.keyboard.press("Enter")
        await page.wait_for_load_state('networkidle', timeout=20000)
        
        session_data["steps"].append({
            "action": "perform_enhanced_search",
            "keyword": keyword,
            "typing_style": "human_like",
            "browser_type": "browserless" if self.use_browserless else "chromium",
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
    
    async def _find_search_box_enhanced(self, page):
        """Enhanced search box finding with multiple strategies"""
        
        selectors = [
            "input[name='q']",
            "textarea[name='q']",
            ".gLFyf",
            "#APjFqb",
            "input[title*='Search']",
            "textarea[title*='Search']"
        ]
        
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if await element.count() > 0 and await element.is_visible():
                    return element
            except:
                continue
        
        return None
    
    async def _human_like_element_approach(self, page, element):
        """Human-like mouse movement to element"""
        
        try:
            # Get element position
            box = await element.bounding_box()
            if box:
                # Move mouse in a slightly curved path
                target_x = box['x'] + box['width'] / 2
                target_y = box['y'] + box['height'] / 2
                
                # Add some randomness to the target
                target_x += random.uniform(-10, 10)
                target_y += random.uniform(-5, 5)
                
                # Move mouse with human-like speed
                await page.mouse.move(target_x, target_y)
                await asyncio.sleep(random.uniform(0.1, 0.3))
        except:
            pass
    
    async def _enhanced_typing_behavior(self, page, text: str):
        """Enhanced human-like typing with realistic patterns"""
        
        # Clear any existing text
        await page.keyboard.press("Control+A")
        await asyncio.sleep(0.1)
        
        # Calculate typing characteristics based on current context
        base_delay = random.uniform(0.08, 0.15)  # Base typing speed
        
        for i, char in enumerate(text):
            # Variable typing speed with realistic patterns
            char_delay = base_delay * random.uniform(0.7, 1.3)
            
            # Longer pauses at word boundaries
            if char == ' ':
                char_delay *= random.uniform(1.5, 3.0)
            
            # Occasional hesitations (more realistic)
            if random.random() < 0.08:
                char_delay *= random.uniform(2, 4)
            
            # Faster typing for common letter combinations
            if i > 0 and text[i-1:i+1].lower() in ['th', 'he', 'in', 'er', 'an']:
                char_delay *= 0.8
            
            # Slight pause after punctuation
            if char in '.,;:!?':
                char_delay *= random.uniform(1.2, 2.0)
            
            await page.keyboard.type(char)
            await asyncio.sleep(char_delay)
    
    async def interact_with_serp_human_like(self, page, target_site: str, session_data: Dict, 
                                          autowebglm, usimagent) -> bool:
        """Enhanced SERP interaction with human-like behavior"""
        
        logging.info("Analyzing SERP with enhanced human-like behavior")
        
        # Wait for results with human-like patience
        await page.wait_for_load_state('networkidle', timeout=20000)
        await asyncio.sleep(random.uniform(1.5, 4.0))
        
        # Analyze page with enhanced methods
        page_context = await autowebglm.analyze_page_context(page)
        
        # Perform human-like SERP exploration
        activities = await self._perform_serp_exploration(page, page_context, session_data, usimagent)
        
        # Find and interact with target
        target_domain = urlparse(target_site).netloc.replace('www.', '')
        target_result = await self._find_target_result_enhanced(page, target_domain)
        
        success = False
        if target_result:
            success = await self._click_target_result_human_like(page, target_result, session_data)
        else:
            # If target not found, click a random result (human-like behavior)
            await self._click_alternative_result(page, session_data)
        
        session_data["steps"].append({
            "action": "enhanced_serp_interaction",
            "target_found": target_result is not None,
            "page_analysis": page_context,
            "human_like_activities": activities,
            "click_success": success,
            "browser_type": "browserless" if self.use_browserless else "chromium",
            "timestamp": datetime.now().isoformat(),
            "success": success
        })
        
        return target_result is not None
    
    async def _perform_serp_exploration(self, page, page_context: Dict, session_data: Dict, usimagent) -> list:
        """Perform human-like SERP exploration"""
        
        activities = []
        exploration_duration = random.uniform(5, 15)
        start_time = time.time()
        
        while time.time() - start_time < exploration_duration:
            # Generate next exploration action
            context = {
                "current_goal": "explore search results",
                "page_type": "search_results",
                "page_context": page_context
            }
            
            action = await usimagent.generate_next_action(context)
            activity = await self._execute_serp_action(page, action)
            
            if activity:
                activities.append(activity)
                session_data["human_like_activities"].append({
                    "activity": activity,
                    "timestamp": datetime.now().isoformat(),
                    "action_details": action
                })
            
            # Check if should continue exploring
            if not usimagent.should_continue_browsing():
                break
        
        return activities
    
    async def _execute_serp_action(self, page, action: Dict) -> str:
        """Execute SERP action and return activity description"""
        
        action_type = action.get("action_type", "wait")
        parameters = action.get("parameters", {})
        
        try:
            if action_type == "hover_search_result":
                return await self._hover_search_results(page, parameters)
            
            elif action_type == "hover_link":
                return await self._hover_general_links(page, parameters)
            
            elif action_type == "scroll_down":
                return await self._human_like_scroll(page, parameters)
            
            elif action_type == "read_content":
                duration = parameters.get("duration", 5)
                await asyncio.sleep(duration)
                return f"read_content_{duration:.1f}s"
            
            elif action_type == "wait_and_observe":
                duration = parameters.get("duration", 3)
                await asyncio.sleep(duration)
                return f"observe_{duration:.1f}s"
            
            else:
                await asyncio.sleep(random.uniform(1, 3))
                return "general_pause"
                
        except Exception as e:
            logging.debug(f"SERP action execution failed: {action_type} - {e}")
            return f"failed_{action_type}"
    
    async def _hover_search_results(self, page, parameters: Dict) -> str:
        """Hover over search results in human-like manner"""
        
        try:
            # Find search result elements
            result_selectors = [
                ".g:visible",
                ".result:visible", 
                "[class*='result']:visible",
                "h3 a:visible",
                ".r a:visible"
            ]
            
            elements = []
            for selector in result_selectors:
                try:
                    found_elements = await page.locator(selector).all()
                    elements.extend(found_elements[:8])  # Limit to first 8
                except:
                    continue
            
            if elements:
                max_hovers = min(parameters.get("max_elements", 3), len(elements))
                hovered_count = 0
                
                for element in random.sample(elements, max_hovers):
                    try:
                        if await element.is_visible():
                            await element.hover()
                            duration = parameters.get("duration", 2)
                            await asyncio.sleep(duration)
                            hovered_count += 1
                            
                            # Small pause between hovers
                            await asyncio.sleep(random.uniform(0.5, 1.5))
                    except:
                        continue
                
                return f"hovered_{hovered_count}_search_results"
            
        except Exception as e:
            logging.debug(f"Search result hovering failed: {e}")
        
        return "hover_search_results_failed"
    
    async def _hover_general_links(self, page, parameters: Dict) -> str:
        """Hover over general links"""
        
        try:
            links = await page.locator("a:visible").all()
            
            if links:
                max_hovers = min(parameters.get("max_elements", 2), len(links))
                selected_links = random.sample(links[:15], max_hovers)  # From first 15 visible
                
                hovered_count = 0
                for link in selected_links:
                    try:
                        if await link.is_visible():
                            await link.hover()
                            duration = parameters.get("duration", 2)
                            await asyncio.sleep(duration)
                            hovered_count += 1
                            
                            await asyncio.sleep(random.uniform(0.3, 1.0))
                    except:
                        continue
                
                return f"hovered_{hovered_count}_general_links"
            
        except Exception as e:
            logging.debug(f"General link hovering failed: {e}")
        
        return "hover_general_links_failed"
    
    async def _human_like_scroll(self, page, parameters: Dict) -> str:
        """Human-like scrolling behavior"""
        
        try:
            amount = parameters.get("amount", 300)
            speed = parameters.get("speed", "normal")
            pause_probability = parameters.get("pause_probability", 0.5)
            
            if speed == "fast":
                # Quick scroll
                await page.mouse.wheel(0, amount)
                if random.random() < pause_probability:
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                return f"fast_scroll_{amount}px"
            
            elif speed == "slow":
                # Gradual scroll with pauses
                steps = 3
                for i in range(steps):
                    await page.mouse.wheel(0, amount // steps)
                    if random.random() < pause_probability:
                        await asyncio.sleep(random.uniform(1, 3))
                    else:
                        await asyncio.sleep(random.uniform(0.3, 0.8))
                return f"slow_scroll_{amount}px"
            
            else:
                # Normal scroll
                steps = 2
                for i in range(steps):
                    await page.mouse.wheel(0, amount // steps)
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                return f"normal_scroll_{amount}px"
                
        except Exception as e:
            logging.debug(f"Scrolling failed: {e}")
            return "scroll_failed"
    
    async def _find_target_result_enhanced(self, page, target_domain: str):
        """Enhanced target result finding"""
        
        # Multiple strategies for finding target
        strategies = [
            # Direct domain match in href
            lambda: page.locator(f"a[href*='{target_domain}']:visible").first,
            
            # Text content match
            lambda: page.locator(f".g:has-text('{target_domain}') a:visible").first,
            lambda: page.locator(f"h3:has-text('{target_domain.split('.')[0]}') a:visible").first,
            
            # URL display text match
            lambda: page.locator(f"span:has-text('{target_domain}') ~ a:visible").first,
            lambda: page.locator(f"cite:has-text('{target_domain}') ~ a:visible").first,
            
            # Broader search for domain parts
            lambda: page.locator(f"a[href*='{target_domain.split('.')[0]}']:visible").first
        ]
        
        for strategy in strategies:
            try:
                element = strategy()
                if await element.count() > 0:
                    href = await element.get_attribute("href")
                    if href and target_domain in href and not any(x in href for x in ['webcache', 'translate', 'youtube.com/redirect']):
                        return element
            except Exception as e:
                logging.debug(f"Strategy failed: {e}")
                continue
        
        return None
    
    async def _click_target_result_human_like(self, page, target_element, session_data: Dict) -> bool:
        """Click target result with enhanced human-like behavior"""
        
        try:
            # Enhanced pre-click behavior
            await self._pre_click_behavior(page, target_element)
            
            # Click the element
            await target_element.click()
            await page.wait_for_load_state('networkidle', timeout=20000)
            
            # Verify navigation
            success = await self._verify_navigation_enhanced(page)
            
            session_data["human_like_activities"].append({
                "activity": "clicked_target_result",
                "timestamp": datetime.now().isoformat(),
                "success": success
            })
            
            return success
            
        except Exception as e:
            logging.debug(f"Target click failed: {e}")
            return False
    
    async def _pre_click_behavior(self, page, element):
        """Enhanced pre-click behavior"""
        
        try:
            # Human-like approach and hover
            await self._human_like_element_approach(page, element)
            
            # Hover with random duration
            hover_duration = random.uniform(1.5, 4.0)
            await element.hover()
            await asyncio.sleep(hover_duration)
            
            # Sometimes move mouse slightly (human-like fidgeting)
            if random.random() < 0.3:
                box = await element.bounding_box()
                if box:
                    await page.mouse.move(
                        box['x'] + box['width'] / 2 + random.uniform(-5, 5),
                        box['y'] + box['height'] / 2 + random.uniform(-3, 3)
                    )
                    await asyncio.sleep(random.uniform(0.1, 0.3))
            
        except Exception as e:
            logging.debug(f"Pre-click behavior failed: {e}")
    
    async def _click_alternative_result(self, page, session_data: Dict):
        """Click alternative result if target not found (human-like behavior)"""
        
        try:
            # Find any clickable search result
            results = await page.locator(".g a:visible, .result a:visible").all()
            
            if results:
                # Click one of the first few results
                result = random.choice(results[:5])
                await self._pre_click_behavior(page, result)
                await result.click()
                
                session_data["human_like_activities"].append({
                    "activity": "clicked_alternative_result",
                    "timestamp": datetime.now().isoformat(),
                    "reason": "target_not_found"
                })
                
                await page.wait_for_load_state('networkidle', timeout=15000)
                
        except Exception as e:
            logging.debug(f"Alternative result click failed: {e}")
    
    async def _verify_navigation_enhanced(self, page) -> bool:
        """Enhanced navigation verification"""
        
        try:
            current_url = page.url
            
            # Check if we've left Google
            if "google.com" not in current_url.lower():
                return True
            
            # Check if we're on a Google redirect page
            if "url?q=" in current_url:
                # Wait a bit more for redirect
                await asyncio.sleep(2)
                current_url = page.url
                return "google.com" not in current_url.lower()
            
            return False
            
        except:
            return False
    
    def __del__(self):
        """Cleanup Browserless session on destruction"""
        if self.browserless_manager:
            try:
                self.browserless_manager.close_session()
            except:
                pass