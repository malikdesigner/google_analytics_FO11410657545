#!/usr/bin/env python3
"""
Realistic Site Browser - Google Search to Site Navigation
Performs human-like browsing from Google search to target site exploration

Features:
- Natural Google search behavior
- Realistic result scanning and hovering
- Target site clicking with delays
- Comprehensive site exploration (About, Contact, Blog, Products)
- Human-like scrolling, hovering, and timing
- Randomized browsing patterns

Input Format: "search for [keyword], scan 3-4 results, click target link, browse site 3–4 mins."
"""

import asyncio
import random
import time
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
import urllib.parse
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class BrowsingTask:
    """Structured browsing task"""
    keyword: str
    target_site: str
    scan_results_count: int
    browse_duration_mins: int
    hover_competitors: int = 3
    thinking_delays: bool = True

class RealisticBrowser:
    """Creates ultra-realistic browser sessions"""
    
    @staticmethod
    async def create_realistic_browser():
        """Create browser with realistic human-like settings"""
        
        p = await async_playwright().start()
        
        # Realistic browser arguments
        args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-automation',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-ipc-flooding-protection',
            '--disable-hang-monitor',
            '--disable-prompt-on-repost',
            '--disable-sync',
            '--force-color-profile=srgb',
            '--metrics-recording-only',
            '--disable-default-apps',
            '--no-default-browser-check',
            '--disable-background-networking',
            '--disable-client-side-phishing-detection',
            '--disable-component-update',
            '--disable-domain-reliability',
            '--disable-features=TranslateUI',
            '--hide-scrollbars',
            '--mute-audio',
            '--use-mock-keychain'
        ]
        
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=random.randint(50, 150),
            args=args
        )
        
        return browser, p
    
    @staticmethod
    async def create_realistic_context(browser):
        """Create context with realistic settings"""
        
        # Realistic viewport sizes
        viewports = [
            {"width": 1366, "height": 768},
            {"width": 1920, "height": 1080},
            {"width": 1440, "height": 900},
            {"width": 1536, "height": 864},
            {"width": 1680, "height": 1050}
        ]
        
        viewport = random.choice(viewports)
        ua = UserAgent()
        
        context = await browser.new_context(
            user_agent=ua.random,
            locale="en-US",
            timezone_id=random.choice(["America/New_York", "America/Los_Angeles", "America/Chicago"]),
            viewport=viewport,
            has_touch=False,
            is_mobile=False,
            device_scale_factor=1,
            permissions=["geolocation"],
            geolocation={"latitude": 40.7128, "longitude": -74.0060},
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
        )
        
        # Anti-detection script
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            
            window.chrome = {
                runtime: {},
                loadTimes: function() {
                    return {
                        commitLoadTime: Date.now() / 1000 - Math.random() * 100,
                        finishDocumentLoadTime: Date.now() / 1000 - Math.random() * 50,
                        finishLoadTime: Date.now() / 1000 - Math.random() * 25,
                        requestTime: Date.now() / 1000 - Math.random() * 150,
                        startLoadTime: Date.now() / 1000 - Math.random() * 200
                    };
                }
            };
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {
                        0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                        description: "Portable Document Format",
                        filename: "internal-pdf-viewer",
                        length: 1,
                        name: "Chrome PDF Plugin"
                    }
                ],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        """)
        
        return context

class GoogleSearcher:
    """Handles realistic Google searching behavior"""
    
    def __init__(self, page):
        self.page = page
        
    async def perform_search(self, keyword: str) -> bool:
        """Perform realistic Google search"""
        
        try:
            logger.info(f"🔍 Searching for: '{keyword}'")
            
            # Navigate to Google
            await self.page.goto("https://www.google.com", wait_until='networkidle')
            await asyncio.sleep(random.uniform(1, 3))
            
            # Find search box
            search_box = await self._find_search_box()
            if not search_box:
                return False
            
            # Perform human-like search
            await self._human_like_search(search_box, keyword)
            
            # Wait for results
            await self.page.wait_for_load_state('networkidle', timeout=20000)
            await asyncio.sleep(random.uniform(2, 4))
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return False
    
    async def _find_search_box(self):
        """Find Google search box with multiple selectors"""
        
        selectors = [
            "input[name='q']",
            "textarea[name='q']",
            "input[title='Search']",
            ".gLFyf",
            "#APjFqb"
        ]
        
        for selector in selectors:
            try:
                element = self.page.locator(selector).first
                if await element.count() > 0:
                    await element.wait_for(state='visible', timeout=5000)
                    return element
            except:
                continue
        
        logger.error("❌ Could not find search box")
        return None
    
    async def _human_like_search(self, search_box, keyword: str):
        """Perform human-like search typing and submission"""
        
        # Click search box
        await search_box.click()
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Clear any existing content
        await search_box.clear()
        await asyncio.sleep(random.uniform(0.3, 0.8))
        
        # Type with human-like rhythm
        logger.info(f"⌨️ Typing: '{keyword}'")
        for i, char in enumerate(keyword):
            typing_delay = random.uniform(0.08, 0.25)
            
            # Natural variations
            if i == 0:
                typing_delay *= 1.5  # Slower start
            elif char == ' ':
                typing_delay *= 2.0  # Pause at spaces
            elif char in 'aeiou':
                typing_delay *= 0.8  # Faster vowels
            
            # Occasional thinking pauses
            if random.random() < 0.1:
                typing_delay += random.uniform(0.3, 1.0)
            
            await self.page.keyboard.type(char)
            await asyncio.sleep(typing_delay)
        
        # Thinking pause before submitting
        thinking_time = random.uniform(1.0, 3.5)
        logger.info(f"🤔 Thinking for {thinking_time:.1f}s before submitting...")
        await asyncio.sleep(thinking_time)
        
        # Submit search
        await self.page.keyboard.press("Enter")

class ResultScanner:
    """Handles realistic search result scanning and interaction"""
    
    def __init__(self, page):
        self.page = page
        
    async def scan_and_hover_results(self, scan_count: int, hover_competitors: int) -> List[Dict]:
        """Scan search results and hover on competitors"""
        
        logger.info(f"👀 Scanning {scan_count} results, hovering on {hover_competitors} competitors")
        
        try:
            # Wait for results to load
            await asyncio.sleep(random.uniform(2, 4))
            
            # Initial page scan (scrolling)
            await self._initial_page_scan()
            
            # Get all result links
            result_links = await self._get_result_links()
            
            if not result_links:
                logger.warning("⚠️ No search results found")
                return []
            
            logger.info(f"📊 Found {len(result_links)} search results")
            
            # Hover on competitor results
            await self._hover_on_competitors(result_links, hover_competitors)
            
            return result_links
            
        except Exception as e:
            logger.error(f"❌ Result scanning failed: {e}")
            return []
    
    async def _initial_page_scan(self):
        """Initial scanning of the search results page"""
        
        # Scroll down to see more results
        scroll_sessions = random.randint(2, 4)
        
        for i in range(scroll_sessions):
            scroll_distance = random.randint(200, 500)
            await self.page.mouse.wheel(0, scroll_distance)
            
            # Reading pause
            reading_time = random.uniform(1.5, 3.5)
            await asyncio.sleep(reading_time)
            
            # Occasional mouse movement
            if random.random() < 0.4:
                await self.page.mouse.move(
                    random.randint(200, 800),
                    random.randint(200, 600)
                )
        
        # Scroll back to top to start clicking
        await self.page.keyboard.press("Home")
        await asyncio.sleep(random.uniform(1, 2))
    
    async def _get_result_links(self) -> List[Dict]:
        """Extract search result links with metadata"""
        
        result_data = []
        
        # Multiple selectors for different Google layouts
        link_selectors = [
            "h3 a",
            ".yuRUbf a",
            ".g a[href*='http']:not([href*='google'])",
            "[data-ved] a[href*='http']:not([href*='google'])"
        ]
        
        for selector in link_selectors:
            try:
                links = await self.page.locator(selector).all()
                
                for link in links:
                    try:
                        href = await link.get_attribute("href")
                        text = await link.inner_text()
                        
                        if href and text and "google" not in href:
                            result_data.append({
                                "element": link,
                                "href": href,
                                "text": text.strip()[:100],
                                "selector": selector
                            })
                    except:
                        continue
                
                if result_data:
                    break  # Found results with this selector
                    
            except:
                continue
        
        # Remove duplicates based on href
        unique_results = []
        seen_hrefs = set()
        
        for result in result_data:
            if result["href"] not in seen_hrefs:
                unique_results.append(result)
                seen_hrefs.add(result["href"])
        
        return unique_results[:10]  # Limit to top 10 results
    
    async def _hover_on_competitors(self, result_links: List[Dict], hover_count: int):
        """Hover on competitor results before clicking target"""
        
        if not result_links:
            return
        
        # Select random competitors to hover on
        competitors_to_hover = random.sample(
            result_links[:8],  # From top 8 results
            min(hover_count, len(result_links))
        )
        
        for i, competitor in enumerate(competitors_to_hover):
            try:
                logger.info(f"🔍 Hovering on competitor {i+1}: {competitor['text'][:50]}...")
                
                # Hover on the competitor link
                await competitor["element"].hover()
                
                # Realistic hover duration (reading snippet)
                hover_duration = random.uniform(2.0, 4.5)
                await asyncio.sleep(hover_duration)
                
                # Occasional additional mouse movements
                if random.random() < 0.3:
                    await self.page.mouse.move(
                        random.randint(100, 300),
                        random.randint(100, 200),
                        steps=random.randint(3, 8)
                    )
                
            except Exception as e:
                logger.warning(f"⚠️ Could not hover on competitor: {e}")
                continue

class TargetSiteClicker:
    """Handles realistic target site clicking behavior"""
    
    def __init__(self, page):
        self.page = page
        
    async def find_and_click_target(self, result_links: List[Dict], target_site: str) -> bool:
        """Find target site and click with realistic behavior"""
        
        logger.info(f"🎯 Looking for target site: {target_site}")
        
        # Find target site in results
        target_result = None
        for result in result_links:
            if target_site.lower() in result["href"].lower():
                target_result = result
                break
        
        if not target_result:
            logger.warning(f"⚠️ Target site {target_site} not found in results")
            # Debug: Show available results
            logger.info("Available results:")
            for i, result in enumerate(result_links[:5]):
                logger.info(f"  {i+1}. {result['href']} - {result['text'][:50]}")
            return False
        
        logger.info(f"✅ Found target site: {target_result['text'][:50]}")
        
        # Realistic pre-click behavior
        await self._pre_click_behavior(target_result)
        
        # Click target site
        await self._click_target_with_delay(target_result)
        
        return True
    
    async def _pre_click_behavior(self, target_result: Dict):
        """Realistic behavior before clicking target"""
        
        logger.info("👀 Analyzing target site snippet...")
        
        # Hover on target site title/snippet
        await target_result["element"].hover()
        
        # Reading/analysis time
        analysis_time = random.uniform(2.5, 5.0)
        await asyncio.sleep(analysis_time)
        
        # Slight mouse movements (user considering the click)
        for _ in range(random.randint(1, 3)):
            current_box = await target_result["element"].bounding_box()
            if current_box:
                await self.page.mouse.move(
                    current_box['x'] + random.randint(-20, 20),
                    current_box['y'] + random.randint(-10, 10),
                    steps=random.randint(3, 6)
                )
            await asyncio.sleep(random.uniform(0.5, 1.5))
    
    async def _click_target_with_delay(self, target_result: Dict):
        """Click target with realistic delay and precision"""
        
        # Random delay before clicking (user decision time)
        click_delay = random.uniform(1.5, 6.0)
        logger.info(f"⏳ Preparing to click in {click_delay:.1f}s...")
        await asyncio.sleep(click_delay)
        
        try:
            # Get element position for natural clicking
            box = await target_result["element"].bounding_box()
            
            if box:
                # Click in a natural position within the element
                click_x = box['x'] + box['width'] * random.uniform(0.2, 0.8)
                click_y = box['y'] + box['height'] * random.uniform(0.3, 0.7)
                
                # Move to click position naturally
                await self.page.mouse.move(click_x, click_y, steps=random.randint(5, 12))
                await asyncio.sleep(random.uniform(0.2, 0.8))
                
                # Click
                await self.page.mouse.click(click_x, click_y)
                logger.info("🖱️ Clicked target site")
            else:
                # Fallback: direct element click
                await target_result["element"].click()
                logger.info("🖱️ Clicked target site (fallback method)")
            
            # Wait for navigation
            await self.page.wait_for_load_state('networkidle', timeout=15000)
            
        except Exception as e:
            logger.error(f"❌ Click failed: {e}")
            raise

class SiteBrowser:
    """Handles realistic website browsing behavior"""
    
    def __init__(self, page):
        self.page = page
        self.pages_visited = []
        
    async def browse_site_realistically(self, duration_minutes: int, target_site: str) -> bool:
        """Browse target site with realistic human behavior"""
        
        logger.info(f"🌐 Starting {duration_minutes}-minute browsing session on {target_site}")
        
        total_time = duration_minutes * 60
        start_time = time.time()
        
        try:
            # Verify we're on the target site
            current_url = self.page.url
            if target_site.lower() not in current_url.lower():
                logger.warning(f"⚠️ Not on target site. Current: {current_url}")
                return False
            
            # Initial page analysis and interaction
            await self._analyze_landing_page()
            
            # Browse multiple pages
            pages_to_visit = random.randint(3, 5)
            time_per_page = total_time / pages_to_visit
            
            for page_num in range(pages_to_visit):
                elapsed = time.time() - start_time
                
                if elapsed >= total_time:
                    logger.info("⏰ Time limit reached")
                    break
                
                logger.info(f"📄 Browsing page {page_num + 1}/{pages_to_visit}")
                
                # Browse current page
                await self._browse_current_page(time_per_page * 0.7)  # 70% of time on content
                
                # Navigate to next page (if not last)
                if page_num < pages_to_visit - 1:
                    navigation_success = await self._navigate_to_next_page()
                    if not navigation_success:
                        logger.info("🔄 Could not navigate to next page, continuing on current page")
                        await self._browse_current_page(time_per_page * 0.3)
            
            # Final activity before leaving
            await self._final_site_activity()
            
            total_browsing_time = time.time() - start_time
            logger.info(f"✅ Browsing session completed ({total_browsing_time:.1f}s)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Site browsing failed: {e}")
            return False
    
    async def _analyze_landing_page(self):
        """Analyze and interact with the landing page"""
        
        logger.info("🔍 Analyzing landing page...")
        
        # Initial page load settling time
        await asyncio.sleep(random.uniform(2, 4))
        
        # Get page info
        try:
            page_title = await self.page.title()
            current_url = self.page.url
            
            self.pages_visited.append({
                "title": page_title,
                "url": current_url,
                "timestamp": time.time()
            })
            
            logger.info(f"📄 Page: {page_title}")
        except:
            pass
        
        # Initial scroll to see page layout
        await self._realistic_page_scroll(3)
    
    async def _browse_current_page(self, time_allocation: float):
        """Browse current page with realistic patterns"""
        
        start_time = time.time()
        
        while (time.time() - start_time) < time_allocation:
            activity = random.choice([
                "scroll_and_read",
                "hover_elements", 
                "thinking_pause",
                "detailed_reading"
            ])
            
            if activity == "scroll_and_read":
                await self._realistic_page_scroll(random.randint(2, 5))
                
            elif activity == "hover_elements":
                await self._hover_on_page_elements()
                
            elif activity == "thinking_pause":
                await self._user_thinking_pause()
                
            elif activity == "detailed_reading":
                await self._detailed_content_reading()
            
            # Check time limit
            if (time.time() - start_time) >= time_allocation:
                break
    
    async def _realistic_page_scroll(self, scroll_count: int):
        """Perform realistic page scrolling"""
        
        for _ in range(scroll_count):
            # Variable scroll distances
            scroll_distance = random.randint(200, 600)
            await self.page.mouse.wheel(0, scroll_distance)
            
            # Reading pause
            reading_time = random.uniform(1.5, 4.0)
            await asyncio.sleep(reading_time)
            
            # Occasional reverse scroll (user went too far)
            if random.random() < 0.15:  # 15% chance
                await self.page.mouse.wheel(0, -random.randint(100, 300))
                await asyncio.sleep(random.uniform(1, 2))
    
    async def _hover_on_page_elements(self):
        """Hover on various page elements (buttons, links, images)"""
        
        try:
            # Find hoverable elements
            hoverable_selectors = [
                "button",
                ".btn",
                "a[href]",
                ".button",
                "[role='button']",
                "img",
                ".card",
                ".product",
                ".service"
            ]
            
            elements_found = []
            
            for selector in hoverable_selectors:
                try:
                    elements = await self.page.locator(selector).all()
                    elements_found.extend(elements[:3])  # Max 3 per selector
                except:
                    continue
            
            if elements_found:
                # Hover on 1-3 random elements
                elements_to_hover = random.sample(
                    elements_found, 
                    min(random.randint(1, 3), len(elements_found))
                )
                
                for element in elements_to_hover:
                    try:
                        # Check if element is visible
                        if await element.is_visible():
                            await element.hover()
                            hover_time = random.uniform(1.0, 3.0)
                            await asyncio.sleep(hover_time)
                            
                            logger.info("🖱️ Hovered on page element")
                    except:
                        continue
        
        except Exception as e:
            logger.debug(f"Hover activity failed: {e}")
    
    async def _user_thinking_pause(self):
        """Simulate user thinking or reading pause"""
        
        thinking_time = random.uniform(3.0, 8.0)
        logger.info(f"🤔 User thinking pause ({thinking_time:.1f}s)")
        await asyncio.sleep(thinking_time)
    
    async def _detailed_content_reading(self):
        """Simulate detailed content reading with minimal scrolling"""
        
        # Small, careful scrolls (reading mode)
        for _ in range(random.randint(2, 4)):
            await self.page.mouse.wheel(0, random.randint(50, 150))
            reading_time = random.uniform(3.0, 6.0)
            await asyncio.sleep(reading_time)
    
    async def _navigate_to_next_page(self) -> bool:
        """Navigate to another page on the site"""
        
        # Common page types to look for
        navigation_targets = [
            {"keywords": ["about", "about us"], "priority": 1},
            {"keywords": ["contact", "contact us"], "priority": 1},
            {"keywords": ["blog", "news", "articles"], "priority": 2},
            {"keywords": ["products", "services"], "priority": 1},
            {"keywords": ["portfolio", "work", "projects"], "priority": 2},
            {"keywords": ["team", "staff"], "priority": 3},
            {"keywords": ["faq", "help", "support"], "priority": 3}
        ]
        
        try:
            # Get all links on the page
            links = await self.page.locator("a[href]").all()
            
            # Find navigation candidates
            navigation_candidates = []
            
            for link in links:
                try:
                    href = await link.get_attribute("href")
                    text = await link.inner_text()
                    
                    if href and text:
                        text_lower = text.lower().strip()
                        href_lower = href.lower()
                        
                        # Check if it's an internal link
                        if (href.startswith('/') or 
                            self.page.url.split('/')[2] in href):
                            
                            # Check against navigation targets
                            for target in navigation_targets:
                                if any(keyword in text_lower or keyword in href_lower 
                                      for keyword in target["keywords"]):
                                    
                                    # Avoid already visited pages
                                    already_visited = any(href in visited["url"] 
                                                        for visited in self.pages_visited)
                                    
                                    if not already_visited:
                                        navigation_candidates.append({
                                            "element": link,
                                            "href": href,
                                            "text": text,
                                            "priority": target["priority"]
                                        })
                                    break
                except:
                    continue
            
            if not navigation_candidates:
                logger.info("🔍 No suitable navigation targets found")
                return False
            
            # Sort by priority and select
            navigation_candidates.sort(key=lambda x: x["priority"])
            chosen_link = random.choice(navigation_candidates[:3])  # From top 3 priorities
            
            logger.info(f"🔗 Navigating to: {chosen_link['text']} ({chosen_link['href']})")
            
            # Hover before clicking
            await chosen_link["element"].hover()
            await asyncio.sleep(random.uniform(1.0, 3.0))
            
            # Click with delay
            await asyncio.sleep(random.uniform(0.5, 2.0))
            await chosen_link["element"].click()
            
            # Wait for navigation
            await self.page.wait_for_load_state('networkidle', timeout=15000)
            
            # Record visited page
            try:
                new_title = await self.page.title()
                new_url = self.page.url
                
                self.pages_visited.append({
                    "title": new_title,
                    "url": new_url,
                    "timestamp": time.time()
                })
            except:
                pass
            
            return True
            
        except Exception as e:
            logger.warning(f"❌ Navigation failed: {e}")
            return False
    
    async def _final_site_activity(self):
        """Final activity before leaving the site"""
        
        logger.info("🏁 Final site activity...")
        
        # Final scroll to bottom
        await self.page.keyboard.press("End")
        await asyncio.sleep(random.uniform(2, 4))
        
        # Maybe scroll back up a bit
        if random.random() < 0.5:
            await self.page.mouse.wheel(0, -random.randint(200, 500))
            await asyncio.sleep(random.uniform(1, 3))

class RealisticSiteBrowser:
    """Main class orchestrating the entire realistic browsing process"""
    
    def __init__(self):
        self.session_data = []
        
    async def execute_browsing_task(self, task_prompt: str) -> bool:
        """
        Execute browsing task from natural language prompt
        
        Example prompts:
        - "search for web design agencies, scan 3-4 results, click invislondon.com, browse site 3–4 mins"
        - "search for digital marketing services, scan 5 results, click targetsite.com, browse 5 minutes"
        """
        
        logger.info(f"🚀 Executing browsing task: {task_prompt}")
        
        # Parse the task
        task = self._parse_task_prompt(task_prompt)
        if not task:
            logger.error("❌ Could not parse task prompt")
            return False
        
        logger.info(f"📋 Parsed task: {task}")
        
        # Create realistic browser
        browser, playwright_instance = await RealisticBrowser.create_realistic_browser()
        context = await RealisticBrowser.create_realistic_context(browser)
        page = await context.new_page()
        
        session_start = time.time()
        
        try:
            # Phase 1: Google Search
            logger.info("=" * 60)
            logger.info("PHASE 1: REALISTIC GOOGLE SEARCH")
            logger.info("=" * 60)
            
            searcher = GoogleSearcher(page)
            search_success = await searcher.perform_search(task.keyword)
            
            if not search_success:
                logger.error("❌ Google search failed")
                return False
            
            # Phase 2: Scan and Hover on Results
            logger.info("\n" + "=" * 60)
            logger.info("PHASE 2: SCAN AND HOVER ON RESULTS")
            logger.info("=" * 60)
            
            scanner = ResultScanner(page)
            result_links = await scanner.scan_and_hover_results(
                task.scan_results_count, 
                task.hover_competitors
            )
            
            if not result_links:
                logger.error("❌ No search results found")
                return False
            
            # Phase 3: Click Target Site
            logger.info("\n" + "=" * 60)
            logger.info("PHASE 3: CLICK TARGET SITE")
            logger.info("=" * 60)
            
            clicker = TargetSiteClicker(page)
            click_success = await clicker.find_and_click_target(result_links, task.target_site)
            
            if not click_success:
                logger.error("❌ Target site click failed")
                return False
            
            # Phase 4: Browse Target Site
            logger.info("\n" + "=" * 60)
            logger.info("PHASE 4: REALISTIC SITE BROWSING")
            logger.info("=" * 60)
            
            browser_obj = SiteBrowser(page)
            browse_success = await browser_obj.browse_site_realistically(
                task.browse_duration_mins, 
                task.target_site
            )
            
            # Record session data
            session_duration = time.time() - session_start
            
            self.session_data.append({
                "task_prompt": task_prompt,
                "keyword": task.keyword,
                "target_site": task.target_site,
                "scan_count": task.scan_results_count,
                "browse_duration": task.browse_duration_mins,
                "search_success": search_success,
                "click_success": click_success,
                "browse_success": browse_success,
                "pages_visited": browser_obj.pages_visited,
                "total_duration": session_duration,
                "final_url": page.url,
                "timestamp": session_start
            })
            
            logger.info("\n" + "=" * 60)
            logger.info("SESSION COMPLETE")
            logger.info("=" * 60)
            logger.info(f"✅ Search: {'Success' if search_success else 'Failed'}")
            logger.info(f"✅ Click: {'Success' if click_success else 'Failed'}")
            logger.info(f"✅ Browse: {'Success' if browse_success else 'Failed'}")
            logger.info(f"📄 Pages Visited: {len(browser_obj.pages_visited)}")
            logger.info(f"⏱️ Total Duration: {session_duration:.1f}s")
            logger.info(f"🌐 Final URL: {page.url}")
            
            overall_success = search_success and click_success and browse_success
            return overall_success
            
        except Exception as e:
            logger.error(f"❌ Session error: {e}")
            return False
        
        finally:
            # Cleanup
            await asyncio.sleep(random.uniform(2, 5))
            try:
                await browser.close()
                await playwright_instance.stop()
            except:
                pass
    
    def _parse_task_prompt(self, prompt: str) -> Optional[BrowsingTask]:
        """Parse natural language task prompt into structured task"""
        
        try:
            prompt_lower = prompt.lower()
            
            # Extract keyword (after "search for")
            keyword = None
            if "search for" in prompt_lower:
                keyword_start = prompt_lower.find("search for") + len("search for")
                keyword_part = prompt[keyword_start:].strip()
                
                # Find end of keyword (before comma or "scan")
                keyword_end_markers = [",", "scan", "click"]
                keyword_end = len(keyword_part)
                
                for marker in keyword_end_markers:
                    marker_pos = keyword_part.lower().find(marker)
                    if marker_pos != -1:
                        keyword_end = min(keyword_end, marker_pos)
                
                keyword = keyword_part[:keyword_end].strip()
            
            # Extract scan count
            scan_count = 4  # default
            if "scan" in prompt_lower:
                import re
                scan_match = re.search(r'scan\s+(\d+)[-–]?(\d+)?', prompt_lower)
                if scan_match:
                    if scan_match.group(2):  # Range like "3-4"
                        scan_count = random.randint(int(scan_match.group(1)), int(scan_match.group(2)))
                    else:  # Single number
                        scan_count = int(scan_match.group(1))
            
            # Extract target site
            target_site = None
            if "click" in prompt_lower:
                click_start = prompt_lower.find("click") + len("click")
                click_part = prompt[click_start:].strip()
                
                # Find target site (usually domain name)
                import re
                domain_match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', click_part)
                if domain_match:
                    target_site = domain_match.group(1)
            
            # Extract browse duration
            browse_duration = 3  # default 3 minutes
            if "browse" in prompt_lower:
                import re
                duration_match = re.search(r'browse[^0-9]*(\d+)[-–]?(\d+)?\s*(min|minutes)', prompt_lower)
                if duration_match:
                    if duration_match.group(2):  # Range like "3-4"
                        browse_duration = random.randint(int(duration_match.group(1)), int(duration_match.group(2)))
                    else:  # Single number
                        browse_duration = int(duration_match.group(1))
            
            if not keyword or not target_site:
                logger.error(f"❌ Could not extract keyword or target site from: {prompt}")
                return None
            
            return BrowsingTask(
                keyword=keyword,
                target_site=target_site,
                scan_results_count=scan_count,
                browse_duration_mins=browse_duration,
                hover_competitors=random.randint(2, 4),
                thinking_delays=True
            )
            
        except Exception as e:
            logger.error(f"❌ Error parsing prompt: {e}")
            return None
    
    def generate_session_report(self):
        """Generate detailed session report"""
        
        if not self.session_data:
            logger.warning("No session data available")
            return
        
        total_sessions = len(self.session_data)
        successful_sessions = sum(1 for s in self.session_data 
                                if s["search_success"] and s["click_success"] and s["browse_success"])
        
        report = {
            "summary": {
                "total_sessions": total_sessions,
                "successful_sessions": successful_sessions,
                "success_rate": f"{successful_sessions/total_sessions*100:.1f}%",
                "average_duration": f"{sum(s['total_duration'] for s in self.session_data)/total_sessions:.1f}s",
                "total_pages_visited": sum(len(s['pages_visited']) for s in self.session_data),
                "average_pages_per_session": f"{sum(len(s['pages_visited']) for s in self.session_data)/total_sessions:.1f}"
            },
            "sessions": self.session_data
        }
        
        # Save report
        filename = f"realistic_browsing_report_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"📊 Session report saved to {filename}")
        
        # Print summary
        print("\n" + "="*70)
        print("REALISTIC BROWSING SESSION REPORT")
        print("="*70)
        print(f"Total Sessions: {total_sessions}")
        print(f"Successful Sessions: {successful_sessions}")
        print(f"Success Rate: {successful_sessions/total_sessions*100:.1f}%")
        print(f"Average Duration: {sum(s['total_duration'] for s in self.session_data)/total_sessions:.1f}s")
        print(f"Total Pages Visited: {sum(len(s['pages_visited']) for s in self.session_data)}")
        print(f"Average Pages per Session: {sum(len(s['pages_visited']) for s in self.session_data)/total_sessions:.1f}")
        print("="*70)

# Convenience functions for easy usage
async def browse_site_from_search(task_prompt: str) -> bool:
    """
    Convenience function to execute a single browsing task
    
    Example usage:
    await browse_site_from_search("search for web design agencies, scan 4 results, click invislondon.com, browse site 3 minutes")
    """
    
    browser = RealisticSiteBrowser()
    return await browser.execute_browsing_task(task_prompt)

async def run_multiple_browsing_tasks(tasks: List[str]) -> Dict[str, Any]:
    """
    Run multiple browsing tasks and return comprehensive results
    
    Example usage:
    tasks = [
        "search for web design agencies, scan 3 results, click invislondon.com, browse 3 minutes",
        "search for digital marketing, scan 4 results, click targetsite.com, browse 4 minutes"
    ]
    results = await run_multiple_browsing_tasks(tasks)
    """
    
    browser = RealisticSiteBrowser()
    results = []
    
    for i, task in enumerate(tasks, 1):
        logger.info(f"\n🎬 Executing Task {i}/{len(tasks)}")
        logger.info(f"📝 Task: {task}")
        
        success = await browser.execute_browsing_task(task)
        results.append(success)
        
        # Delay between tasks (to avoid detection)
        if i < len(tasks):
            delay = random.uniform(60, 180)  # 1-3 minutes between tasks
            logger.info(f"⏳ Waiting {delay:.1f}s before next task...")
            await asyncio.sleep(delay)
    
    # Generate report
    browser.generate_session_report()
    
    return {
        "tasks_completed": len(tasks),
        "tasks_successful": sum(results),
        "success_rate": f"{sum(results)/len(tasks)*100:.1f}%",
        "session_data": browser.session_data
    }

# Example usage and testing
async def run_example_browsing_session():
    """Example of how to use the realistic browsing system"""
    
    print("🚀 Starting Realistic Site Browsing Example")
    print("=" * 60)
    
    # Example tasks with different patterns
    example_tasks = [
        "search for web design agencies london, scan 4 results, click invislondon.com, browse site 3 minutes",
        "search for digital marketing services, scan 3 results, click invislondon.com, browse 4 minutes",
        "search for seo companies, scan 5 results, click invislondon.com, browse site 2 minutes"
    ]
    
    # Run multiple tasks
    results = await run_multiple_browsing_tasks(example_tasks)
    
    print("\n🎯 FINAL RESULTS")
    print("=" * 30)
    print(f"Tasks Completed: {results['tasks_completed']}")
    print(f"Tasks Successful: {results['tasks_successful']}")
    print(f"Success Rate: {results['success_rate']}")

# Single task example
async def run_single_task_example():
    """Example of running a single browsing task"""
    
    print("🚀 Single Task Example")
    print("=" * 30)
    
    task = "search for web design agencies, scan 4 results, click invislondon.com, browse site 3 minutes"
    
    success = await browse_site_from_search(task)
    
    print(f"\n🎯 Task Result: {'✅ SUCCESS' if success else '❌ FAILED'}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "single":
            print("Running single task example...")
            asyncio.run(run_single_task_example())
        elif sys.argv[1] == "custom" and len(sys.argv) > 2:
            custom_task = " ".join(sys.argv[2:])
            print(f"Running custom task: {custom_task}")
            asyncio.run(browse_site_from_search(custom_task))
        else:
            print("Running multiple tasks example...")
            asyncio.run(run_example_browsing_session())
    else:
        print("🤖 Realistic Site Browser")
        print("=" * 40)
        print("Usage:")
        print("  python realistic_site_browser.py                    - Run example with multiple tasks")
        print("  python realistic_site_browser.py single             - Run single task example")
        print("  python realistic_site_browser.py custom [task]      - Run custom task")
        print()
        print("Example custom task:")
        print("  python realistic_site_browser.py custom \"search for web design, scan 3 results, click invislondon.com, browse 4 minutes\"")
        print()
        print("🚀 Running default example...")
        asyncio.run(run_example_browsing_session())