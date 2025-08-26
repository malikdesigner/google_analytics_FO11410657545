#site_activity.py
"""
SITE ACTIVITY MODULE
Handles target site browsing with enhanced human-like behavior
Updated for Browserless compatibility
"""

import asyncio
import random
import time
import logging
from datetime import datetime
from typing import Dict, Any, List

from model_integration import UserPersona

class SiteActivityManager:
    """Site Activity Manager with enhanced human-like browsing and Browserless support"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.use_browserless = self.config.get('use_browserless', True)
    
    async def visit_target_site_enhanced(self, page, target_site: str, session_data: Dict,
                                       autowebglm, usimagent, persona: UserPersona) -> bool:
        """Enhanced target site visit with human-like browsing"""
        
        backend = "Browserless" if self.use_browserless else "Chromium"
        logging.info(f"Visiting target site with enhanced human-like behavior using {backend}")
        
        try:
            # Wait for page load with extended timeout for Browserless
            timeout = 30000 if self.use_browserless else 25000
            await page.wait_for_load_state('networkidle', timeout=timeout)
            await asyncio.sleep(random.uniform(2, 5))
            
            current_url = page.url
            logging.info(f"Reached: {current_url}")
            
            # Enhanced page analysis
            page_context = await autowebglm.analyze_page_context(page)
            
            # Calculate enhanced session duration
            session_duration = self._calculate_enhanced_session_duration(page_context, persona)
            
            # Execute enhanced human-like browsing
            activities = await self._execute_enhanced_browsing(
                page, session_duration, page_context, session_data, usimagent, persona
            )
            
            session_data["steps"].append({
                "action": "visit_target_site_enhanced",
                "final_url": current_url,
                "page_analysis": page_context,
                "browsing_activities": activities,
                "session_duration": session_duration,
                "browser_backend": backend,
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            return True
            
        except Exception as e:
            logging.error(f"Enhanced target site visit failed: {e}")
            session_data["steps"].append({
                "action": "visit_target_site_failed",
                "error": str(e),
                "browser_backend": backend,
                "timestamp": datetime.now().isoformat(),
                "success": False
            })
            return False
    
    def _calculate_enhanced_session_duration(self, page_context: Dict, persona: UserPersona) -> int:
        """Calculate enhanced session duration based on analysis and persona"""
        
        # Base duration from persona
        min_duration, max_duration = persona.session_duration_range
        base_duration = random.randint(min_duration, max_duration)
        
        # Adjust based on page analysis
        page_type = page_context.get("page_type", "general_page")
        interactive_elements = page_context.get("interactive_elements", {})
        
        # Page type multipliers
        type_multipliers = {
            "ecommerce": 1.3,
            "content_page": 1.2,
            "homepage": 1.1,
            "social_media": 0.8,
            "search_results": 0.7,
            "general_page": 1.0
        }
        
        multiplier = type_multipliers.get(page_type, 1.0)
        
        # Adjust for interactive elements
        total_elements = interactive_elements.get("total", 0)
        if total_elements > 20:
            multiplier *= 1.2
        elif total_elements < 5:
            multiplier *= 0.8
        
        # Persona-specific adjustments
        if persona.reading_pattern == "thorough":
            multiplier *= 1.3
        elif persona.reading_pattern == "skimmer":
            multiplier *= 0.7
        
        # Browserless adjustment (slightly longer for cloud latency)
        if self.use_browserless:
            multiplier *= 1.1
        
        final_duration = int(base_duration * multiplier)
        return max(30, min(1200, final_duration))  # Between 30s and 20min
    
    async def _execute_enhanced_browsing(self, page, total_duration: int, page_context: Dict,
                                       session_data: Dict, usimagent, persona: UserPersona) -> List[str]:
        """Execute enhanced human-like browsing behavior"""
        
        start_time = time.time()
        end_time = start_time + total_duration
        activities = []
        
        backend = "Browserless" if self.use_browserless else "Chromium"
        logging.info(f"Executing {total_duration}s of enhanced human-like browsing with {backend}")
        
        # Initial page orientation
        await self._enhanced_page_orientation(page)
        activities.append("enhanced_page_orientation")
        
        action_count = 0
        while time.time() < end_time and action_count < 25:
            remaining_time = end_time - time.time()
            
            if remaining_time < 5:
                break
            
            # Check if should continue browsing
            if not usimagent.should_continue_browsing():
                logging.info("Enhanced USimAgent decided to stop browsing")
                break
            
            # Generate enhanced browsing action
            context = {
                "current_goal": "explore website content",
                "page_type": page_context.get("page_type", "unknown"),
                "session_duration": time.time() - start_time,
                "remaining_time": remaining_time,
                "interactive_elements": page_context.get("interactive_elements", {}),
                "hoverable_elements": page_context.get("hoverable_elements", {}),
                "browser_backend": backend
            }
            
            try:
                action = await usimagent.generate_next_action(context)
                activity = await self._execute_enhanced_browsing_action(page, action, persona)
                
                if activity:
                    activities.append(activity)
                    session_data["human_like_activities"].append({
                        "activity": activity,
                        "timestamp": datetime.now().isoformat(),
                        "action_details": action,
                        "browser_backend": backend
                    })
                
                # Record cognitive journey
                session_data.setdefault("cognitive_journey", []).append({
                    "time": time.time() - start_time,
                    "action": action.get("action_type"),
                    "confidence": action.get("confidence", 0.5),
                    "cognitive_load": usimagent.cognitive_load,
                    "interest_level": usimagent.interest_level,
                    "emotional_state": usimagent.emotional_state
                })
                
                action_count += 1
                
                # Slightly longer delays for Browserless to account for network latency
                if self.use_browserless:
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                
            except Exception as e:
                logging.debug(f"Enhanced browsing action failed: {e}")
                activities.append("failed_action")
                await asyncio.sleep(random.uniform(1, 3))
        
        logging.info(f"Completed enhanced browsing with {len(activities)} activities using {backend}")
        return activities
    
    async def _enhanced_page_orientation(self, page):
        """Enhanced page orientation behavior with Browserless compatibility"""
        
        try:
            # Human-like initial page scan
            await asyncio.sleep(random.uniform(1, 3))
            
            # Small initial scroll to see more content
            scroll_amount = random.randint(100, 300)
            await page.mouse.wheel(0, scroll_amount)
            
            # Wait longer for Browserless due to potential network latency
            wait_time = random.uniform(2, 4) if not self.use_browserless else random.uniform(3, 5)
            await asyncio.sleep(wait_time)
            
            # Scroll back up to start
            await page.mouse.wheel(0, -random.randint(50, 150))
            await asyncio.sleep(random.uniform(1, 2))
            
        except Exception as e:
            logging.debug(f"Enhanced page orientation failed: {e}")
    
    async def _execute_enhanced_browsing_action(self, page, action: Dict, persona: UserPersona) -> str:
        """Execute enhanced browsing action with Browserless compatibility"""
        
        action_type = action.get("action_type", "wait")
        parameters = action.get("parameters", {})
        
        try:
            if action_type == "hover_link":
                return await self._enhanced_hover_links(page, parameters)
            
            elif action_type == "hover_search_result":
                return await self._enhanced_hover_elements(page, parameters, "search_results")
            
            elif action_type == "hover_navigation":
                return await self._enhanced_hover_elements(page, parameters, "navigation")
            
            elif action_type == "scroll_down":
                return await self._enhanced_scroll_behavior(page, parameters)
            
            elif action_type == "scroll_up":
                return await self._enhanced_scroll_up(page, parameters)
            
            elif action_type == "read_content":
                return await self._enhanced_reading_behavior(page, parameters, persona)
            
            elif action_type == "wait_and_observe":
                return await self._enhanced_observation(page, parameters)
            
            elif action_type == "click_link":
                return await self._enhanced_link_clicking(page, parameters)
            
            elif action_type == "prepare_to_leave":
                return await self._prepare_to_leave_behavior(page, parameters)
            
            else:
                # Slightly longer wait for Browserless
                wait_time = random.uniform(1, 3) if not self.use_browserless else random.uniform(1.5, 4)
                await asyncio.sleep(wait_time)
                return "general_pause"
                
        except Exception as e:
            logging.debug(f"Enhanced browsing action execution failed: {action_type} - {e}")
            return f"failed_{action_type}"
    
    async def _enhanced_hover_links(self, page, parameters: Dict) -> str:
        """Enhanced link hovering behavior with Browserless optimization"""
        
        try:
            # Find various types of links
            link_selectors = [
                "a:visible",
                "nav a:visible",
                ".menu a:visible",
                ".navigation a:visible",
                "header a:visible",
                "footer a:visible"
            ]
            
            all_links = []
            for selector in link_selectors:
                try:
                    # Use count() first to avoid loading too many elements
                    count = await page.locator(selector).count()
                    if count > 0:
                        links = await page.locator(selector).all()
                        all_links.extend(links[:10])  # Limit per selector
                except Exception as e:
                    logging.debug(f"Link selector failed: {selector} - {e}")
                    continue
            
            if all_links:
                max_hovers = min(parameters.get("max_elements", 3), len(all_links))
                selected_links = random.sample(all_links, max_hovers)
                
                hovered_count = 0
                for link in selected_links:
                    try:
                        if await link.is_visible():
                            # Human-like approach
                            await self._human_like_element_approach(page, link)
                            await link.hover()
                            
                            # Hover duration based on persona and backend
                            duration = parameters.get("duration", 2)
                            if self.use_browserless:
                                duration *= random.uniform(1.1, 1.3)  # Slightly longer for Browserless
                            
                            await asyncio.sleep(duration)
                            hovered_count += 1
                            
                            # Pause between hovers
                            pause_time = random.uniform(0.5, 2.0)
                            if self.use_browserless:
                                pause_time *= 1.2
                            await asyncio.sleep(pause_time)
                    except Exception as e:
                        logging.debug(f"Link hover failed: {e}")
                        continue
                
                return f"hovered_{hovered_count}_links"
            
        except Exception as e:
            logging.debug(f"Enhanced link hovering failed: {e}")
        
        return "hover_links_failed"
    
    async def _enhanced_hover_elements(self, page, parameters: Dict, element_type: str) -> str:
        """Enhanced hovering for specific element types with Browserless support"""
        
        try:
            if element_type == "navigation":
                selectors = ["nav *:visible", ".nav *:visible", ".navigation *:visible", "header a:visible"]
            elif element_type == "search_results":
                selectors = [".result:visible", ".g:visible", "h3:visible", ".search-result:visible"]
            else:
                selectors = ["*:visible"]
            
            elements = []
            for selector in selectors:
                try:
                    count = await page.locator(selector).count()
                    if count > 0:
                        found = await page.locator(selector).all()
                        elements.extend(found[:8])
                except Exception as e:
                    logging.debug(f"Element selector failed: {selector} - {e}")
                    continue
            
            if elements:
                max_hovers = min(parameters.get("max_elements", 2), len(elements))
                selected = random.sample(elements, max_hovers)
                
                hovered_count = 0
                for element in selected:
                    try:
                        if await element.is_visible():
                            await element.hover()
                            
                            duration = parameters.get("duration", 2)
                            if self.use_browserless:
                                duration *= random.uniform(1.1, 1.2)
                                
                            await asyncio.sleep(duration)
                            hovered_count += 1
                            
                            pause_time = random.uniform(0.3, 1.5)
                            if self.use_browserless:
                                pause_time *= 1.1
                            await asyncio.sleep(pause_time)
                    except Exception as e:
                        logging.debug(f"Element hover failed: {e}")
                        continue
                
                return f"hovered_{hovered_count}_{element_type}"
            
        except Exception as e:
            logging.debug(f"Enhanced {element_type} hovering failed: {e}")
        
        return f"hover_{element_type}_failed"
    
    async def _enhanced_scroll_behavior(self, page, parameters: Dict) -> str:
        """Enhanced scrolling with human-like patterns and Browserless optimization"""
        
        try:
            amount = parameters.get("amount", 300)
            speed = parameters.get("speed", "normal")
            pause_probability = parameters.get("pause_probability", 0.5)
            
            # Adjust pause probability for Browserless
            if self.use_browserless:
                pause_probability *= 1.2
            
            if speed == "fast":
                # Quick scroll with occasional pauses
                await page.mouse.wheel(0, amount)
                if random.random() < pause_probability:
                    pause_time = random.uniform(0.5, 2.0)
                    if self.use_browserless:
                        pause_time *= 1.1
                    await asyncio.sleep(pause_time)
                return f"fast_scroll_{amount}px"
            
            elif speed == "slow":
                # Very gradual scroll with reading pauses
                steps = random.randint(3, 5)
                for i in range(steps):
                    await page.mouse.wheel(0, amount // steps)
                    if random.random() < pause_probability:
                        pause_time = random.uniform(1, 4)
                        if self.use_browserless:
                            pause_time *= 1.1
                        await asyncio.sleep(pause_time)
                    else:
                        base_pause = random.uniform(0.5, 1.5)
                        if self.use_browserless:
                            base_pause *= 1.1
                        await asyncio.sleep(base_pause)
                return f"slow_scroll_{amount}px_{steps}steps"
            
            else:
                # Normal scroll with natural pauses
                steps = 2
                for i in range(steps):
                    await page.mouse.wheel(0, amount // steps)
                    if random.random() < pause_probability:
                        pause_time = random.uniform(1, 3)
                        if self.use_browserless:
                            pause_time *= 1.1
                        await asyncio.sleep(pause_time)
                    else:
                        base_pause = random.uniform(0.3, 1.0)
                        if self.use_browserless:
                            base_pause *= 1.1
                        await asyncio.sleep(base_pause)
                return f"normal_scroll_{amount}px"
                
        except Exception as e:
            logging.debug(f"Enhanced scrolling failed: {e}")
            return "scroll_failed"
    
    async def _enhanced_scroll_up(self, page, parameters: Dict) -> str:
        """Enhanced upward scrolling with Browserless support"""
        
        try:
            amount = parameters.get("amount", 200)
            await page.mouse.wheel(0, -amount)
            
            wait_time = random.uniform(1, 3)
            if self.use_browserless:
                wait_time *= 1.1
            await asyncio.sleep(wait_time)
            
            return f"scroll_up_{amount}px"
        except:
            return "scroll_up_failed"
    
    async def _enhanced_reading_behavior(self, page, parameters: Dict, persona: UserPersona) -> str:
        """Enhanced reading simulation with Browserless considerations"""
        
        try:
            duration = parameters.get("duration", 10)
            
            # Adjust duration based on persona reading pattern
            if persona.reading_pattern == "thorough":
                duration *= 1.5
            elif persona.reading_pattern == "skimmer":
                duration *= 0.6
            
            # Slightly longer for Browserless to account for potential latency
            if self.use_browserless:
                duration *= 1.1
            
            # Simulate reading with occasional small scrolls
            read_segments = random.randint(1, 3)
            segment_duration = duration / read_segments
            
            for i in range(read_segments):
                await asyncio.sleep(segment_duration * 0.7)
                
                # Small scroll to simulate reading progress
                if random.random() < 0.6:
                    await page.mouse.wheel(0, random.randint(50, 150))
                    remaining_time = segment_duration * 0.3
                    if self.use_browserless:
                        remaining_time *= 1.1
                    await asyncio.sleep(remaining_time)
            
            return f"reading_{duration:.1f}s_{read_segments}segments"
            
        except Exception as e:
            logging.debug(f"Enhanced reading failed: {e}")
            return "reading_failed"
    
    async def _enhanced_observation(self, page, parameters: Dict) -> str:
        """Enhanced observation behavior with Browserless support"""
        
        try:
            duration = parameters.get("duration", 3)
            
            # Adjust for Browserless latency
            if self.use_browserless:
                duration *= 1.1
            
            # Simulate looking around the page
            observation_actions = random.randint(1, 3)
            action_duration = duration / observation_actions
            
            for i in range(observation_actions):
                # Random mouse movement (human-like fidgeting)
                if random.random() < 0.5:
                    await page.mouse.move(
                        random.randint(100, 800),
                        random.randint(100, 600)
                    )
                
                await asyncio.sleep(action_duration)
            
            return f"observing_{duration:.1f}s_{observation_actions}actions"
            
        except Exception as e:
            logging.debug(f"Enhanced observation failed: {e}")
            return "observation_failed"
    
    async def _enhanced_link_clicking(self, page, parameters: Dict) -> str:
        """Enhanced link clicking behavior with Browserless support"""
        
        try:
            # Find clickable links with better error handling
            links = await page.locator("a:visible").all()
            
            if links:
                # Select a random link from the first several
                link = random.choice(links[:10])
                
                # Pre-click behavior
                pre_hover_duration = parameters.get("pre_hover_duration", 2)
                if self.use_browserless:
                    pre_hover_duration *= 1.1
                
                await self._human_like_element_approach(page, link)
                await link.hover()
                await asyncio.sleep(pre_hover_duration)
                
                # Click with confidence check (simulate decision making)
                confidence_threshold = parameters.get("confidence_threshold", 0.6)
                if random.random() > confidence_threshold:  # Simulate hesitation
                    await link.click()
                    
                    wait_time = random.uniform(1, 3)
                    if self.use_browserless:
                        wait_time *= 1.2
                    await asyncio.sleep(wait_time)
                    
                    return "clicked_link_success"
                else:
                    return "clicked_link_hesitated"
            
        except Exception as e:
            logging.debug(f"Enhanced link clicking failed: {e}")
        
        return "click_link_failed"
    
    async def _prepare_to_leave_behavior(self, page, parameters: Dict) -> str:
        """Behavior when preparing to leave the page with Browserless support"""
        
        try:
            # Simulate final page scan
            await page.mouse.wheel(0, -200)  # Scroll up a bit
            
            wait_time = random.uniform(1, 3)
            if self.use_browserless:
                wait_time *= 1.1
            await asyncio.sleep(wait_time)
            
            # Look around one more time
            await page.mouse.move(
                random.randint(200, 600),
                random.randint(100, 400)
            )
            
            final_wait = random.uniform(2, 5)
            if self.use_browserless:
                final_wait *= 1.1
            await asyncio.sleep(final_wait)
            
            return "preparing_to_leave"
            
        except Exception as e:
            logging.debug(f"Prepare to leave behavior failed: {e}")
            return "prepare_leave_failed"
    
    async def _human_like_element_approach(self, page, element):
        """Human-like mouse movement to element with Browserless compatibility"""
        
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
                
                # Slightly longer wait for Browserless
                wait_time = random.uniform(0.1, 0.3)
                if self.use_browserless:
                    wait_time *= 1.2
                await asyncio.sleep(wait_time)
                
        except Exception as e:
            logging.debug(f"Human-like element approach failed: {e}")
    
    async def explore_page_content(self, page, duration: int, persona: UserPersona) -> List[str]:
        """Explore page content with persona-specific behavior and Browserless support"""
        
        activities = []
        start_time = time.time()
        
        # Adjust duration for Browserless
        if self.use_browserless:
            duration = int(duration * 1.1)
        
        while time.time() - start_time < duration:
            # Choose exploration activity based on persona
            if persona.reading_pattern == "thorough":
                activities.extend(await self._thorough_exploration(page))
            elif persona.reading_pattern == "skimmer":
                activities.extend(await self._skimming_exploration(page))
            else:
                activities.extend(await self._balanced_exploration(page))
            
            # Break if we've done enough activities
            if len(activities) > 20:
                break
        
        return activities
    
    async def _thorough_exploration(self, page) -> List[str]:
        """Thorough exploration pattern with Browserless support"""
        activities = []
        
        try:
            # Read content thoroughly
            read_time = random.uniform(10, 20)
            if self.use_browserless:
                read_time *= 1.1
            await asyncio.sleep(read_time)
            activities.append("thorough_reading")
            
            # Scroll slowly and pause frequently
            for _ in range(random.randint(2, 4)):
                await page.mouse.wheel(0, random.randint(100, 200))
                
                pause_time = random.uniform(3, 6)
                if self.use_browserless:
                    pause_time *= 1.1
                await asyncio.sleep(pause_time)
                activities.append("slow_scroll_with_reading")
            
            # Hover over multiple elements
            elements = await page.locator("a:visible, h1:visible, h2:visible, h3:visible").all()
            if elements:
                for element in random.sample(elements, min(5, len(elements))):
                    try:
                        await element.hover()
                        hover_time = random.uniform(2, 4)
                        if self.use_browserless:
                            hover_time *= 1.1
                        await asyncio.sleep(hover_time)
                        activities.append("thorough_element_hover")
                    except Exception as e:
                        logging.debug(f"Thorough hover failed: {e}")
                        continue
        
        except Exception as e:
            logging.debug(f"Thorough exploration failed: {e}")
        
        return activities
    
    async def _skimming_exploration(self, page) -> List[str]:
        """Skimming exploration pattern with Browserless support"""
        activities = []
        
        try:
            # Quick scroll through content
            for _ in range(random.randint(4, 8)):
                await page.mouse.wheel(0, random.randint(300, 600))
                
                scroll_pause = random.uniform(0.5, 1.5)
                if self.use_browserless:
                    scroll_pause *= 1.1
                await asyncio.sleep(scroll_pause)
                activities.append("quick_scroll")
            
            # Brief pauses on interesting elements
            brief_read = random.uniform(2, 5)
            if self.use_browserless:
                brief_read *= 1.1
            await asyncio.sleep(brief_read)
            activities.append("brief_reading")
            
            # Quick hover over a few elements
            elements = await page.locator("a:visible").all()
            if elements:
                for element in random.sample(elements, min(3, len(elements))):
                    try:
                        await element.hover()
                        quick_hover = random.uniform(0.5, 1.5)
                        if self.use_browserless:
                            quick_hover *= 1.1
                        await asyncio.sleep(quick_hover)
                        activities.append("quick_hover")
                    except Exception as e:
                        logging.debug(f"Quick hover failed: {e}")
                        continue
        
        except Exception as e:
            logging.debug(f"Skimming exploration failed: {e}")
        
        return activities
    
    async def _balanced_exploration(self, page) -> List[str]:
        """Balanced exploration pattern with Browserless support"""
        activities = []
        
        try:
            # Mix of reading and scrolling
            read_time = random.uniform(5, 10)
            if self.use_browserless:
                read_time *= 1.1
            await asyncio.sleep(read_time)
            activities.append("moderate_reading")
            
            # Medium-paced scrolling
            for _ in range(random.randint(3, 6)):
                await page.mouse.wheel(0, random.randint(200, 400))
                
                scroll_pause = random.uniform(1.5, 3)
                if self.use_browserless:
                    scroll_pause *= 1.1
                await asyncio.sleep(scroll_pause)
                activities.append("moderate_scroll")
            
            # Moderate hovering
            elements = await page.locator("a:visible, button:visible").all()
            if elements:
                for element in random.sample(elements, min(4, len(elements))):
                    try:
                        await element.hover()
                        hover_time = random.uniform(1, 3)
                        if self.use_browserless:
                            hover_time *= 1.1
                        await asyncio.sleep(hover_time)
                        activities.append("moderate_hover")
                    except Exception as e:
                        logging.debug(f"Moderate hover failed: {e}")
                        continue
        
        except Exception as e:
            logging.debug(f"Balanced exploration failed: {e}")
        
        return activities
    
    async def interact_with_forms(self, page, persona: UserPersona) -> List[str]:
        """Interact with forms based on persona with Browserless support"""
        activities = []
        
        try:
            # Find forms on the page
            forms = await page.locator("form:visible").all()
            
            if forms and persona.form_completion_rate > random.random():
                form = random.choice(forms)
                
                # Find input fields
                inputs = await form.locator("input:visible, textarea:visible").all()
                
                for input_field in inputs[:3]:  # Limit to first 3 inputs
                    try:
                        input_type = await input_field.get_attribute("type") or "text"
                        
                        if input_type in ["text", "email", "search"]:
                            await input_field.click()
                            
                            click_pause = random.uniform(0.5, 1.5)
                            if self.use_browserless:
                                click_pause *= 1.1
                            await asyncio.sleep(click_pause)
                            
                            # Type some sample text based on field type
                            if input_type == "email":
                                sample_text = "test@example.com"
                            elif input_type == "search":
                                sample_text = "sample search"
                            else:
                                sample_text = "sample text"
                            
                            # Human-like typing with Browserless consideration
                            base_delay = 0.1 if not self.use_browserless else 0.12
                            for char in sample_text:
                                await page.keyboard.type(char)
                                char_delay = base_delay * random.uniform(0.8, 1.2)
                                await asyncio.sleep(char_delay)
                            
                            activities.append(f"filled_{input_type}_field")
                            
                            # Clear the field (don't submit)
                            await page.keyboard.press("Control+A")
                            await page.keyboard.press("Delete")
                            
                    except Exception as e:
                        logging.debug(f"Form interaction failed: {e}")
                        continue
        
        except Exception as e:
            logging.debug(f"Form interaction failed: {e}")
        
        return activities
    
    async def check_page_performance(self, page) -> Dict[str, Any]:
        """Check page performance metrics with Browserless awareness"""
        
        try:
            # Basic page metrics
            metrics = {
                "url": page.url,
                "title": await page.title(),
                "load_time": time.time(),  # Simplified
                "browser_backend": "browserless" if self.use_browserless else "chromium",
                "elements": {}
            }
            
            # Count elements with error handling for Browserless
            try:
                metrics["elements"]["links"] = await page.locator("a").count()
            except:
                metrics["elements"]["links"] = 0
                
            try:
                metrics["elements"]["images"] = await page.locator("img").count()
            except:
                metrics["elements"]["images"] = 0
                
            try:
                metrics["elements"]["buttons"] = await page.locator("button").count()
            except:
                metrics["elements"]["buttons"] = 0
                
            try:
                metrics["elements"]["forms"] = await page.locator("form").count()
            except:
                metrics["elements"]["forms"] = 0
            
            return metrics
            
        except Exception as e:
            logging.debug(f"Performance check failed: {e}")
            return {
                "error": str(e),
                "browser_backend": "browserless" if self.use_browserless else "chromium"
            }
    
    async def enhanced_page_interaction(self, page, interaction_type: str = "general") -> List[str]:
        """Enhanced page interactions with Browserless optimization"""
        activities = []
        
        try:
            if interaction_type == "ecommerce":
                activities.extend(await self._ecommerce_interactions(page))
            elif interaction_type == "content":
                activities.extend(await self._content_interactions(page))
            elif interaction_type == "social":
                activities.extend(await self._social_interactions(page))
            else:
                activities.extend(await self._general_interactions(page))
                
        except Exception as e:
            logging.debug(f"Enhanced page interaction failed: {e}")
            activities.append("interaction_failed")
        
        return activities
    
    async def _ecommerce_interactions(self, page) -> List[str]:
        """E-commerce specific interactions with Browserless support"""
        activities = []
        
        try:
            # Look for product elements
            product_selectors = [".product:visible", ".item:visible", "[data-product]:visible"]
            
            for selector in product_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if elements:
                        element = random.choice(elements[:5])
                        await element.hover()
                        
                        hover_time = random.uniform(2, 4)
                        if self.use_browserless:
                            hover_time *= 1.1
                        await asyncio.sleep(hover_time)
                        activities.append("product_hover")
                        break
                except:
                    continue
            
            # Look for price elements
            price_selectors = [".price:visible", ".cost:visible", "[class*='price']:visible"]
            for selector in price_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if elements:
                        element = random.choice(elements[:3])
                        await element.hover()
                        
                        price_hover = random.uniform(1, 3)
                        if self.use_browserless:
                            price_hover *= 1.1
                        await asyncio.sleep(price_hover)
                        activities.append("price_check")
                        break
                except:
                    continue
                    
        except Exception as e:
            logging.debug(f"E-commerce interactions failed: {e}")
        
        return activities
    
    async def _content_interactions(self, page) -> List[str]:
        """Content-focused interactions with Browserless support"""
        activities = []
        
        try:
            # Interact with headings
            headings = await page.locator("h1:visible, h2:visible, h3:visible").all()
            if headings:
                heading = random.choice(headings[:5])
                await heading.hover()
                
                heading_time = random.uniform(1.5, 3)
                if self.use_browserless:
                    heading_time *= 1.1
                await asyncio.sleep(heading_time)
                activities.append("heading_focus")
            
            # Look for article content
            content_selectors = ["article:visible", ".content:visible", ".post:visible"]
            for selector in content_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if elements:
                        element = elements[0]
                        box = await element.bounding_box()
                        if box:
                            # Scroll to content
                            await page.mouse.wheel(0, int(box['y'] - 200))
                            
                            content_time = random.uniform(3, 8)
                            if self.use_browserless:
                                content_time *= 1.1
                            await asyncio.sleep(content_time)
                            activities.append("content_reading")
                        break
                except:
                    continue
                    
        except Exception as e:
            logging.debug(f"Content interactions failed: {e}")
        
        return activities
    
    async def _social_interactions(self, page) -> List[str]:
        """Social media interactions with Browserless support"""
        activities = []
        
        try:
            # Look for social elements
            social_selectors = [".post:visible", ".tweet:visible", ".status:visible"]
            
            for selector in social_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if elements:
                        for element in random.sample(elements, min(3, len(elements))):
                            await element.hover()
                            
                            social_time = random.uniform(1, 2)
                            if self.use_browserless:
                                social_time *= 1.1
                            await asyncio.sleep(social_time)
                            activities.append("social_hover")
                        break
                except:
                    continue
                    
        except Exception as e:
            logging.debug(f"Social interactions failed: {e}")
        
        return activities
    
    async def _general_interactions(self, page) -> List[str]:
        """General page interactions with Browserless support"""
        activities = []
        
        try:
            # Random scrolling
            for _ in range(random.randint(2, 4)):
                scroll_amount = random.randint(200, 500)
                await page.mouse.wheel(0, scroll_amount)
                
                scroll_pause = random.uniform(1, 3)
                if self.use_browserless:
                    scroll_pause *= 1.1
                await asyncio.sleep(scroll_pause)
                activities.append("general_scroll")
            
            # Random element interactions
            interactive_elements = await page.locator("a:visible, button:visible").all()
            if interactive_elements:
                element = random.choice(interactive_elements[:10])
                await element.hover()
                
                interaction_time = random.uniform(1, 2)
                if self.use_browserless:
                    interaction_time *= 1.1
                await asyncio.sleep(interaction_time)
                activities.append("general_interaction")
                
        except Exception as e:
            logging.debug(f"General interactions failed: {e}")
        
        return activities