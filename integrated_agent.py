#!/usr/bin/env python3
"""
ENHANCED SITE ACTIVITY SIMULATOR
Improved target site interaction with more realistic browsing behaviors
"""

import asyncio
import random
import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

class EnhancedSiteActivitySimulator:
    """Enhanced site activity simulator with more realistic browsing patterns"""
    
    def __init__(self, persona, autowebglm=None, usimagent=None):
        self.persona = persona
        self.autowebglm = autowebglm
        self.usimagent = usimagent
        self.activity_log = []
        self.interaction_count = 0
        
    async def execute_site_exploration(self, page, session_data: Dict) -> bool:
        """Execute comprehensive site exploration with enhanced activities"""
        
        logging.info("🌐 Starting enhanced site exploration")
        
        try:
            # Wait for page to fully load
            await page.wait_for_load_state('networkidle', timeout=20000)
            await asyncio.sleep(random.uniform(2, 4))
            
            current_url = page.url
            logging.info(f"📍 Currently on: {current_url}")
            
            # Analyze page structure
            page_context = await self._analyze_page_structure(page)
            
            # Generate comprehensive activity plan
            activity_plan = await self._generate_activity_plan(page_context)
            
            # Calculate realistic session duration
            session_duration = self._calculate_enhanced_session_duration(page_context)
            
            logging.info(f"⏱️ Planned session duration: {session_duration}s")
            logging.info(f"📋 Activity plan: {len(activity_plan)} activities")
            
            # Execute enhanced browsing activities
            activities_performed = await self._execute_enhanced_activities(
                page, session_duration, activity_plan, session_data
            )
            
            # Log session summary
            session_summary = {
                "final_url": page.url,
                "activities_performed": activities_performed,
                "interaction_count": self.interaction_count,
                "session_duration": session_duration,
                "page_analysis": page_context,
                "activity_plan": activity_plan,
                "success": True
            }
            
            session_data["site_exploration"] = session_summary
            
            logging.info(f"✅ Site exploration completed: {len(activities_performed)} activities")
            return True
            
        except Exception as e:
            logging.error(f"❌ Site exploration failed: {e}")
            session_data["site_exploration"] = {"success": False, "error": str(e)}
            return False
    
    async def _analyze_page_structure(self, page) -> Dict[str, Any]:
        """Enhanced page structure analysis"""
        
        try:
            url = page.url
            title = await page.title()
            
            # Count interactive elements
            elements_info = await self._count_page_elements(page)
            
            # Detect page features
            page_features = await self._detect_page_features(page)
            
            # Classify content type
            content_type = self._classify_content_type(url, title, elements_info)
            
            # Calculate page complexity
            complexity_score = self._calculate_page_complexity(elements_info, page_features)
            
            page_context = {
                "url": url,
                "title": title,
                "content_type": content_type,
                "elements": elements_info,
                "features": page_features,
                "complexity_score": complexity_score,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"📊 Page analysis: {content_type}, complexity: {complexity_score:.2f}")
            
            return page_context
            
        except Exception as e:
            logging.debug(f"Page analysis error: {e}")
            return {"content_type": "unknown", "complexity_score": 0.5}
    
    async def _count_page_elements(self, page) -> Dict[str, int]:
        """Count different types of page elements"""
        
        element_counts = {}
        
        element_selectors = {
            "links": "a[href]:visible",
            "buttons": "button:visible, input[type='button']:visible, input[type='submit']:visible",
            "forms": "form:visible",
            "images": "img:visible",
            "videos": "video:visible, iframe[src*='youtube']:visible, iframe[src*='vimeo']:visible",
            "headings": "h1:visible, h2:visible, h3:visible, h4:visible, h5:visible, h6:visible",
            "paragraphs": "p:visible",
            "lists": "ul:visible, ol:visible",
            "inputs": "input:visible, textarea:visible, select:visible",
            "social_links": "a[href*='facebook']:visible, a[href*='twitter']:visible, a[href*='instagram']:visible, a[href*='linkedin']:visible",
            "nav_menus": "nav:visible, .menu:visible, .navigation:visible",
            "cards": ".card:visible, .product:visible, .item:visible",
            "modals": ".modal:visible, .popup:visible, .dialog:visible"
        }
        
        for element_type, selector in element_selectors.items():
            try:
                count = await page.locator(selector).count()
                element_counts[element_type] = count
            except:
                element_counts[element_type] = 0
        
        # Calculate totals
        element_counts["total_interactive"] = (
            element_counts["links"] + element_counts["buttons"] + 
            element_counts["inputs"] + element_counts["forms"]
        )
        
        element_counts["total_content"] = (
            element_counts["headings"] + element_counts["paragraphs"] + 
            element_counts["images"] + element_counts["videos"]
        )
        
        return element_counts
    
    async def _detect_page_features(self, page) -> Dict[str, bool]:
        """Detect specific page features"""
        
        features = {}
        
        # Check for common page features
        feature_checks = {
            "has_search": "input[type='search']:visible, input[placeholder*='search' i]:visible, .search:visible",
            "has_navigation": "nav:visible, .navbar:visible, .menu:visible",
            "has_footer": "footer:visible, .footer:visible",
            "has_sidebar": ".sidebar:visible, .aside:visible, aside:visible",
            "has_carousel": ".carousel:visible, .slider:visible, .swiper:visible",
            "has_tabs": ".tabs:visible, .tab-content:visible, [role='tablist']:visible",
            "has_accordion": ".accordion:visible, .collapsible:visible",
            "has_dropdown": ".dropdown:visible, select:visible",
            "has_pagination": ".pagination:visible, .page-numbers:visible",
            "has_filters": ".filter:visible, .sort:visible",
            "has_shopping_cart": ".cart:visible, [href*='cart']:visible, [href*='basket']:visible",
            "has_contact_form": "form[class*='contact']:visible, form[id*='contact']:visible",
            "has_newsletter": "input[type='email']:visible, .newsletter:visible",
            "has_social_media": "a[href*='facebook']:visible, a[href*='twitter']:visible",
            "has_breadcrumbs": ".breadcrumb:visible, .breadcrumbs:visible",
            "has_reviews": ".review:visible, .rating:visible, .stars:visible"
        }
        
        for feature_name, selector in feature_checks.items():
            try:
                count = await page.locator(selector).count()
                features[feature_name] = count > 0
            except:
                features[feature_name] = False
        
        return features
    
    def _classify_content_type(self, url: str, title: str, elements: Dict) -> str:
        """Classify the type of content/website"""
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        # E-commerce indicators
        if (any(keyword in url_lower for keyword in ["shop", "store", "buy", "cart", "product", "ecommerce"]) or
            any(keyword in title_lower for keyword in ["shop", "store", "buy", "product"]) or
            elements.get("has_shopping_cart", False)):
            return "ecommerce"
        
        # Blog/News indicators
        if (any(keyword in url_lower for keyword in ["blog", "news", "article", "post"]) or
            any(keyword in title_lower for keyword in ["blog", "news", "article"]) or
            elements.get("paragraphs", 0) > 10):
            return "blog_news"
        
        # Business/Service indicators
        if (any(keyword in url_lower for keyword in ["service", "business", "company", "about"]) or
            elements.get("has_contact_form", False)):
            return "business_service"
        
        # Portfolio/Gallery indicators
        if (elements.get("images", 0) > 15 or
            any(keyword in url_lower for keyword in ["portfolio", "gallery", "photos"])):
            return "portfolio_gallery"
        
        # Directory/Listing indicators
        if (elements.get("cards", 0) > 5 or
            elements.get("has_filters", False) or
            any(keyword in url_lower for keyword in ["directory", "list", "find"])):
            return "directory_listing"
        
        # Educational/Documentation
        if (any(keyword in url_lower for keyword in ["edu", "doc", "guide", "tutorial", "learn"]) or
            any(keyword in title_lower for keyword in ["documentation", "guide", "tutorial"])):
            return "educational"
        
        # Homepage indicators
        if (url_lower.count('/') <= 3 and 
            elements.get("has_navigation", False) and 
            elements.get("total_content", 0) > 5):
            return "homepage"
        
        return "general"
    
    def _calculate_page_complexity(self, elements: Dict, features: Dict) -> float:
        """Calculate page complexity score (0-1)"""
        
        complexity = 0.0
        
        # Interactive elements contribute to complexity
        interactive_score = min(1.0, elements.get("total_interactive", 0) / 20)
        complexity += interactive_score * 0.4
        
        # Content volume
        content_score = min(1.0, elements.get("total_content", 0) / 30)
        complexity += content_score * 0.2
        
        # Advanced features
        advanced_features = ["has_carousel", "has_tabs", "has_accordion", "has_filters", "has_pagination"]
        feature_score = sum(features.get(f, False) for f in advanced_features) / len(advanced_features)
        complexity += feature_score * 0.3
        
        # Form complexity
        form_score = min(1.0, elements.get("inputs", 0) / 10)
        complexity += form_score * 0.1
        
        return min(1.0, complexity)
    
    async def _generate_activity_plan(self, page_context: Dict) -> List[Dict[str, Any]]:
        """Generate comprehensive activity plan based on page analysis"""
        
        content_type = page_context.get("content_type", "general")
        elements = page_context.get("elements", {})
        features = page_context.get("features", {})
        complexity = page_context.get("complexity_score", 0.5)
        
        activities = []
        
        # Always start with page orientation
        activities.append({
            "type": "page_orientation",
            "priority": 1.0,
            "duration_range": (3, 8),
            "description": "Initial page scan and orientation"
        })
        
        # Content-specific activities
        if content_type == "ecommerce":
            activities.extend([
                {"type": "browse_products", "priority": 0.9, "duration_range": (15, 45)},
                {"type": "view_product_details", "priority": 0.8, "duration_range": (20, 60)},
                {"type": "use_filters", "priority": 0.6, "duration_range": (10, 25)},
                {"type": "check_prices", "priority": 0.7, "duration_range": (5, 15)}
            ])
            
            if features.get("has_shopping_cart", False):
                activities.append({"type": "explore_cart", "priority": 0.5, "duration_range": (5, 15)})
        
        elif content_type == "blog_news":
            activities.extend([
                {"type": "read_articles", "priority": 0.9, "duration_range": (30, 120)},
                {"type": "scroll_content", "priority": 0.8, "duration_range": (20, 60)},
                {"type": "explore_categories", "priority": 0.6, "duration_range": (10, 30)},
                {"type": "check_related_content", "priority": 0.7, "duration_range": (15, 45)}
            ])
        
        elif content_type == "business_service":
            activities.extend([
                {"type": "explore_services", "priority": 0.8, "duration_range": (20, 60)},
                {"type": "read_about_info", "priority": 0.7, "duration_range": (15, 45)},
                {"type": "check_contact_info", "priority": 0.6, "duration_range": (10, 30)}
            ])
            
            if features.get("has_contact_form", False):
                activities.append({"type": "examine_contact_form", "priority": 0.5, "duration_range": (10, 25)})
        
        # Feature-based activities
        if features.get("has_navigation", False):
            activities.append({"type": "explore_navigation", "priority": 0.7, "duration_range": (10, 30)})
        
        if features.get("has_search", False):
            activities.append({"type": "try_search", "priority": 0.6, "duration_range": (10, 25)})
        
        if features.get("has_carousel", False):
            activities.append({"type": "interact_carousel", "priority": 0.5, "duration_range": (10, 30)})
        
        if features.get("has_tabs", False):
            activities.append({"type": "explore_tabs", "priority": 0.6, "duration_range": (15, 35)})
        
        if features.get("has_social_media", False):
            activities.append({"type": "check_social_links", "priority": 0.3, "duration_range": (5, 15)})
        
        if elements.get("images", 0) > 5:
            activities.append({"type": "view_images", "priority": 0.6, "duration_range": (15, 45)})
        
        if elements.get("videos", 0) > 0:
            activities.append({"type": "explore_videos", "priority": 0.7, "duration_range": (20, 60)})
        
        # General browsing activities
        activities.extend([
            {"type": "scroll_exploration", "priority": 0.8, "duration_range": (10, 30)},
            {"type": "hover_elements", "priority": 0.6, "duration_range": (5, 20)},
            {"type": "random_clicks", "priority": 0.4, "duration_range": (5, 15)},
            {"type": "reading_pauses", "priority": 0.7, "duration_range": (10, 45)}
        ])
        
        # Adjust priorities based on persona
        activities = self._adjust_activities_for_persona(activities)
        
        # Sort by priority and limit
        activities.sort(key=lambda x: x["priority"], reverse=True)
        
        # Select activities based on complexity and persona
        max_activities = max(5, min(12, int(complexity * 15)))
        selected_activities = activities[:max_activities]
        
        logging.info(f"📋 Generated {len(selected_activities)} activities for {content_type} page")
        
        return selected_activities
    
    def _adjust_activities_for_persona(self, activities: List[Dict]) -> List[Dict]:
        """Adjust activity priorities based on persona characteristics"""
        
        if not self.persona:
            return activities
        
        for activity in activities:
            # Adjust based on browsing speed
            if self.persona.browsing_speed == "fast":
                if activity["type"] in ["reading_pauses", "read_articles"]:
                    activity["priority"] *= 0.7
                    activity["duration_range"] = (
                        int(activity["duration_range"][0] * 0.7),
                        int(activity["duration_range"][1] * 0.7)
                    )
                elif activity["type"] in ["scroll_exploration", "random_clicks"]:
                    activity["priority"] *= 1.3
            
            elif self.persona.browsing_speed == "slow":
                if activity["type"] in ["reading_pauses", "read_articles"]:
                    activity["priority"] *= 1.2
                    activity["duration_range"] = (
                        int(activity["duration_range"][0] * 1.3),
                        int(activity["duration_range"][1] * 1.3)
                    )
            
            # Adjust based on tech comfort
            if self.persona.tech_comfort == "high":
                if activity["type"] in ["try_search", "use_filters", "explore_tabs"]:
                    activity["priority"] *= 1.2
            elif self.persona.tech_comfort == "low":
                if activity["type"] in ["random_clicks", "interact_carousel"]:
                    activity["priority"] *= 0.8
            
            # Adjust based on attention span
            if self.persona.attention_span == "short":
                activity["duration_range"] = (
                    max(3, int(activity["duration_range"][0] * 0.8)),
                    max(10, int(activity["duration_range"][1] * 0.8))
                )
            elif self.persona.attention_span == "long":
                activity["duration_range"] = (
                    int(activity["duration_range"][0] * 1.2),
                    int(activity["duration_range"][1] * 1.2)
                )
        
        return activities
    
    def _calculate_enhanced_session_duration(self, page_context: Dict) -> int:
        """Calculate realistic session duration"""
        
        if not self.persona:
            return random.randint(60, 300)
        
        # Base duration from persona
        min_duration, max_duration = self.persona.session_duration_range
        base_duration = random.randint(min_duration, max_duration)
        
        # Adjust based on page characteristics
        complexity = page_context.get("complexity_score", 0.5)
        content_type = page_context.get("content_type", "general")
        
        multiplier = 1.0
        
        # Content type adjustments
        content_multipliers = {
            "ecommerce": 1.2,
            "blog_news": 1.4,
            "educational": 1.5,
            "portfolio_gallery": 1.1,
            "business_service": 1.0,
            "directory_listing": 0.9,
            "homepage": 0.8,
            "general": 1.0
        }
        
        multiplier *= content_multipliers.get(content_type, 1.0)
        
        # Complexity adjustment
        multiplier *= (0.7 + complexity * 0.6)  # 0.7 to 1.3 range
        
        # Persona-specific adjustments
        if self.persona.reading_pattern == "thorough":
            multiplier *= 1.3
        elif self.persona.reading_pattern == "skimmer":
            multiplier *= 0.8
        
        if self.persona.attention_span == "long":
            multiplier *= 1.2
        elif self.persona.attention_span == "short":
            multiplier *= 0.7
        
        # Apply cognitive state if available
        if self.usimagent:
            if hasattr(self.usimagent, 'interest_level'):
                multiplier *= (0.6 + self.usimagent.interest_level * 0.8)
            if hasattr(self.usimagent, 'fatigue_level'):
                multiplier *= (1.2 - self.usimagent.fatigue_level * 0.4)
        
        final_duration = int(base_duration * multiplier)
        
        # Ensure reasonable bounds
        final_duration = max(30, min(600, final_duration))
        
        return final_duration
    
    async def _execute_enhanced_activities(self, page, total_duration: int, 
                                         activity_plan: List[Dict], 
                                         session_data: Dict) -> List[str]:
        """Execute the planned activities with realistic timing"""
        
        start_time = time.time()
        end_time = start_time + total_duration
        activities_performed = []
        
        logging.info(f"🚀 Starting {total_duration}s of enhanced site activities")
        
        # Shuffle activity order for realism
        activity_plan = activity_plan.copy()
        random.shuffle(activity_plan)
        
        activity_index = 0
        
        while time.time() < end_time and activity_index < len(activity_plan):
            remaining_time = end_time - time.time()
            
            if remaining_time < 5:
                break
            
            # Check if should continue (cognitive state)
            if self.usimagent and hasattr(self.usimagent, 'should_continue_browsing'):
                if not self.usimagent.should_continue_browsing():
                    logging.info("🧠 Cognitive model decided to stop browsing")
                    break
            
            # Select next activity
            activity = activity_plan[activity_index]
            activity_type = activity["type"]
            
            # Calculate activity duration
            min_dur, max_dur = activity["duration_range"]
            activity_duration = min(remaining_time - 2, random.randint(min_dur, max_dur))
            
            if activity_duration < 3:
                break
            
            logging.info(f"🎯 Executing: {activity_type} ({activity_duration}s)")
            
            try:
                # Execute the specific activity
                success = await self._execute_specific_activity(page, activity_type, activity_duration)
                
                if success:
                    activities_performed.append(activity_type)
                    self.activity_log.append({
                        "activity": activity_type,
                        "duration": activity_duration,
                        "timestamp": datetime.now().isoformat(),
                        "success": True
                    })
                else:
                    logging.debug(f"Activity failed: {activity_type}")
                
                # Update cognitive state
                if self.usimagent and hasattr(self.usimagent, '_update_cognitive_state'):
                    mock_action = {
                        "action_type": activity_type,
                        "confidence": 0.8 if success else 0.4
                    }
                    self.usimagent._update_cognitive_state(mock_action)
                
            except Exception as e:
                logging.debug(f"Activity execution error: {activity_type} - {e}")
                activities_performed.append(f"{activity_type}_failed")
            
            activity_index += 1
            
            # Random pause between activities
            if time.time() < end_time - 3:
                pause_duration = random.uniform(1, 3)
                await asyncio.sleep(pause_duration)
        
        actual_duration = time.time() - start_time
        logging.info(f"✅ Site activities completed: {len(activities_performed)} activities in {actual_duration:.1f}s")
        
        # Add activity summary to session data
        session_data.setdefault("activity_details", {}).update({
            "planned_activities": len(activity_plan),
            "performed_activities": len(activities_performed),
            "actual_duration": actual_duration,
            "planned_duration": total_duration,
            "activity_log": self.activity_log
        })
        
        return activities_performed
    
    async def _execute_specific_activity(self, page, activity_type: str, duration: int) -> bool:
        """Execute a specific activity type"""
        
        try:
            if activity_type == "page_orientation":
                return await self._page_orientation_activity(page, duration)
            elif activity_type == "scroll_exploration":
                return await self._scroll_exploration_activity(page, duration)
            elif activity_type == "browse_products":
                return await self._browse_products_activity(page, duration)
            elif activity_type == "view_product_details":
                return await self._view_product_details_activity(page, duration)
            elif activity_type == "read_articles":
                return await self._read_articles_activity(page, duration)
            elif activity_type == "explore_navigation":
                return await self._explore_navigation_activity(page, duration)
            elif activity_type == "try_search":
                return await self._try_search_activity(page, duration)
            elif activity_type == "interact_carousel":
                return await self._interact_carousel_activity(page, duration)
            elif activity_type == "explore_tabs":
                return await self._explore_tabs_activity(page, duration)
            elif activity_type == "hover_elements":
                return await self._hover_elements_activity(page, duration)
            elif activity_type == "view_images":
                return await self._view_images_activity(page, duration)
            elif activity_type == "explore_videos":
                return await self._explore_videos_activity(page, duration)
            elif activity_type == "random_clicks":
                return await self._random_clicks_activity(page, duration)
            elif activity_type == "reading_pauses":
                return await self._reading_pauses_activity(page, duration)
            elif activity_type == "use_filters":
                return await self._use_filters_activity(page, duration)
            elif activity_type == "check_contact_info":
                return await self._check_contact_info_activity(page, duration)
            else:
                # Default activity - scrolling and waiting
                return await self._default_activity(page, duration)
        
        except Exception as e:
            logging.debug(f"Specific activity execution failed: {activity_type} - {e}")
            return False
    
    async def _page_orientation_activity(self, page, duration: int) -> bool:
        """Initial page orientation - scroll to see layout"""
        
        try:
            # Initial pause to "read" the page
            await asyncio.sleep(random.uniform(2, 4))
            
            # Scroll down to see more content
            scroll_amount = random.randint(300, 600)
            await page.mouse.wheel(0, scroll_amount)
            await asyncio.sleep(random.uniform(2, 4))
            
            # Scroll back up to top
            await page.mouse.wheel(0, -scroll_amount)
            await asyncio.sleep(random.uniform(1, 3))
            
            # Small scroll down to settle
            await page.mouse.wheel(0, random.randint(100, 200))
            
            remaining_time = duration - 7
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
            
            return True
            
        except Exception as e:
            logging.debug(f"Page orientation failed: {e}")
            return False
    
    async def _scroll_exploration_activity(self, page, duration: int) -> bool:
        """Realistic scrolling exploration"""
        
        try:
            end_time = time.time() + duration
            
            while time.time() < end_time:
                # Variable scrolling
                if random.random() < 0.7:  # Scroll down
                    scroll_amount = random.randint(200, 500)
                    await page.mouse.wheel(0, scroll_amount)
                else:  # Occasionally scroll up
                    scroll_amount = random.randint(100, 300)
                    await page.mouse.wheel(0, -scroll_amount)
                
                # Pause to "read"
                pause = random.uniform(2, 6)
                await asyncio.sleep(pause)
                
                # Occasionally hover over elements while scrolling
                if random.random() < 0.3:
                    try:
                        visible_elements = await page.locator("h2:visible, h3:visible, a:visible").all()
                        if visible_elements:
                            element = random.choice(visible_elements[:5])
                            await element.hover()
                            await asyncio.sleep(random.uniform(1, 2))
                    except:
                        pass
            
            return True
            
        except Exception as e:
            logging.debug(f"Scroll exploration failed: {e}")
            return False
    
    async def _browse_products_activity(self, page, duration: int) -> bool:
        """Browse products on e-commerce sites"""
        
        try:
            end_time = time.time() + duration
            
            # Look for product elements
            product_selectors = [
                ".product:visible",
                ".item:visible", 
                ".card:visible",
                "[data-product]:visible",
                ".product-item:visible"
            ]
            
            products = []
            for selector in product_selectors:
                try:
                    found_products = await page.locator(selector).all()
                    if found_products:
                        products.extend(found_products[:10])
                        break
                except:
                    continue
            
            if not products:
                # Fallback to general browsing
                return await self._scroll_exploration_activity(page, duration)
            
            # Browse through products
            products_viewed = 0
            while time.time() < end_time and products_viewed < len(products):
                try:
                    product = products[products_viewed]
                    
                    # Scroll to product
                    await product.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Hover over product
                    await product.hover()
                    await asyncio.sleep(random.uniform(2, 5))
                    
                    # Occasionally click for more details
                    if random.random() < 0.3:
                        clickable = product.locator("a:visible, button:visible").first
                        if await clickable.count() > 0:
                            # Store current URL to go back
                            current_url = page.url
                            await clickable.click()
                            await asyncio.sleep(random.uniform(3, 8))
                            
                            # Go back if we navigated away
                            if page.url != current_url:
                                await page.go_back()
                                await asyncio.sleep(random.uniform(2, 4))
                    
                    products_viewed += 1
                    
                except Exception as e:
                    logging.debug(f"Product browsing error: {e}")
                    products_viewed += 1
                    continue
            
            return True
            
        except Exception as e:
            logging.debug(f"Browse products failed: {e}")
            return False
    
    async def _view_product_details_activity(self, page, duration: int) -> bool:
        """View detailed product information"""
        
        try:
            # Look for product detail elements
            detail_selectors = [
                ".product-details:visible",
                ".description:visible",
                ".specs:visible",
                ".features:visible",
                "h1:visible"
            ]
            
            for selector in detail_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if elements:
                        for element in elements[:3]:
                            await element.scroll_into_view_if_needed()
                            await asyncio.sleep(random.uniform(3, 8))
                        break
                except:
                    continue
            
            # Look for images to view
            try:
                images = await page.locator("img:visible").all()
                if images:
                    for img in images[:3]:
                        await img.hover()
                        await asyncio.sleep(random.uniform(2, 4))
            except:
                pass
            
            # Scroll through content
            remaining_time = max(0, duration - 20)
            if remaining_time > 0:
                await self._scroll_exploration_activity(page, remaining_time)
            
            return True
            
        except Exception as e:
            logging.debug(f"View product details failed: {e}")
            return False
    
    async def _read_articles_activity(self, page, duration: int) -> bool:
        """Read article content with realistic behavior"""
        
        try:
            # Find article content
            content_selectors = [
                "article:visible",
                ".content:visible",
                ".post-content:visible",
                "main:visible",
                ".article-body:visible"
            ]
            
            content_found = False
            for selector in content_selectors:
                try:
                    content = page.locator(selector).first
                    if await content.count() > 0:
                        await content.scroll_into_view_if_needed()
                        content_found = True
                        break
                except:
                    continue
            
            if not content_found:
                return await self._scroll_exploration_activity(page, duration)
            
            # Reading behavior - scroll slowly with pauses
            end_time = time.time() + duration
            
            while time.time() < end_time:
                # Small scroll (like reading)
                scroll_amount = random.randint(50, 200)
                await page.mouse.wheel(0, scroll_amount)
                
                # Reading pause
                reading_pause = random.uniform(3, 8)
                await asyncio.sleep(reading_pause)
                
                # Occasionally scroll back up (re-reading)
                if random.random() < 0.15:
                    back_scroll = random.randint(50, 150)
                    await page.mouse.wheel(0, -back_scroll)
                    await asyncio.sleep(random.uniform(2, 4))
            
            return True
            
        except Exception as e:
            logging.debug(f"Read articles failed: {e}")
            return False
    
    async def _explore_navigation_activity(self, page, duration: int) -> bool:
        """Explore site navigation"""
        
        try:
            # Find navigation elements
            nav_selectors = [
                "nav:visible a",
                ".menu:visible a",
                ".navigation:visible a",
                "header:visible a"
            ]
            
            nav_links = []
            for selector in nav_selectors:
                try:
                    links = await page.locator(selector).all()
                    if links:
                        nav_links.extend(links[:8])
                        break
                except:
                    continue
            
            if not nav_links:
                return await self._scroll_exploration_activity(page, duration)
            
            # Explore navigation items
            end_time = time.time() + duration
            links_explored = 0
            
            while time.time() < end_time and links_explored < len(nav_links):
                try:
                    link = nav_links[links_explored]
                    
                    # Hover over navigation item
                    await link.hover()
                    await asyncio.sleep(random.uniform(2, 4))
                    
                    # Occasionally click (but go back quickly)
                    if random.random() < 0.3:
                        href = await link.get_attribute("href")
                        if href and not any(x in href for x in ["#", "javascript:", "mailto:", "tel:"]):
                            current_url = page.url
                            await link.click()
                            await asyncio.sleep(random.uniform(2, 5))
                            
                            # Go back to continue exploring
                            if page.url != current_url:
                                await page.go_back()
                                await asyncio.sleep(random.uniform(1, 3))
                    
                    links_explored += 1
                    
                except Exception as e:
                    logging.debug(f"Navigation exploration error: {e}")
                    links_explored += 1
            
            return True
            
        except Exception as e:
            logging.debug(f"Explore navigation failed: {e}")
            return False
    
    async def _try_search_activity(self, page, duration: int) -> bool:
        """Try using site search functionality"""
        
        try:
            # Find search input
            search_selectors = [
                "input[type='search']:visible",
                "input[placeholder*='search' i]:visible",
                ".search input:visible",
                "#search:visible"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    input_elem = page.locator(selector).first
                    if await input_elem.count() > 0 and await input_elem.is_visible():
                        search_input = input_elem
                        break
                except:
                    continue
            
            if not search_input:
                return await self._scroll_exploration_activity(page, duration)
            
            # Click on search input
            await search_input.click()
            await asyncio.sleep(random.uniform(1, 2))
            
            # Type a search query (relevant to the site)
            search_queries = [
                "help", "info", "about", "contact", "services", 
                "products", "support", "FAQ", "guide"
            ]
            
            query = random.choice(search_queries)
            
            # Type with realistic speed
            for char in query:
                await page.keyboard.type(char)
                await asyncio.sleep(random.uniform(0.1, 0.3))
            
            await asyncio.sleep(random.uniform(2, 4))
            
            # Sometimes press Enter, sometimes just clear
            if random.random() < 0.5:
                await page.keyboard.press("Enter")
                await asyncio.sleep(random.uniform(3, 6))
                
                # Go back if we navigated
                try:
                    await page.go_back()
                    await asyncio.sleep(random.uniform(2, 4))
                except:
                    pass
            else:
                # Clear the search
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Delete")
            
            # Use remaining time for general browsing
            remaining_time = max(0, duration - 15)
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
            
            return True
            
        except Exception as e:
            logging.debug(f"Try search failed: {e}")
            return False
    
    async def _interact_carousel_activity(self, page, duration: int) -> bool:
        """Interact with carousels/sliders"""
        
        try:
            # Find carousel elements
            carousel_selectors = [
                ".carousel:visible",
                ".slider:visible", 
                ".swiper:visible",
                "[data-carousel]:visible"
            ]
            
            carousel = None
            for selector in carousel_selectors:
                try:
                    elem = page.locator(selector).first
                    if await elem.count() > 0:
                        carousel = elem
                        break
                except:
                    continue
            
            if not carousel:
                return await self._scroll_exploration_activity(page, duration)
            
            # Scroll carousel into view
            await carousel.scroll_into_view_if_needed()
            await asyncio.sleep(random.uniform(2, 4))
            
            # Look for navigation buttons
            nav_selectors = [
                ".carousel-next:visible, .next:visible",
                ".carousel-prev:visible, .prev:visible", 
                ".slick-next:visible",
                ".slick-prev:visible"
            ]
            
            end_time = time.time() + duration
            interactions = 0
            
            while time.time() < end_time and interactions < 5:
                try:
                    # Try to find and click next/prev buttons
                    for nav_selector in nav_selectors:
                        try:
                            nav_buttons = await page.locator(nav_selector).all()
                            if nav_buttons:
                                button = random.choice(nav_buttons)
                                if await button.is_visible():
                                    await button.click()
                                    await asyncio.sleep(random.uniform(3, 6))
                                    interactions += 1
                                    break
                        except:
                            continue
                    
                    # If no buttons, try swiping gestures
                    if interactions == 0:
                        # Simulate swipe by clicking and dragging
                        try:
                            bbox = await carousel.bounding_box()
                            if bbox:
                                start_x = bbox["x"] + bbox["width"] * 0.7
                                end_x = bbox["x"] + bbox["width"] * 0.3
                                y = bbox["y"] + bbox["height"] * 0.5
                                
                                await page.mouse.move(start_x, y)
                                await page.mouse.down()
                                await page.mouse.move(end_x, y)
                                await page.mouse.up()
                                
                                await asyncio.sleep(random.uniform(2, 4))
                                interactions += 1
                        except:
                            pass
                    
                    if interactions == 0:
                        break
                        
                except Exception as e:
                    logging.debug(f"Carousel interaction error: {e}")
                    break
            
            return interactions > 0
            
        except Exception as e:
            logging.debug(f"Interact carousel failed: {e}")
            return False
    
    async def _explore_tabs_activity(self, page, duration: int) -> bool:
        """Explore tab interfaces"""
        
        try:
            # Find tab elements
            tab_selectors = [
                ".tab:visible, [role='tab']:visible",
                ".nav-tab:visible",
                ".ui-tab:visible"
            ]
            
            tabs = []
            for selector in tab_selectors:
                try:
                    found_tabs = await page.locator(selector).all()
                    if found_tabs:
                        tabs = found_tabs[:6]  # Limit to 6 tabs
                        break
                except:
                    continue
            
            if not tabs:
                return await self._scroll_exploration_activity(page, duration)
            
            # Click through tabs
            end_time = time.time() + duration
            tab_index = 0
            
            while time.time() < end_time and tab_index < len(tabs):
                try:
                    tab = tabs[tab_index]
                    
                    # Click the tab
                    await tab.click()
                    await asyncio.sleep(random.uniform(3, 8))
                    
                    # Scroll to see tab content
                    try:
                        await page.mouse.wheel(0, random.randint(100, 300))
                        await asyncio.sleep(random.uniform(2, 5))
                    except:
                        pass
                    
                    tab_index += 1
                    
                except Exception as e:
                    logging.debug(f"Tab click error: {e}")
                    tab_index += 1
            
            return True
            
        except Exception as e:
            logging.debug(f"Explore tabs failed: {e}")
            return False
    
    async def _hover_elements_activity(self, page, duration: int) -> bool:
        """Hover over various page elements"""
        
        try:
            # Find hoverable elements
            hover_selectors = [
                "a:visible",
                "button:visible",
                ".card:visible",
                ".item:visible",
                "img:visible"
            ]
            
            hoverable_elements = []
            for selector in hover_selectors:
                try:
                    elements = await page.locator(selector).all()
                    hoverable_elements.extend(elements[:15])
                except:
                    continue
            
            if not hoverable_elements:
                return await self._scroll_exploration_activity(page, duration)
            
            # Random hover behavior
            end_time = time.time() + duration
            hovers_performed = 0
            
            while time.time() < end_time and hovers_performed < 10:
                try:
                    element = random.choice(hoverable_elements)
                    
                    if await element.is_visible():
                        await element.hover()
                        hover_duration = random.uniform(1, 4)
                        await asyncio.sleep(hover_duration)
                        hovers_performed += 1
                    
                except Exception as e:
                    logging.debug(f"Hover error: {e}")
                
                # Small pause between hovers
                await asyncio.sleep(random.uniform(0.5, 2))
            
            return True
            
        except Exception as e:
            logging.debug(f"Hover elements failed: {e}")
            return False
    
    async def _view_images_activity(self, page, duration: int) -> bool:
        """View and interact with images"""
        
        try:
            # Find images
            images = await page.locator("img:visible").all()
            
            if not images:
                return await self._scroll_exploration_activity(page, duration)
            
            # Limit to reasonable number
            images = images[:10]
            
            end_time = time.time() + duration
            images_viewed = 0
            
            while time.time() < end_time and images_viewed < len(images):
                try:
                    img = images[images_viewed]
                    
                    # Scroll to image
                    await img.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Hover over image
                    await img.hover()
                    view_duration = random.uniform(2, 6)
                    await asyncio.sleep(view_duration)
                    
                    # Occasionally click (for lightbox, etc.)
                    if random.random() < 0.2:
                        try:
                            await img.click()
                            await asyncio.sleep(random.uniform(2, 5))
                            
                            # Try to close if modal opened
                            close_selectors = [
                                ".close:visible",
                                ".modal-close:visible",
                                "[aria-label='close']:visible"
                            ]
                            
                            for close_selector in close_selectors:
                                try:
                                    close_btn = page.locator(close_selector).first
                                    if await close_btn.count() > 0:
                                        await close_btn.click()
                                        await asyncio.sleep(1)
                                        break
                                except:
                                    continue
                            
                            # If modal still open, press Escape
                            try:
                                await page.keyboard.press("Escape")
                                await asyncio.sleep(1)
                            except:
                                pass
                                
                        except:
                            pass
                    
                    images_viewed += 1
                    
                except Exception as e:
                    logging.debug(f"Image viewing error: {e}")
                    images_viewed += 1
            
            return True
            
        except Exception as e:
            logging.debug(f"View images failed: {e}")
            return False
    
    async def _explore_videos_activity(self, page, duration: int) -> bool:
        """Explore video content"""
        
        try:
            # Find video elements
            video_selectors = [
                "video:visible",
                "iframe[src*='youtube']:visible",
                "iframe[src*='vimeo']:visible",
                ".video:visible"
            ]
            
            videos = []
            for selector in video_selectors:
                try:
                    found_videos = await page.locator(selector).all()
                    if found_videos:
                        videos.extend(found_videos[:3])
                        break
                except:
                    continue
            
            if not videos:
                return await self._scroll_exploration_activity(page, duration)
            
            # Interact with videos
            for video in videos:
                try:
                    # Scroll to video
                    await video.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(2, 4))
                    
                    # Hover over video
                    await video.hover()
                    await asyncio.sleep(random.uniform(3, 8))
                    
                    # Don't actually play videos (too disruptive)
                    # Just observe them
                    
                except Exception as e:
                    logging.debug(f"Video exploration error: {e}")
                    continue
            
            # Use remaining time for general activity
            remaining_time = max(0, duration - 20)
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
            
            return True
            
        except Exception as e:
            logging.debug(f"Explore videos failed: {e}")
            return False
    
    async def _random_clicks_activity(self, page, duration: int) -> bool:
        """Perform safe random clicks"""
        
        try:
            # Find safe clickable elements (avoid forms, external links)
            safe_selectors = [
                "a[href^='#']:visible",  # Internal anchors
                "button[type='button']:visible",  # Generic buttons
                ".toggle:visible",
                ".expand:visible",
                ".show-more:visible",
                ".accordion:visible h3",
                ".tab:visible"
            ]
            
            clickable_elements = []
            for selector in safe_selectors:
                try:
                    elements = await page.locator(selector).all()
                    clickable_elements.extend(elements[:8])
                except:
                    continue
            
            if not clickable_elements:
                return await self._hover_elements_activity(page, duration)
            
            end_time = time.time() + duration
            clicks_performed = 0
            
            while time.time() < end_time and clicks_performed < 5:
                try:
                    element = random.choice(clickable_elements)
                    
                    if await element.is_visible():
                        current_url = page.url
                        
                        await element.click()
                        await asyncio.sleep(random.uniform(2, 5))
                        
                        # If we navigated away, go back
                        if page.url != current_url:
                            await page.go_back()
                            await asyncio.sleep(random.uniform(2, 4))
                        
                        clicks_performed += 1
                    
                except Exception as e:
                    logging.debug(f"Random click error: {e}")
                
                # Pause between clicks
                await asyncio.sleep(random.uniform(3, 6))
            
            return True
            
        except Exception as e:
            logging.debug(f"Random clicks failed: {e}")
            return False
    
    async def _reading_pauses_activity(self, page, duration: int) -> bool:
        """Simulate reading with natural pauses"""
        
        try:
            # Find text content to "read"
            text_selectors = [
                "p:visible",
                "article:visible",
                ".content:visible p",
                "main:visible p",
                "h2:visible, h3:visible"
            ]
            
            text_elements = []
            for selector in text_selectors:
                try:
                    elements = await page.locator(selector).all()
                    text_elements.extend(elements[:10])
                except:
                    continue
            
            if not text_elements:
                return await self._scroll_exploration_activity(page, duration)
            
            # Reading behavior with pauses
            end_time = time.time() + duration
            elements_read = 0
            
            while time.time() < end_time and elements_read < len(text_elements):
                try:
                    element = text_elements[elements_read]
                    
                    # Scroll to text
                    await element.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # "Read" the text (pause based on estimated length)
                    try:
                        text_content = await element.inner_text()
                        # Rough reading time calculation (200 words per minute)
                        word_count = len(text_content.split())
                        reading_time = max(2, min(15, word_count * 0.3))
                        
                        await asyncio.sleep(reading_time)
                        
                    except:
                        # Fallback pause
                        await asyncio.sleep(random.uniform(3, 8))
                    
                    elements_read += 1
                    
                except Exception as e:
                    logging.debug(f"Reading pause error: {e}")
                    elements_read += 1
            
            return True
            
        except Exception as e:
            logging.debug(f"Reading pauses failed: {e}")
            return False
    
    async def _use_filters_activity(self, page, duration: int) -> bool:
        """Interact with filter/sort options"""
        
        try:
            # Find filter elements
            filter_selectors = [
                ".filter:visible select",
                ".sort:visible select", 
                ".filter:visible input[type='checkbox']",
                "[data-filter]:visible",
                ".dropdown:visible"
            ]
            
            filter_elements = []
            for selector in filter_selectors:
                try:
                    elements = await page.locator(selector).all()
                    filter_elements.extend(elements[:5])
                except:
                    continue
            
            if not filter_elements:
                return await self._scroll_exploration_activity(page, duration)
            
            # Interact with filters
            end_time = time.time() + duration
            interactions = 0
            
            while time.time() < end_time and interactions < 3:
                try:
                    filter_elem = random.choice(filter_elements)
                    
                    if await filter_elem.is_visible():
                        tag_name = await filter_elem.evaluate("el => el.tagName.toLowerCase()")
                        
                        if tag_name == "select":
                            # Handle dropdown
                            options = await filter_elem.locator("option").all()
                            if len(options) > 1:
                                option = random.choice(options[1:])  # Skip first option
                                await option.click()
                                await asyncio.sleep(random.uniform(3, 6))
                        
                        elif tag_name == "input":
                            # Handle checkbox
                            await filter_elem.check()
                            await asyncio.sleep(random.uniform(2, 4))
                            
                            # Sometimes uncheck
                            if random.random() < 0.5:
                                await filter_elem.uncheck()
                                await asyncio.sleep(random.uniform(1, 3))
                        
                        else:
                            # Generic click
                            await filter_elem.click()
                            await asyncio.sleep(random.uniform(2, 5))
                        
                        interactions += 1
                    
                except Exception as e:
                    logging.debug(f"Filter interaction error: {e}")
                
                # Pause between filter interactions
                await asyncio.sleep(random.uniform(2, 4))
            
            return interactions > 0
            
        except Exception as e:
            logging.debug(f"Use filters failed: {e}")
            return False
    
    async def _check_contact_info_activity(self, page, duration: int) -> bool:
        """Look for and examine contact information"""
        
        try:
            # Find contact-related elements
            contact_selectors = [
                "a[href*='contact']:visible",
                "a[href^='tel:']:visible",
                "a[href^='mailto:']:visible",
                ".contact:visible",
                ".phone:visible",
                ".email:visible",
                "footer:visible"
            ]
            
            contact_elements = []
            for selector in contact_selectors:
                try:
                    elements = await page.locator(selector).all()
                    contact_elements.extend(elements[:5])
                except:
                    continue
            
            if not contact_elements:
                return await self._scroll_exploration_activity(page, duration)
            
            # Examine contact elements
            end_time = time.time() + duration
            elements_checked = 0
            
            while time.time() < end_time and elements_checked < len(contact_elements):
                try:
                    element = contact_elements[elements_checked]
                    
                    # Scroll to element
                    await element.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Hover to examine
                    await element.hover()
                    await asyncio.sleep(random.uniform(2, 5))
                    
                    elements_checked += 1
                    
                except Exception as e:
                    logging.debug(f"Contact check error: {e}")
                    elements_checked += 1
            
            return True
            
        except Exception as e:
            logging.debug(f"Check contact info failed: {e}")
            return False
    
    async def _default_activity(self, page, duration: int) -> bool:
        """Default activity - combination of scrolling and waiting"""
        
        try:
            end_time = time.time() + duration
            
            while time.time() < end_time:
                # Random action
                action = random.choice([
                    "scroll_down", "scroll_up", "wait", "small_scroll"
                ])
                
                if action == "scroll_down":
                    await page.mouse.wheel(0, random.randint(200, 500))
                elif action == "scroll_up":
                    await page.mouse.wheel(0, -random.randint(100, 300))
                elif action == "small_scroll":
                    await page.mouse.wheel(0, random.randint(50, 150))
                else:  # wait
                    pass
                
                # Always pause
                await asyncio.sleep(random.uniform(2, 6))
            
            return True
            
        except Exception as e:
            logging.debug(f"Default activity failed: {e}")
            return False


