#!/usr/bin/env python3
"""
COMPLETE GOOGLE SEARCH SIMULATOR - ALL FIXES INCLUDED
Handles Unicode issues, element visibility, and includes all required classes
"""

import asyncio
import random
import time
import json
import logging
import argparse
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urlparse
from playwright.async_api import async_playwright
import sys
import os

# ============================================================================
# FIX 1: UNICODE LOGGING CONFIGURATION
# ============================================================================

def setup_unicode_logging():
    """Configure logging to handle Unicode characters properly on Windows"""
    
    # Set console encoding to UTF-8 if possible
    if sys.platform.startswith('win'):
        try:
            # Try to set console to UTF-8
            os.system('chcp 65001 >nul')
        except:
            pass
    
    # Create custom formatter that handles Unicode
    class UnicodeFormatter(logging.Formatter):
        def format(self, record):
            # Replace problematic Unicode characters with ASCII equivalents
            msg = super().format(record)
            
            # Unicode replacements for emojis
            unicode_replacements = {
                '🔍': '[SEARCH]',
                '🎭': '[INTENT]',
                '🌐': '[WEB]',
                '⌨️': '[TYPE]',
                '👀': '[LOOK]',
                '🖱️': '[MOUSE]',
                '🎯': '[TARGET]',
                '✅': '[OK]',
                '❌': '[FAIL]',
                '⚠️': '[WARN]',
                '⏳': '[WAIT]',
                '📍': '[POS]',
                '📄': '[PAGE]',
                '💭': '[THINK]',
                '🔄': '[BACK]',
                '🚀': '[START]',
                '📊': '[STATS]',
                '🎉': '[DONE]',
                '⏱️': '[TIME]',
                '🧪': '[TEST]',
                '📂': '[FILE]',
                '💾': '[SAVE]',
                '🔀': '[SHUFFLE]'
            }
            
            for emoji, replacement in unicode_replacements.items():
                msg = msg.replace(emoji, replacement)
            
            return msg
    
    # Configure logging with Unicode handling
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('google_search_simulator.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )
    
    # Apply Unicode formatter to all handlers
    for handler in logging.getLogger().handlers:
        handler.setFormatter(UnicodeFormatter('%(asctime)s - %(levelname)s - %(message)s'))

# Initialize Unicode logging at module level
setup_unicode_logging()
logger = logging.getLogger(__name__)

# ============================================================================
# HUMAN BEHAVIOR PATTERNS
# ============================================================================

class HumanSearchBehavior:
    """
    Realistic human search behavior patterns based on UX research
    """
    
    # User intent types and their typical behaviors
    USER_INTENT_PATTERNS = {
        "informational": {
            "time_on_site": (90, 180),  # 1.5-3 minutes
            "scroll_pattern": "thorough",
            "click_probability": 0.7,
            "pogo_stick_chance": 0.4,
            "pages_visited": (2, 4)
        },
        "commercial": {
            "time_on_site": (120, 300),  # 2-5 minutes
            "scroll_pattern": "focused",
            "click_probability": 0.8,
            "pogo_stick_chance": 0.3,
            "pages_visited": (3, 6)
        },
        "transactional": {
            "time_on_site": (180, 360),  # 3-6 minutes
            "scroll_pattern": "detailed",
            "click_probability": 0.9,
            "pogo_stick_chance": 0.2,
            "pages_visited": (4, 8)
        },
        "navigational": {
            "time_on_site": (60, 120),  # 1-2 minutes
            "scroll_pattern": "quick",
            "click_probability": 0.95,
            "pogo_stick_chance": 0.1,
            "pages_visited": (1, 3)
        }
    }
    
    # Reading simulation patterns
    READING_PATTERNS = {
        "skimmer": {"words_per_second": 8, "pause_frequency": 0.3},
        "normal": {"words_per_second": 4, "pause_frequency": 0.5},
        "careful": {"words_per_second": 2, "pause_frequency": 0.7}
    }

# ============================================================================
# FIXED GOOGLE SEARCH SIMULATOR
# ============================================================================

class GoogleSearchSimulator:
    """
    Fixed Google Search Simulator with proper element handling
    """
    
    def __init__(self):
        self.session_data = []
        self.current_session = None
        
    async def create_realistic_browser(self):
        """Create browser with human-like configuration"""
        
        # Import stealth if available
        try:
            from playwright_stealth import stealth_async
            stealth_available = True
        except ImportError:
            stealth_available = False
            logger.warning("[WARN] playwright-stealth not available. Install: pip install playwright-stealth")
        
        playwright = await async_playwright().start()
        
        # Realistic browser configurations
        browser_configs = [
            {
                "viewport": {"width": 1366, "height": 768},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "device_scale_factor": 1
            },
            {
                "viewport": {"width": 1920, "height": 1080},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "device_scale_factor": 1
            },
            {
                "viewport": {"width": 1440, "height": 900},
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "device_scale_factor": 2
            }
        ]
        
        config = random.choice(browser_configs)
        
        browser = await playwright.chromium.launch(
            headless=False,  # Set to True for production
            slow_mo=random.randint(50, 150),
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-automation',
                '--no-sandbox',
                '--disable-extensions',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--allow-running-insecure-content'
            ]
        )
        
        context = await browser.new_context(
            viewport=config["viewport"],
            user_agent=config["user_agent"],
            device_scale_factor=config["device_scale_factor"],
            locale="en-US",
            timezone_id=random.choice(["America/New_York", "America/Los_Angeles", "America/Chicago"]),
            geolocation={"latitude": 40.7128, "longitude": -74.0060},
            permissions=["geolocation"],
            color_scheme="light"
        )
        
        page = await context.new_page()
        
        # Apply stealth if available
        if stealth_available:
            await stealth_async(page)
        
        # Add human-like scripts
        await self._inject_human_behavior_scripts(page)
        
        return page, browser, playwright
    
    async def _inject_human_behavior_scripts(self, page):
        """Inject scripts that simulate human browser behavior"""
        
        await page.add_init_script("""
            // Remove automation indicators
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Add realistic chrome object
            window.chrome = {
                runtime: {},
                loadTimes: function() {
                    return {
                        commitLoadTime: Date.now() / 1000 - Math.random() * 100,
                        finishDocumentLoadTime: Date.now() / 1000 - Math.random() * 50,
                        finishLoadTime: Date.now() / 1000 - Math.random() * 25,
                        navigationType: "Other",
                        requestTime: Date.now() / 1000 - Math.random() * 150
                    };
                }
            };
            
            // Add mouse tracking for realistic movement
            window.mouseTracker = {
                lastX: 0,
                lastY: 0,
                movements: [],
                track: function(x, y) {
                    this.movements.push({x, y, time: Date.now()});
                    if (this.movements.length > 100) {
                        this.movements.shift();
                    }
                    this.lastX = x;
                    this.lastY = y;
                }
            };
            
            document.addEventListener('mousemove', (e) => {
                window.mouseTracker.track(e.clientX, e.clientY);
            });
        """)
    
    async def simulate_search_session(self, keyword: str, target_site: str) -> Dict[str, Any]:
        """
        Simulate a complete search session for a keyword and target site
        """
        
        logger.info(f"[SEARCH] Starting search session: '{keyword}' -> {target_site}")
        
        session_start = time.time()
        
        # Determine user intent from keyword
        user_intent = self._analyze_user_intent(keyword)
        behavior_config = HumanSearchBehavior.USER_INTENT_PATTERNS[user_intent]
        
        logger.info(f"[INTENT] User intent: {user_intent}")
        
        # Create browser
        page, browser, playwright = await self.create_realistic_browser()
        
        session_data = {
            "keyword": keyword,
            "target_site": target_site,
            "user_intent": user_intent,
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "success": False
        }
        
        try:
            # Step 1: Navigate to Google
            await self._navigate_to_google(page, session_data)
            
            # Step 2: Perform search
            await self._perform_search(page, keyword, session_data)
            
            # Step 3: Analyze SERP and interact
            await self._interact_with_serp(page, target_site, behavior_config, session_data)
            
            # Step 4: Visit target site
            success = await self._visit_target_site(page, target_site, behavior_config, session_data)
            
            session_data["success"] = success
            session_data["duration"] = time.time() - session_start
            
            logger.info(f"[OK] Search session completed: {success}")
            
        except Exception as e:
            logger.error(f"[FAIL] Search session failed: {e}")
            session_data["error"] = str(e)
            session_data["duration"] = time.time() - session_start
            
        finally:
            try:
                await browser.close()
                await playwright.stop()
            except:
                pass
        
        self.session_data.append(session_data)
        return session_data
    
    def _analyze_user_intent(self, keyword: str) -> str:
        """Analyze keyword to determine user intent"""
        
        keyword_lower = keyword.lower()
        
        # Transactional intent keywords
        if any(word in keyword_lower for word in [
            "buy", "purchase", "order", "booking", "book", "appointment", 
            "software", "app", "tool", "service", "hire", "get", "find"
        ]):
            return "transactional"
        
        # Commercial intent keywords  
        elif any(word in keyword_lower for word in [
            "best", "top", "review", "compare", "vs", "price", "cost",
            "cheap", "discount", "deal", "shop", "store"
        ]):
            return "commercial"
        
        # Navigational intent keywords
        elif any(word in keyword_lower for word in [
            "login", "sign in", "website", "official", "homepage"
        ]):
            return "navigational"
        
        # Default to informational
        else:
            return "informational"
    
    async def _navigate_to_google(self, page, session_data: Dict):
        """Navigate to Google with human-like behavior"""
        
        logger.info("[WEB] Navigating to Google")
        
        # Sometimes visit google.com directly, sometimes search from address bar
        if random.random() < 0.8:  # 80% direct navigation
            await page.goto("https://www.google.com", wait_until='networkidle', timeout=20000)
        else:
            await page.goto("https://www.google.com/search", wait_until='networkidle', timeout=20000)
        
        # Human reaction time
        await asyncio.sleep(random.uniform(1, 3))
        
        session_data["steps"].append({
            "action": "navigate_to_google",
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
    
    async def _perform_search(self, page, keyword: str, session_data: Dict):
        """Perform search with realistic typing behavior"""
        
        logger.info(f"[TYPE] Typing search query: '{keyword}'")
        
        # Find search box with multiple selectors
        search_selectors = [
            "input[name='q']",
            "textarea[name='q']", 
            "input[title='Search']",
            ".gLFyf",
            "#APjFqb"
        ]
        
        search_box = None
        for selector in search_selectors:
            try:
                element = page.locator(selector).first
                if await element.count() > 0 and await element.is_visible():
                    search_box = element
                    break
            except:
                continue
        
        if not search_box:
            raise Exception("Could not find search box")
        
        # Click search box with natural mouse movement
        await self._human_like_click(page, search_box)
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Clear any existing content
        await search_box.clear()
        await asyncio.sleep(random.uniform(0.2, 0.5))
        
        # Type with human-like patterns
        await self._human_like_typing(page, keyword)
        
        # Random pause before submitting (human thinking time)
        await asyncio.sleep(random.uniform(1, 3))
        
        # Submit search
        await page.keyboard.press("Enter")
        
        # Wait for results
        await page.wait_for_load_state('networkidle', timeout=15000)
        await asyncio.sleep(random.uniform(1, 2))
        
        session_data["steps"].append({
            "action": "perform_search",
            "keyword": keyword,
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
        
    # ============================================================================
    # FIXED SERP INTERACTION METHODS
    # ============================================================================
    
    async def _find_target_result(self, page, target_domain: str):
        """Find visible and clickable target result - FIXED VERSION"""
        
        logger.info(f"[SEARCH] Looking for target domain: {target_domain}")
        
        # Wait for search results to fully load
        try:
            await page.wait_for_selector(".g", timeout=10000)
            await asyncio.sleep(2)  # Extra wait for dynamic content
        except:
            logger.warning("[WARN] Standard result selector not found")
        
        # Strategy 1: Find visible clickable links first
        visible_selectors = [
            f"a[href*='{target_domain}']:visible",
            f".g:visible a[href*='{target_domain}']",
            f".yuRUbf:visible a[href*='{target_domain}']"
        ]
        
        for selector in visible_selectors:
            try:
                logger.debug(f"[SEARCH] Trying visible selector: {selector}")
                elements = await page.locator(selector).all()
                
                for element in elements:
                    try:
                        # Check if element is actually visible and interactable
                        if await element.is_visible() and await element.is_enabled():
                            href = await element.get_attribute("href")
                            if href and target_domain in href and not any(x in href for x in ['webcache', 'translate']):
                                # Scroll element into view
                                await element.scroll_into_view_if_needed()
                                await asyncio.sleep(0.5)
                                
                                # Double-check it's still visible after scrolling
                                if await element.is_visible():
                                    logger.info(f"[OK] Found visible target result: {href}")
                                    return element
                    except Exception as e:
                        logger.debug(f"[WARN] Element check failed: {e}")
                        continue
            except Exception as e:
                logger.debug(f"[WARN] Selector failed: {selector} - {e}")
                continue
        
        # Strategy 2: Find by text content in visible containers
        try:
            logger.info("[SEARCH] Trying text-based search...")
            
            # Get all visible result containers
            containers = await page.locator(".g:visible, .yuRUbf:visible, div[data-ved]:visible").all()
            
            for container in containers:
                try:
                    text_content = await container.inner_text()
                    if target_domain.lower() in text_content.lower():
                        # Find the main link within this container
                        links = await container.locator("a[href*='http']").all()
                        
                        for link in links:
                            if await link.is_visible() and await link.is_enabled():
                                href = await link.get_attribute("href")
                                if href and target_domain in href:
                                    await link.scroll_into_view_if_needed()
                                    await asyncio.sleep(0.5)
                                    
                                    if await link.is_visible():
                                        logger.info(f"[OK] Found target via text search: {href}")
                                        return link
                except Exception as e:
                    logger.debug(f"[WARN] Container search failed: {e}")
                    continue
        
        except Exception as e:
            logger.debug(f"[WARN] Text-based search failed: {e}")
        
        # Strategy 3: Debug what's actually available
        await self._debug_available_results(page)
        
        logger.warning(f"[FAIL] Target domain {target_domain} not found in visible results")
        return None
    
    async def _interact_with_serp(self, page, target_site: str, behavior_config: Dict, session_data: Dict):
        """Interact with Search Engine Results Page - COMPLETELY FIXED VERSION"""
        
        logger.info("[LOOK] Analyzing SERP results")
        
        # Extract domain from target site URL
        target_domain = urlparse(target_site).netloc.replace('www.', '')
        
        # Wait for results to load completely
        await page.wait_for_load_state('networkidle', timeout=15000)
        await asyncio.sleep(random.uniform(2, 4))
        
        # Scroll past top results first (realistic behavior)
        await self._scroll_past_top_results(page)
        
        # Find all result links for hovering (with error handling)
        try:
            result_links = await page.locator(".g h3:visible, .yuRUbf h3:visible").all()
        except:
            result_links = []
        
        # Hover on 2-3 other results before target (with error handling)
        try:
            await self._hover_on_other_results(page, result_links, target_domain)
        except Exception as e:
            logger.warning(f"[WARN] Hover on other results failed: {e}")
        
        # Find target site result
        target_result = await self._find_target_result(page, target_domain)
        
        if target_result:
            # Hover on target site (optional, continue if fails)
            hover_success = await self._hover_on_target_result(page, target_result)
            
            # Random delay before clicking (1.5-6 seconds)
            delay = random.uniform(1.5, 6.0)
            logger.info(f"[WAIT] Waiting {delay:.1f}s before clicking target")
            await asyncio.sleep(delay)
            
            # Click target result with improved error handling
            success = await self._click_target_result(page, target_result, target_site)
            
            session_data["steps"].append({
                "action": "click_target_result",
                "target_domain": target_domain,
                "hover_success": hover_success,
                "click_success": success,
                "timestamp": datetime.now().isoformat(),
                "success": success
            })
            
        else:
            logger.warning(f"[WARN] Target site {target_domain} not found in results")
            
            session_data["steps"].append({
                "action": "target_not_found",
                "target_domain": target_domain,
                "timestamp": datetime.now().isoformat(),
                "success": False
            })
    
    async def _hover_on_target_result(self, page, target_result):
        """Hover on target result with better error handling"""
        
        logger.info("[TARGET] Hovering on target result")
        
        try:
            # Ensure element is in view and stable
            await target_result.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            
            # Check if still visible after scroll
            if not await target_result.is_visible():
                logger.warning("[WARN] Target result became invisible after scroll")
                return False
            
            # Hover with timeout
            await target_result.hover(timeout=5000)
            await asyncio.sleep(random.uniform(1, 2))
            
            # Add slight mouse jitter
            await self._add_mouse_jitter(page)
            return True
            
        except Exception as e:
            logger.warning(f"[WARN] Hover failed, will proceed to click: {e}")
            return False
    
    async def _click_target_result(self, page, target_result, target_site: str) -> bool:
        """Click target result with comprehensive fallback methods"""
        
        try:
            # Get the href before clicking to verify
            href = await target_result.get_attribute("href")
            logger.info(f"[TARGET] Attempting to click: {href}")
            
            # Ensure element is ready
            await target_result.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            
            if not await target_result.is_visible():
                logger.warning("[WARN] Element not visible, trying alternative methods")
                return await self._alternative_navigation_methods(page, href, target_site)
            
            # Method 1: Regular click with navigation wait
            try:
                logger.info("[TARGET] Trying regular click...")
                
                # Click and wait for navigation
                async with page.expect_navigation(timeout=15000, wait_until="networkidle"):
                    await target_result.click()
                
                logger.info("[OK] Navigation completed via regular click")
                return True
                
            except Exception as e:
                logger.info(f"[WARN] Regular click failed: {e}")
                
                # Method 2: Force click with JavaScript
                try:
                    logger.info("[TARGET] Trying JavaScript click...")
                    
                    await target_result.evaluate("element => element.click()")
                    await page.wait_for_load_state('networkidle', timeout=15000)
                    
                    # Verify navigation happened
                    current_url = page.url
                    target_domain = urlparse(target_site).netloc.replace('www.', '')
                    
                    if target_domain in current_url:
                        logger.info("[OK] Navigation completed via JS click")
                        return True
                    else:
                        logger.info(f"[WARN] JS click didn't navigate to target. Current: {current_url}")
                        
                except Exception as e2:
                    logger.info(f"[WARN] JS click failed: {e2}")
                
                # Method 3: Direct navigation to href
                return await self._alternative_navigation_methods(page, href, target_site)
    
        except Exception as e:
            logger.error(f"[FAIL] All click methods failed: {e}")
            return False
    
    async def _alternative_navigation_methods(self, page, href: str, target_site: str) -> bool:
        """Alternative methods when clicking fails"""
        
        if not href or 'http' not in href:
            logger.error("[FAIL] No valid href found for direct navigation")
            return False
        
        try:
            logger.info("[TARGET] Trying direct navigation...")
            
            # Clean up the URL (remove Google tracking parameters)
            clean_url = self._clean_google_url(href)
            
            await page.goto(clean_url, wait_until='networkidle', timeout=20000)
            
            # Verify we reached the target
            current_url = page.url
            target_domain = urlparse(target_site).netloc.replace('www.', '')
            
            if target_domain in current_url:
                logger.info("[OK] Navigation completed via direct goto")
                return True
            else:
                logger.warning(f"[WARN] Direct navigation didn't reach target. Current: {current_url}")
                return False
                
        except Exception as e:
            logger.error(f"[FAIL] Direct navigation failed: {e}")
            return False
    
    def _clean_google_url(self, google_url: str) -> str:
        """Extract clean URL from Google's wrapped URL"""
        
        try:
            # If it's already a clean URL, return as-is
            if not google_url.startswith('https://www.google.com/url'):
                return google_url
            
            # Extract the actual URL from Google's wrapper
            import urllib.parse as urlparse_module
            parsed = urlparse_module.urlparse(google_url)
            query_params = urlparse_module.parse_qs(parsed.query)
            
            if 'url' in query_params:
                return query_params['url'][0]
            elif 'q' in query_params:
                return query_params['q'][0]
            else:
                return google_url
                
        except Exception:
            return google_url
    
    # ============================================================================
    # HELPER METHODS
    # ============================================================================
    
    async def _scroll_past_top_results(self, page):
        """Scroll past top results (realistic user behavior)"""
        
        # Scroll down to see more results
        scroll_distance = random.randint(300, 600)
        await page.mouse.wheel(0, scroll_distance)
        await asyncio.sleep(random.uniform(1, 2))
        
        # Sometimes scroll back up slightly
        if random.random() < 0.3:
            await page.mouse.wheel(0, -random.randint(100, 200))
            await asyncio.sleep(random.uniform(0.5, 1))
    
    async def _hover_on_other_results(self, page, result_links: List, target_domain: str):
        """Hover on 2-3 other results before clicking target - WITH ERROR HANDLING"""
        
        if not result_links:
            logger.info("[MOUSE] No result links found for hovering")
            return
        
        hover_count = min(random.randint(2, 3), len(result_links))
        logger.info(f"[MOUSE] Hovering on {hover_count} other results first")
        
        hovered = 0
        for i, result in enumerate(result_links):
            if hovered >= hover_count:
                break
                
            try:
                # Skip if this might be our target domain
                result_text = await result.inner_text()
                if target_domain.lower() in result_text.lower():
                    continue
                
                # Check if element is visible and interactable
                if await result.is_visible() and await result.is_enabled():
                    # Hover with timeout
                    await result.hover(timeout=3000)
                    await asyncio.sleep(random.uniform(1, 2.5))
                    hovered += 1
                    
                    # Sometimes move mouse slightly (jitter)
                    if random.random() < 0.4:
                        await self._add_mouse_jitter(page)
                
            except Exception as e:
                logger.debug(f"[WARN] Hover failed on result {i}: {e}")
                continue
        
        logger.info(f"[MOUSE] Successfully hovered on {hovered} results")
    
    async def _debug_available_results(self, page):
        """Debug function to see what results are actually available"""
        
        logger.info("[SEARCH] DEBUG: Available search results:")
        
        try:
            # Get all links in search results
            links = await page.locator("a[href*='http']").all()
            
            visible_count = 0
            for i, link in enumerate(links[:15]):  # Show first 15
                try:
                    href = await link.get_attribute("href")
                    is_visible = await link.is_visible()
                    
                    if is_visible:
                        visible_count += 1
                        text = await link.inner_text()
                        text = text.strip()[:80]  # First 80 chars
                        logger.info(f"  {visible_count}. [VISIBLE] {href} | {text}")
                    elif href and not any(x in href for x in ['google.com', 'webcache']):
                        text = await link.inner_text()
                        text = text.strip()[:80]
                        logger.info(f"  {i+1}. [HIDDEN] {href} | {text}")
                        
                except Exception as e:
                    logger.debug(f"[WARN] Debug link {i} failed: {e}")
                    continue
            
            logger.info(f"[SEARCH] Found {visible_count} visible links out of {len(links)} total")
                
        except Exception as e:
            logger.debug(f"[WARN] Debug failed: {e}")
    
    async def _add_mouse_jitter(self, page):
        """Add realistic mouse jitter/movement with error handling"""
        
        try:
            # Get current viewport
            viewport = page.viewport_size
            
            # Small random movements
            for _ in range(random.randint(1, 2)):
                # Small jitter movements (1-5 pixels)
                dx = random.randint(-5, 5)
                dy = random.randint(-5, 5)
                
                current_pos = await page.evaluate("""
                    () => ({
                        x: window.mouseTracker ? window.mouseTracker.lastX : window.innerWidth/2,
                        y: window.mouseTracker ? window.mouseTracker.lastY : window.innerHeight/2
                    })
                """)
                
                new_x = max(0, min(viewport["width"], current_pos["x"] + dx))
                new_y = max(0, min(viewport["height"], current_pos["y"] + dy))
                
                await page.mouse.move(new_x, new_y)
                await asyncio.sleep(random.uniform(0.05, 0.15))
                
        except Exception as e:
            logger.debug(f"[WARN] Mouse jitter failed: {e}")
    
    async def _human_like_typing(self, page, text: str):
        """Type text with human-like patterns"""
        
        typing_speed_base = random.uniform(80, 120)  # WPM
        char_delay_base = 60 / (typing_speed_base * 5)  # Convert to seconds per character
        
        for i, char in enumerate(text):
            # Add randomness to typing speed
            char_delay = char_delay_base * random.uniform(0.5, 1.5)
            
            # Slower for complex characters
            if char in ' .,!?':
                char_delay *= random.uniform(1.2, 2.0)
            
            # Occasional longer pauses (thinking)
            if random.random() < 0.1:  # 10% chance
                char_delay *= random.uniform(2, 4)
            
            await page.keyboard.type(char)
            await asyncio.sleep(char_delay)
    
    async def _human_like_click(self, page, element):
        """Perform human-like click with natural mouse movement"""
        
        # Get element position
        try:
            box = await element.bounding_box()
            if not box:
                await element.click()
                return
            
            # Add randomness to click position within element
            x = box["x"] + box["width"] * random.uniform(0.3, 0.7)
            y = box["y"] + box["height"] * random.uniform(0.3, 0.7)
            
            # Move mouse to position with slight curve
            await page.mouse.move(x, y)
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Click
            await page.mouse.click(x, y)
        except:
            # Fallback to simple click
            await element.click()
    
    async def _visit_target_site(self, page, target_site: str, behavior_config: Dict, session_data: Dict) -> bool:
        """Visit target site and perform realistic browsing"""
        
        logger.info(f"[WEB] Visiting target site: {target_site}")
        
        try:
            # Wait for page to load completely
            await page.wait_for_load_state('networkidle', timeout=20000)
            await asyncio.sleep(random.uniform(1, 3))
            
            # Get current URL
            current_url = page.url
            logger.info(f"[POS] Current URL: {current_url}")
            
            # Verify we're on the correct site
            target_domain = urlparse(target_site).netloc.replace('www.', '')
            current_domain = urlparse(current_url).netloc.replace('www.', '')
            
            # More flexible domain matching
            is_correct_site = (
                target_domain in current_domain or 
                current_domain in target_domain or
                target_domain.replace('.com', '') in current_domain
            )
            
            if not is_correct_site:
                logger.warning(f"[WARN] Domain mismatch:")
                logger.warning(f"  Expected: {target_domain}")
                logger.warning(f"  Current:  {current_domain}")
                logger.warning(f"  Full URL: {current_url}")
                
                # Check if we're on a redirect or similar domain
                if any(x in current_url.lower() for x in ['google.com', 'search', 'webcache']):
                    logger.error("[FAIL] Still on Google or cache page")
                    return False
                else:
                    logger.info("[WARN] Continuing despite domain difference (might be redirect)")
            
            logger.info(f"[OK] Successfully reached: {current_url}")
            
            # Check if page loaded properly (not error page)
            try:
                page_title = await page.title()
                logger.info(f"[PAGE] Page title: {page_title}")
                
                # Check for error indicators
                if any(x in page_title.lower() for x in ['error', '404', '403', '500', 'not found']):
                    logger.warning(f"[WARN] Possible error page: {page_title}")
            except:
                pass
            
            # Determine time on site
            time_range = behavior_config["time_on_site"]
            time_on_site = random.randint(*time_range)
            logger.info(f"[TIME] Planning to stay {time_on_site} seconds")
            
            # Perform realistic browsing activities
            await self._perform_site_activities(page, time_on_site, behavior_config, session_data)
            
            session_data["steps"].append({
                "action": "site_visit_complete",
                "final_url": current_url,
                "target_domain": target_domain,
                "current_domain": current_domain,
                "domain_match": is_correct_site,
                "time_on_site": time_on_site,
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            return True
            
        except Exception as e:
            logger.error(f"[FAIL] Site visit failed: {e}")
            session_data["steps"].append({
                "action": "site_visit_failed",
                "error": str(e),
                "current_url": page.url if page else "unknown",
                "timestamp": datetime.now().isoformat(),
                "success": False
            })
            return False
    
    async def _perform_site_activities(self, page, total_time: int, behavior_config: Dict, session_data: Dict):
        """Perform realistic human-like activities on the target site"""
        
        start_time = time.time()
        end_time = start_time + total_time
        
        activities = []
        
        logger.info(f"[SITE] Starting {total_time}s of realistic browsing activities")
        
        # Initial page scan and exploration
        await self._simulate_reading(page, duration=random.uniform(3, 8))
        activities.append("initial_reading")
        
        # Get page info for better activity selection
        page_info = await self._analyze_page_content(page)
        
        activity_weights = {
            "scroll_and_read": 25,
            "click_internal_links": 20,
            "hover_and_explore": 15,
            "form_interaction": 10,
            "menu_navigation": 12,
            "search_on_site": 8,
            "inactive_pause": 7,
            "mouse_exploration": 3
        }
        
        # Adjust weights based on page content
        if page_info.get("has_forms"):
            activity_weights["form_interaction"] *= 2
        if page_info.get("has_search"):
            activity_weights["search_on_site"] *= 2
        if page_info.get("has_navigation"):
            activity_weights["menu_navigation"] *= 1.5
        
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            
            if remaining_time < 10:  # Less than 10 seconds left
                break
            
            # Choose weighted random activity
            activity = self._weighted_choice(activity_weights)
            
            try:
                logger.info(f"[ACTIVITY] Performing: {activity}")
                
                if activity == "scroll_and_read":
                    await self._scroll_and_read_activity(page)
                    activities.append("scroll_read")
                
                elif activity == "click_internal_links":
                    clicked = await self._click_internal_links_activity(page)
                    if clicked:
                        activities.append("clicked_link")
                        # Spend time on new page
                        await asyncio.sleep(random.uniform(10, 25))
                        # Maybe go back
                        if random.random() < 0.6:
                            await page.go_back()
                            await page.wait_for_load_state('networkidle', timeout=10000)
                            await asyncio.sleep(random.uniform(2, 5))
                            activities.append("went_back")
                
                elif activity == "hover_and_explore":
                    await self._hover_and_explore_activity(page)
                    activities.append("hover_explore")
                
                elif activity == "form_interaction":
                    if page_info.get("has_forms"):
                        filled = await self._form_interaction_activity(page)
                        if filled:
                            activities.append("form_interaction")
                
                elif activity == "menu_navigation":
                    if page_info.get("has_navigation"):
                        navigated = await self._menu_navigation_activity(page)
                        if navigated:
                            activities.append("menu_navigation")
                
                elif activity == "search_on_site":
                    if page_info.get("has_search"):
                        searched = await self._search_on_site_activity(page)
                        if searched:
                            activities.append("site_search")
                
                elif activity == "inactive_pause":
                    await self._inactive_pause_activity()
                    activities.append("thinking_pause")
                
                elif activity == "mouse_exploration":
                    await self._mouse_exploration_activity(page)
                    activities.append("mouse_exploration")
                
            except Exception as e:
                logger.debug(f"[WARN] Activity {activity} failed: {e}")
                # Fallback to basic scrolling
                await self._scroll_and_read_activity(page)
                activities.append("fallback_scroll")
        
        logger.info(f"[SITE] Completed {len(activities)} activities: {', '.join(activities)}")
        
        session_data["steps"].append({
            "action": "site_activities",
            "activities": activities,
            "activity_count": len(activities),
            "activity_duration": total_time,
            "timestamp": datetime.now().isoformat()
        })
    
    def _weighted_choice(self, weights_dict):
        """Choose activity based on weights"""
        items = list(weights_dict.keys())
        weights = list(weights_dict.values())
        return random.choices(items, weights=weights)[0]
    
    async def _analyze_page_content(self, page):
        """Analyze page to determine available interactive elements"""
        
        try:
            page_info = {
                "has_forms": False,
                "has_search": False,
                "has_navigation": False,
                "has_buttons": False,
                "has_links": False
            }
            
            # Check for forms
            forms = await page.locator("form, input[type='text'], input[type='email'], textarea").count()
            page_info["has_forms"] = forms > 0
            
            # Check for search
            search_elements = await page.locator("input[type='search'], input[placeholder*='search' i], .search-input, #search").count()
            page_info["has_search"] = search_elements > 0
            
            # Check for navigation
            nav_elements = await page.locator("nav, .navigation, .navbar, .menu, .nav-menu").count()
            page_info["has_navigation"] = nav_elements > 0
            
            # Check for interactive buttons
            buttons = await page.locator("button, .btn, input[type='submit'], input[type='button']").count()
            page_info["has_buttons"] = buttons > 0
            
            # Check for internal links
            links = await page.locator("a[href]:not([href*='mailto:']):not([href*='tel:'])").count()
            page_info["has_links"] = links > 3  # More than just basic links
            
            logger.debug(f"[ANALYSIS] Page info: {page_info}")
            return page_info
            
        except Exception as e:
            logger.debug(f"[WARN] Page analysis failed: {e}")
            return {"has_forms": False, "has_search": False, "has_navigation": False, "has_buttons": False, "has_links": False}
    
    async def _click_internal_links_activity(self, page):
        """Click on internal links and explore sub-pages"""
        
        try:
            # Find internal links (avoid external sites)
            current_domain = urlparse(page.url).netloc
            
            # Look for internal links
            internal_link_selectors = [
                f"a[href^='/']",  # Relative URLs
                f"a[href*='{current_domain}']",  # Same domain
                "a[href^='#']",  # Anchors
                ".nav-item a", ".menu-item a", ".navigation a"  # Navigation links
            ]
            
            potential_links = []
            
            for selector in internal_link_selectors:
                try:
                    links = await page.locator(selector).all()
                    for link in links:
                        if await link.is_visible() and await link.is_enabled():
                            href = await link.get_attribute("href")
                            text = await link.inner_text()
                            
                            # Filter out unwanted links
                            if href and text and not any(x in href.lower() for x in [
                                'mailto:', 'tel:', 'javascript:', '.pdf', '.doc', 
                                'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com',
                                'logout', 'login', 'signup', 'register'
                            ]) and len(text.strip()) > 0:
                                potential_links.append(link)
                except:
                    continue
            
            if potential_links:
                # Choose a random link
                target_link = random.choice(potential_links)
                
                # Hover first
                await target_link.hover()
                await asyncio.sleep(random.uniform(1, 2))
                
                # Get link info for logging
                href = await target_link.get_attribute("href")
                text = await target_link.inner_text()
                logger.info(f"[CLICK] Clicking internal link: {text[:50]} -> {href}")
                
                # Click the link
                await target_link.click()
                await page.wait_for_load_state('networkidle', timeout=10000)
                
                return True
            
        except Exception as e:
            logger.debug(f"[WARN] Internal link clicking failed: {e}")
        
        return False
    
    async def _hover_and_explore_activity(self, page):
        """Hover over various elements to explore the page"""
        
        try:
            # Elements that are interesting to hover over
            hover_selectors = [
                "button", ".btn", "[role='button']",
                ".nav-item", ".menu-item", 
                ".card", ".product", ".item",
                ".cta", ".call-to-action",
                "img", ".image",
                ".dropdown", ".dropdown-toggle",
                "h1, h2, h3", ".title", ".heading"
            ]
            
            hover_count = random.randint(3, 7)
            hovered = 0
            
            for selector in hover_selectors:
                if hovered >= hover_count:
                    break
                    
                try:
                    elements = await page.locator(selector + ":visible").all()
                    if elements:
                        element = random.choice(elements)
                        await element.hover()
                        
                        # Simulate reading/thinking
                        await asyncio.sleep(random.uniform(1, 3))
                        
                        # Add mouse jitter
                        await self._add_mouse_jitter(page)
                        
                        hovered += 1
                        
                        # Small chance to click non-destructive elements
                        if random.random() < 0.2 and selector in ["img", ".image", "h1, h2, h3"]:
                            try:
                                await element.click()
                                await asyncio.sleep(random.uniform(1, 2))
                            except:
                                pass
                        
                except:
                    continue
            
            logger.debug(f"[HOVER] Hovered over {hovered} elements")
            
        except Exception as e:
            logger.debug(f"[WARN] Hover exploration failed: {e}")
    
    async def _form_interaction_activity(self, page):
        """Interact with forms (fill sample data, but don't submit)"""
        
        try:
            # Find visible form elements
            form_elements = [
                "input[type='text']:visible",
                "input[type='email']:visible", 
                "textarea:visible",
                "input[type='search']:visible"
            ]
            
            filled_fields = 0
            
            for selector in form_elements:
                try:
                    inputs = await page.locator(selector).all()
                    
                    for input_field in inputs[:2]:  # Limit to 2 fields
                        if await input_field.is_visible() and await input_field.is_enabled():
                            
                            # Click on the field
                            await input_field.click()
                            await asyncio.sleep(random.uniform(0.5, 1))
                            
                            # Determine what type of data to enter
                            placeholder = await input_field.get_attribute("placeholder") or ""
                            name = await input_field.get_attribute("name") or ""
                            input_type = await input_field.get_attribute("type") or "text"
                            
                            sample_data = self._get_sample_form_data(input_type, placeholder, name)
                            
                            if sample_data:
                                # Clear field first
                                await input_field.clear()
                                await asyncio.sleep(random.uniform(0.2, 0.5))
                                
                                # Type with human-like behavior
                                await self._human_like_typing(page, sample_data)
                                
                                filled_fields += 1
                                logger.info(f"[FORM] Filled field with sample data")
                                
                                # Move to next field or click elsewhere
                                await asyncio.sleep(random.uniform(1, 2))
                
                except Exception as e:
                    logger.debug(f"[WARN] Form field interaction failed: {e}")
                    continue
            
            # Click somewhere else to unfocus
            if filled_fields > 0:
                try:
                    await page.click("body")
                except:
                    pass
            
            return filled_fields > 0
            
        except Exception as e:
            logger.debug(f"[WARN] Form interaction failed: {e}")
            return False
    
    def _get_sample_form_data(self, input_type, placeholder, name):
        """Generate appropriate sample data for form fields"""
        
        placeholder_lower = placeholder.lower()
        name_lower = name.lower()
        
        # Email fields
        if input_type == "email" or any(x in placeholder_lower + name_lower for x in ["email", "mail"]):
            return random.choice(["test@example.com", "user@demo.com", "sample@test.org"])
        
        # Search fields  
        elif input_type == "search" or any(x in placeholder_lower + name_lower for x in ["search", "find", "query"]):
            return random.choice(["product", "services", "information", "help", "contact"])
        
        # Name fields
        elif any(x in placeholder_lower + name_lower for x in ["name", "first", "last"]):
            return random.choice(["John", "Jane", "Test User", "Demo"])
        
        # Phone fields
        elif any(x in placeholder_lower + name_lower for x in ["phone", "tel", "mobile"]):
            return random.choice(["555-0123", "123-456-7890", "(555) 123-4567"])
        
        # Company/Organization
        elif any(x in placeholder_lower + name_lower for x in ["company", "organization", "business"]):
            return random.choice(["Test Company", "Demo Corp", "Sample Business"])
        
        # Address fields
        elif any(x in placeholder_lower + name_lower for x in ["address", "street", "city", "zip"]):
            return random.choice(["123 Main St", "Demo City", "12345"])
        
        # Generic text
        else:
            return random.choice(["test", "demo", "sample", "information"])
    
    async def _menu_navigation_activity(self, page):
        """Navigate through site menus"""
        
        try:
            # Look for navigation menus
            nav_selectors = [
                "nav a:visible", 
                ".navigation a:visible", 
                ".navbar a:visible",
                ".menu a:visible", 
                ".nav-menu a:visible",
                "header a:visible"
            ]
            
            for selector in nav_selectors:
                try:
                    nav_links = await page.locator(selector).all()
                    
                    if nav_links:
                        # Choose 1-2 navigation items to explore
                        explore_count = min(random.randint(1, 2), len(nav_links))
                        
                        for _ in range(explore_count):
                            nav_link = random.choice(nav_links)
                            
                            if await nav_link.is_visible():
                                text = await nav_link.inner_text()
                                
                                # Skip unwanted navigation items
                                if not any(x in text.lower() for x in [
                                    'logout', 'login', 'signup', 'register', 'cart', 'checkout'
                                ]):
                                    logger.info(f"[NAV] Exploring navigation: {text[:30]}")
                                    
                                    # Hover first
                                    await nav_link.hover()
                                    await asyncio.sleep(random.uniform(1, 2))
                                    
                                    # Maybe click (50% chance)
                                    if random.random() < 0.5:
                                        await nav_link.click()
                                        await page.wait_for_load_state('networkidle', timeout=8000)
                                        await asyncio.sleep(random.uniform(3, 8))
                                        
                                        # Go back
                                        await page.go_back()
                                        await page.wait_for_load_state('networkidle', timeout=8000)
                                        await asyncio.sleep(random.uniform(1, 3))
                        
                        return True
                        
                except Exception as e:
                    logger.debug(f"[WARN] Navigation failed for {selector}: {e}")
                    continue
            
        except Exception as e:
            logger.debug(f"[WARN] Menu navigation failed: {e}")
        
        return False
    
    async def _search_on_site_activity(self, page):
        """Use the site's search functionality"""
        
        try:
            # Find search inputs
            search_selectors = [
                "input[type='search']:visible",
                "input[placeholder*='search' i]:visible",
                ".search-input:visible",
                "#search:visible",
                ".search-box input:visible"
            ]
            
            for selector in search_selectors:
                try:
                    search_inputs = await page.locator(selector).all()
                    
                    if search_inputs:
                        search_input = search_inputs[0]
                        
                        if await search_input.is_visible() and await search_input.is_enabled():
                            
                            # Click on search box
                            await search_input.click()
                            await asyncio.sleep(random.uniform(0.5, 1))
                            
                            # Clear any existing content
                            await search_input.clear()
                            await asyncio.sleep(random.uniform(0.2, 0.5))
                            
                            # Choose search term
                            search_terms = [
                                "product", "service", "information", "help", 
                                "contact", "about", "support", "pricing"
                            ]
                            search_term = random.choice(search_terms)
                            
                            logger.info(f"[SEARCH] Searching for: {search_term}")
                            
                            # Type search term
                            await self._human_like_typing(page, search_term)
                            await asyncio.sleep(random.uniform(1, 2))
                            
                            # Submit search (Enter key or search button)
                            try:
                                await search_input.press("Enter")
                            except:
                                # Look for search button
                                search_buttons = await page.locator("button[type='submit'], .search-button, input[type='submit']").all()
                                if search_buttons:
                                    await search_buttons[0].click()
                            
                            # Wait for search results
                            await page.wait_for_load_state('networkidle', timeout=8000)
                            await asyncio.sleep(random.uniform(3, 6))
                            
                            return True
                            
                except Exception as e:
                    logger.debug(f"[WARN] Search failed for {selector}: {e}")
                    continue
            
        except Exception as e:
            logger.debug(f"[WARN] Site search failed: {e}")
        
        return False
    
    async def _mouse_exploration_activity(self, page):
        """Explore page with natural mouse movements"""
        
        try:
            viewport = page.viewport_size
            
            # Simulate reading pattern with mouse following
            for _ in range(random.randint(3, 8)):
                # Random position on page
                x = random.randint(50, viewport["width"] - 50)
                y = random.randint(100, viewport["height"] - 100)
                
                # Move mouse with slight curve
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
                # Small movements (following text/content)
                for _ in range(random.randint(2, 5)):
                    x += random.randint(-20, 20)
                    y += random.randint(-10, 10)
                    
                    x = max(0, min(viewport["width"], x))
                    y = max(0, min(viewport["height"], y))
                    
                    await page.mouse.move(x, y)
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                
                # Pause (reading)
                await asyncio.sleep(random.uniform(1, 3))
            
        except Exception as e:
            logger.debug(f"[WARN] Mouse exploration failed: {e}")
    
    async def _scroll_and_read_activity(self, page):
        """Auto-scroll to simulate reading"""
        
        # Scroll down gradually
        scroll_distance = random.randint(200, 400)
        await page.mouse.wheel(0, scroll_distance)
        
        # Simulate reading time
        reading_time = random.uniform(2, 6)
        await asyncio.sleep(reading_time)
        
        # Occasionally scroll back up
        if random.random() < 0.3:
            await page.mouse.wheel(0, -random.randint(100, 200))
            await asyncio.sleep(random.uniform(1, 2))
    
    async def _hover_elements_activity(self, page):
        """Hover over buttons or links without clicking"""
        
        selectors = [
            "button", ".btn", "[role='button']",
            "a", ".link", 
            ".nav-item", ".menu-item",
            ".cta", ".call-to-action"
        ]
        
        for selector in selectors:
            try:
                elements = await page.locator(selector).all()
                if elements:
                    # Hover on 1-2 elements
                    hover_count = min(random.randint(1, 2), len(elements))
                    
                    for i in range(hover_count):
                        element = random.choice(elements)
                        if await element.is_visible():
                            await element.hover(timeout=3000)
                            await asyncio.sleep(random.uniform(1, 2))
                            
                            # Add mouse jitter
                            await self._add_mouse_jitter(page)
                    break
            except:
                continue
    
    async def _inactive_pause_activity(self):
        """Simulate user thinking or reading (inactivity)"""
        
        pause_duration = random.uniform(3, 10)
        logger.debug(f"[THINK] Inactive pause: {pause_duration:.1f}s")
        await asyncio.sleep(pause_duration)
    
    async def _mouse_jitter_activity(self, page):
        """Add realistic mouse jitter"""
        
        await self._add_mouse_jitter(page)
        await asyncio.sleep(random.uniform(0.5, 1.5))
    
    async def _simulate_reading(self, page, duration: float):
        """Simulate reading behavior with eye movement patterns"""
        
        reading_pattern = random.choice(["skimmer", "normal", "careful"])
        pattern_config = HumanSearchBehavior.READING_PATTERNS[reading_pattern]
        
        chunks = int(duration / 2)  # 2-second reading chunks
        
        for _ in range(chunks):
            # Simulate eye movement with small mouse movements
            if random.random() < pattern_config["pause_frequency"]:
                await self._add_mouse_jitter(page)
            
            await asyncio.sleep(2)


# ============================================================================
# JSON SEARCH PROCESSOR CLASS
# ============================================================================

class JSONSearchProcessor:
    """
    Processes JSON files with keyword-site pairs and runs search simulations
    """
    
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.search_simulator = GoogleSearchSimulator()
        self.results = []
    
    def load_search_data(self) -> List[Dict[str, str]]:
        """Load search data from JSON file"""
        
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"[FILE] Loaded {len(data)} search tasks from {self.json_file_path}")
            
            # Validate data structure
            for i, item in enumerate(data):
                if not isinstance(item, dict) or "keyword" not in item or "site" not in item:
                    raise ValueError(f"Invalid item at index {i}: {item}")
            
            return data
            
        except FileNotFoundError:
            logger.error(f"[FAIL] File not found: {self.json_file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"[FAIL] Invalid JSON format: {e}")
            raise
        except Exception as e:
            logger.error(f"[FAIL] Error loading search data: {e}")
            raise
    
    async def process_all_searches(self, delay_between_searches: int = 180, 
                                 randomize_order: bool = True) -> List[Dict[str, Any]]:
        """
        Process all search tasks from JSON file
        
        Args:
            delay_between_searches: Delay between searches in seconds (default 3 minutes)
            randomize_order: Whether to randomize the order of searches
        """
        
        search_data = self.load_search_data()
        
        if randomize_order:
            random.shuffle(search_data)
            logger.info("[SHUFFLE] Randomized search order")
        
        logger.info(f"[START] Starting {len(search_data)} search simulations")
        logger.info(f"[TIME] Estimated total time: {(len(search_data) * (delay_between_searches + 300)) / 60:.1f} minutes")
        
        all_results = []
        
        for i, search_task in enumerate(search_data):
            keyword = search_task["keyword"]
            site = search_task["site"]
            
            logger.info(f"\n[POS] Search {i+1}/{len(search_data)}: '{keyword}' -> {site}")
            
            try:
                # Run search simulation
                result = await self.search_simulator.simulate_search_session(keyword, site)
                all_results.append(result)
                
                # Log result
                if result.get("success"):
                    steps_count = len(result.get("steps", []))
                    duration = result.get("duration", 0)
                    logger.info(f"[OK] Search completed: {steps_count} steps, {duration:.1f}s")
                else:
                    error = result.get("error", "Unknown error")
                    logger.info(f"[FAIL] Search failed: {error}")
                
            except Exception as e:
                logger.error(f"[FAIL] Search simulation error: {e}")
                all_results.append({
                    "keyword": keyword,
                    "target_site": site,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
            
            # Delay between searches (except for last one)
            if i < len(search_data) - 1:
                # Add randomness to delay (±30 seconds)
                actual_delay = delay_between_searches + random.randint(-30, 30)
                logger.info(f"[WAIT] Waiting {actual_delay} seconds before next search...")
                await asyncio.sleep(actual_delay)
        
        # Generate summary
        successful = sum(1 for r in all_results if r.get("success", False))
        
        summary = {
            "total_searches": len(all_results),
            "successful_searches": successful,
            "success_rate": (successful / len(all_results)) * 100 if all_results else 0,
            "results": all_results,
            "processing_time": datetime.now().isoformat()
        }
        
        logger.info(f"\n[DONE] PROCESSING COMPLETE")
        logger.info(f"[STATS] Success rate: {successful}/{len(all_results)} ({summary['success_rate']:.1f}%)")
        
        self.results = summary
        return summary
    
    async def process_single_search(self, keyword: str, site: str) -> Dict[str, Any]:
        """Process a single search task"""
        
        logger.info(f"[SEARCH] Single search: '{keyword}' -> {site}")
        
        result = await self.search_simulator.simulate_search_session(keyword, site)
        
        if result.get("success"):
            logger.info(f"[OK] Search completed successfully")
        else:
            logger.info(f"[FAIL] Search failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def save_results(self, output_file: str):
        """Save results to JSON file"""
        
        if not self.results:
            logger.warning("[WARN] No results to save")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"[SAVE] Results saved to {output_file}")
            
        except Exception as e:
            logger.error(f"[FAIL] Failed to save results: {e}")


# ============================================================================
# MAIN FUNCTION AND CLI
# ============================================================================

async def main():
    """Main function with fixed Unicode logging"""
    
    # Ensure Unicode logging is set up
    setup_unicode_logging()
    
    parser = argparse.ArgumentParser(
        description="Google Search Simulator with Realistic Human Behavior (Fixed Unicode)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search_simulator.py search_data.json
  python search_simulator.py search_data.json --delay 300 --output results.json
        """
    )
    
    parser.add_argument("json_file", help="JSON file containing keyword-site pairs")
    parser.add_argument("--delay", type=int, default=180, help="Delay between searches in seconds")
    parser.add_argument("--output", type=str, help="Output file to save results")
    parser.add_argument("--randomize", action="store_true", help="Randomize order of searches")
    parser.add_argument("--single", nargs=2, metavar=("KEYWORD", "SITE"), help="Run single search")
    
    args = parser.parse_args()
    
    print("[START] Google Search Simulator - Fixed Version")
    print("=" * 50)
    
    try:
        if args.single:
            # Single search mode
            keyword, site = args.single
            print(f"[SEARCH] Single search mode")
            print(f"Keyword: {keyword}")
            print(f"Site: {site}")
            
            # Create processor for single search
            processor = JSONSearchProcessor("")
            result = await processor.process_single_search(keyword, site)
            
            print(f"\n[RESULT] {'[OK] SUCCESS' if result.get('success') else '[FAIL] FAILED'}")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, default=str, ensure_ascii=False)
                print(f"[SAVE] Result saved to {args.output}")
        
        else:
            # Batch processing mode
            print(f"[FILE] Input file: {args.json_file}")
            print(f"[TIME] Delay between searches: {args.delay}s")
            print(f"[SHUFFLE] Randomize order: {args.randomize}")
            
            # Create processor with our fixed GoogleSearchSimulator
            processor = JSONSearchProcessor(args.json_file)
            
            # Process all searches
            results = await processor.process_all_searches(
                delay_between_searches=args.delay,
                randomize_order=args.randomize
            )
            
            # Print summary
            print(f"\n[STATS] FINAL SUMMARY")
            print(f"[OK] Successful: {results['successful_searches']}/{results['total_searches']}")
            print(f"[STATS] Success rate: {results['success_rate']:.1f}%")
            
            # Save results if requested
            if args.output:
                processor.save_results(args.output)
    
    except KeyboardInterrupt:
        print("\n[WARN] Interrupted by user")
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        logger.error(f"Main execution error: {e}")


# ============================================================================
# QUICK TEST FUNCTION
# ============================================================================

async def quick_test():
    """Quick test with a simple search"""
    
    setup_unicode_logging()
    
    print("[TEST] Running quick test...")
    
    simulator = GoogleSearchSimulator()
    
    # Test with a simple, reliable target
    result = await simulator.simulate_search_session(
        keyword="wikipedia encyclopedia", 
        target_site="https://www.wikipedia.org/"
    )
    
    print(f"[RESULT] Test result: {'[OK] SUCCESS' if result.get('success') else '[FAIL] FAILED'}")
    print(f"[STATS] Steps completed: {len(result.get('steps', []))}")
    
    if result.get('error'):
        print(f"[ERROR] {result['error']}")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        asyncio.run(quick_test())
    else:
        asyncio.run(main())