# Integration function to replace the existing _visit_target_site method
async def enhanced_visit_target_site(page, target_site: str, session_data: Dict, 
                                   persona, autowebglm=None, usimagent=None) -> bool:
    """Enhanced target site visit with comprehensive activities"""
    
    logging.info(f"🌐 Enhanced target site visit starting")
    
    try:
        # Wait for page load
        await page.wait_for_load_state('networkidle', timeout=20000)
        await asyncio.sleep(random.uniform(1, 3))
        
        current_url = page.url
        logging.info(f"📍 Successfully reached: {current_url}")
        
        # Initialize enhanced activity simulator
        activity_simulator = EnhancedSiteActivitySimulator(
            persona=persona,
            autowebglm=autowebglm, 
            usimagent=usimagent
        )
        
        # Execute comprehensive site exploration
        success = await activity_simulator.execute_site_exploration(page, session_data)
        
        # Add enhanced visit step to session data
        session_data["steps"].append({
            "action": "enhanced_visit_target_site",
            "final_url": current_url,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "activity_simulator_used": True
        })
        
        logging.info(f"🎉 Enhanced site visit {'✅ completed' if success else '❌ failed'}")
        
        return success
        
    except Exception as e:
        logging.error(f"❌ Enhanced target site visit failed: {e}")
        session_data["steps"].append({
            "action": "enhanced_visit_target_site_failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "success": False
        })
        return False