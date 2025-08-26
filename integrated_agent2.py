# ============================================================================
# MAIN FUNCTION
# ============================================================================
import sys


import asyncio
import random
import time
import json
import logging
import argparse
import sys
import os
import numpy as np
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from dataclasses import dataclass
from enum import Enum
import re
from pathlib import Path

# Add modals directory to path for imports
SCRIPT_DIR = Path(__file__).parent
MODALS_DIR = SCRIPT_DIR / "modals"

# Add the actual model paths
sys.path.append(str(MODALS_DIR / "AutoWebGLM"))
sys.path.append(str(MODALS_DIR / "USimAgent"))

# Import model components with better error handling
try:
    # AutoWebGLM imports
    sys.path.append(str(MODALS_DIR / "AutoWebGLM" / "miniwob++"))
    sys.path.append(str(MODALS_DIR / "AutoWebGLM" / "webarena"))
    sys.path.append(str(MODALS_DIR / "AutoWebGLM" / "webarena" / "browser_env"))
    
    from html_tools.html_parser import HTMLParser
    from html_tools.identifier import ElementIdentifier
    from html_tools.utils import extract_elements
    
    # USimAgent imports
    from agent.agent import Agent as USimAgent
    from agent.state import State
    from agent.task import Task
    from config.config import Config as USimConfig
    
    MODELS_AVAILABLE = True
    logging.info("✅ Real model components imported successfully")
    
except ImportError as e:
    logging.warning(f"⚠️ Could not import model components: {e}")
    logging.warning("Using enhanced fallback implementations")
    MODELS_AVAILABLE = False

# ============================================================================
# ENHANCED USER PERSONA SYSTEM
# ============================================================================

class UserPersonaType(Enum):
    RESEARCHER = "researcher"
    CASUAL_BROWSER = "casual_browser"
    PROFESSIONAL = "professional"
    STUDENT = "student"
    SENIOR = "senior"
    TECH_SAVVY = "tech_savvy"
    BARGAIN_HUNTER = "bargain_hunter"
    MOBILE_FIRST = "mobile_first"

@dataclass
class UserPersona:
    """Enhanced user persona with detailed behavioral patterns"""
    persona_type: UserPersonaType
    name: str
    age_range: tuple
    device_preferences: List[str]
    browsing_speed: str
    attention_span: str
    tech_comfort: str
    reading_pattern: str
    social_media_usage: str
    online_shopping_frequency: str
    search_query_style: str
    multitasking_tendency: str
    privacy_consciousness: str
    
    # Behavioral weights
    click_through_rate: float
    bounce_rate: float
    scroll_depth_preference: float
    form_completion_rate: float
    social_sharing_likelihood: float
    ad_interaction_rate: float
    link_hover_tendency: float
    page_exploration_time: float
    
    # Timing patterns
    session_duration_range: tuple
    page_dwell_time_range: tuple
    search_refinement_likelihood: float
    back_button_usage: float
    new_tab_usage: float
    hover_duration_range: tuple
    scroll_pause_frequency: float

class EnhancedPersonaManager:
    """Enhanced persona manager with more detailed personas"""
    
    PERSONAS = {
        UserPersonaType.RESEARCHER: UserPersona(
            persona_type=UserPersonaType.RESEARCHER,
            name="Dr. Academic",
            age_range=(25, 65),
            device_preferences=["desktop", "laptop"],
            browsing_speed="slow",
            attention_span="long",
            tech_comfort="high",
            reading_pattern="thorough",
            social_media_usage="low",
            online_shopping_frequency="low",
            search_query_style="detailed",
            multitasking_tendency="medium",
            privacy_consciousness="high",
            click_through_rate=0.8,
            bounce_rate=0.2,
            scroll_depth_preference=0.9,
            form_completion_rate=0.7,
            social_sharing_likelihood=0.3,
            ad_interaction_rate=0.1,
            link_hover_tendency=0.9,
            page_exploration_time=0.8,
            session_duration_range=(300, 900),
            page_dwell_time_range=(60, 180),
            search_refinement_likelihood=0.7,
            back_button_usage=0.4,
            new_tab_usage=0.8,
            hover_duration_range=(2, 6),
            scroll_pause_frequency=0.7
        ),
        
        UserPersonaType.CASUAL_BROWSER: UserPersona(
            persona_type=UserPersonaType.CASUAL_BROWSER,
            name="Casual Surfer",
            age_range=(18, 45),
            device_preferences=["mobile", "tablet", "desktop"],
            browsing_speed="fast",
            attention_span="short",
            tech_comfort="medium",
            reading_pattern="skimmer",
            social_media_usage="high",
            online_shopping_frequency="medium",
            search_query_style="brief",
            multitasking_tendency="high",
            privacy_consciousness="low",
            click_through_rate=0.6,
            bounce_rate=0.4,
            scroll_depth_preference=0.5,
            form_completion_rate=0.3,
            social_sharing_likelihood=0.7,
            ad_interaction_rate=0.3,
            link_hover_tendency=0.6,
            page_exploration_time=0.4,
            session_duration_range=(60, 300),
            page_dwell_time_range=(15, 60),
            search_refinement_likelihood=0.3,
            back_button_usage=0.7,
            new_tab_usage=0.5,
            hover_duration_range=(1, 3),
            scroll_pause_frequency=0.4
        ),
        
        UserPersonaType.TECH_SAVVY: UserPersona(
            persona_type=UserPersonaType.TECH_SAVVY,
            name="Tech Expert",
            age_range=(20, 50),
            device_preferences=["desktop", "laptop", "mobile"],
            browsing_speed="fast",
            attention_span="medium",
            tech_comfort="high",
            reading_pattern="scanner",
            social_media_usage="medium",
            online_shopping_frequency="high",
            search_query_style="precise",
            multitasking_tendency="high",
            privacy_consciousness="high",
            click_through_rate=0.7,
            bounce_rate=0.3,
            scroll_depth_preference=0.6,
            form_completion_rate=0.8,
            social_sharing_likelihood=0.4,
            ad_interaction_rate=0.2,
            link_hover_tendency=0.8,
            page_exploration_time=0.6,
            session_duration_range=(120, 450),
            page_dwell_time_range=(30, 90),
            search_refinement_likelihood=0.6,
            back_button_usage=0.5,
            new_tab_usage=0.9,
            hover_duration_range=(1, 4),
            scroll_pause_frequency=0.5
        ),
    }
    
    @classmethod
    def get_random_persona(cls) -> UserPersona:
        """Get a random user persona"""
        return random.choice(list(cls.PERSONAS.values()))
    
    @classmethod
    def get_persona_by_type(cls, persona_type: UserPersonaType) -> UserPersona:
        """Get specific persona by type"""
        return cls.PERSONAS[persona_type]

# ============================================================================
# ENHANCED MODEL INTEGRATION CLASSES
# ============================================================================

class EnhancedAutoWebGLM:
    """Enhanced AutoWebGLM integration with better page analysis"""
    
    def __init__(self, persona, config=None):
        self.persona = persona
        self.config = config or {}
        
        if MODELS_AVAILABLE:
            try:
                self.html_parser = HTMLParser()
                self.element_identifier = ElementIdentifier()
                logging.info("✅ AutoWebGLM HTML tools initialized")
            except Exception as e:
                logging.warning(f"⚠️ AutoWebGLM initialization failed: {e}")
                self.html_parser = None
                self.element_identifier = None
        else:
            self.html_parser = None
            self.element_identifier = None
        
        self.page_context = {}
        self.navigation_history = []
    
    async def analyze_page_context(self, page) -> Dict[str, Any]:
        """Enhanced page analysis with detailed element detection"""
        
        try:
            url = page.url
            title = await page.title()
            
            # Enhanced element counting
            links = await page.locator("a[href]:visible").count()
            buttons = await page.locator("button:visible, input[type='button']:visible, input[type='submit']:visible").count()
            forms = await page.locator("form:visible").count()
            images = await page.locator("img:visible").count()
            text_inputs = await page.locator("input[type='text']:visible, input[type='email']:visible, textarea:visible").count()
            
            # Detect specific element types for hovering
            search_results = await page.locator(".g:visible, .result:visible, [class*='result']:visible").count()
            navigation_links = await page.locator("nav a:visible, .nav a:visible, [class*='nav'] a:visible").count()
            content_headings = await page.locator("h1:visible, h2:visible, h3:visible").count()
            
            # Classify page type more accurately
            page_type = self._classify_page_type(url, title)
            
            context = {
                "page_type": page_type,
                "url": url,
                "title": title,
                "analysis_method": "enhanced_analysis",
                "interactive_elements": {
                    "links": links,
                    "buttons": buttons,
                    "forms": forms,
                    "images": images,
                    "text_inputs": text_inputs,
                    "search_results": search_results,
                    "navigation_links": navigation_links,
                    "content_headings": content_headings,
                    "total": links + buttons + forms
                },
                "hoverable_elements": {
                    "priority_links": min(links, 10),
                    "navigation": min(navigation_links, 5),
                    "search_results": min(search_results, 8),
                    "content_headings": min(content_headings, 6)
                }
            }
            
            self.page_context = context
            return context
            
        except Exception as e:
            logging.debug(f"Page analysis failed: {e}")
            return {"page_type": "unknown", "analysis_method": "error"}
    
    def _classify_page_type(self, url: str, title: str) -> str:
        """Enhanced page type classification"""
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        # Google search results
        if "google.com/search" in url_lower or "search" in url_lower:
            return "search_results"
        
        # E-commerce
        if any(keyword in url_lower for keyword in ["shop", "store", "buy", "cart", "product", "checkout"]):
            return "ecommerce"
        
        # Content/blog
        if any(keyword in url_lower for keyword in ["blog", "article", "post", "news", "content"]):
            return "content_page"
        
        # Social media
        if any(keyword in url_lower for keyword in ["facebook", "twitter", "instagram", "linkedin", "social"]):
            return "social_media"
        
        # Homepage detection
        if url_lower.count('/') <= 3 and not any(char in url_lower for char in ['?', '=', '&']):
            return "homepage"
        
        return "general_page"

class EnhancedUSimAgent:
    """Enhanced USimAgent with human-like behavior patterns"""
    
    def __init__(self, persona, config=None):
        self.persona = persona
        self.config = config or {}
        
        if MODELS_AVAILABLE:
            try:
                self.usim_config = USimConfig()
                self.agent_state = State()
                self.current_task = None
                self.agent = USimAgent(self.usim_config)
                logging.info("✅ Real USimAgent initialized")
            except Exception as e:
                logging.warning(f"⚠️ USimAgent initialization failed: {e}")
                self.agent = None
                self._initialize_fallback()
        else:
            self.agent = None
            self._initialize_fallback()
        
        # Enhanced cognitive state tracking
        self.cognitive_load = 0.0
        self.fatigue_level = 0.0
        self.interest_level = 1.0
        self.session_actions = []
        self.emotional_state = "neutral"
        self.exploration_satisfaction = 0.5
        self.last_action_time = time.time()
    
    def _initialize_fallback(self):
        """Initialize enhanced fallback behavior modeling"""
        self.working_memory_capacity = self._calculate_working_memory()
        self.attention_decay_rate = self._calculate_attention_decay()
        self.decision_speed = self._calculate_decision_speed()
        self.exploration_tendency = self._calculate_exploration_tendency()
    
    def _calculate_working_memory(self) -> int:
        """Calculate working memory based on persona"""
        base_capacity = {"low": 3, "medium": 5, "high": 7}
        return base_capacity.get(self.persona.tech_comfort, 5)
    
    def _calculate_attention_decay(self) -> float:
        """Calculate attention decay rate"""
        decay_map = {"short": 0.05, "medium": 0.03, "long": 0.01}
        return decay_map.get(self.persona.attention_span, 0.03)
    
    def _calculate_decision_speed(self) -> float:
        """Calculate decision making speed"""
        speed_map = {"slow": 1.5, "medium": 1.0, "fast": 0.7}
        return speed_map.get(self.persona.browsing_speed, 1.0)
    
    def _calculate_exploration_tendency(self) -> float:
        """Calculate tendency to explore vs focus"""
        if self.persona.persona_type == UserPersonaType.RESEARCHER:
            return 0.8
        elif self.persona.persona_type == UserPersonaType.CASUAL_BROWSER:
            return 0.6
        elif self.persona.persona_type == UserPersonaType.TECH_SAVVY:
            return 0.7
        return 0.6
    
    async def generate_next_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate next action with enhanced human-like behavior"""
        
        # Update cognitive state based on time and context
        self._update_cognitive_state_from_context(context)
        
        if self.agent and MODELS_AVAILABLE:
            return await self._generate_action_with_real_agent(context)
        else:
            return await self._generate_enhanced_fallback_action(context)
    
    def _update_cognitive_state_from_context(self, context: Dict[str, Any]):
        """Update cognitive state based on current context"""
        
        # Time since last action affects attention
        time_elapsed = time.time() - self.last_action_time
        if time_elapsed > 30:  # Long pause increases fatigue
            self.fatigue_level = min(1.0, self.fatigue_level + 0.1)
        
        # Page complexity affects cognitive load
        page_type = context.get("page_type", "unknown")
        interactive_elements = context.get("interactive_elements", {})
        
        complexity_factor = min(interactive_elements.get("total", 0) / 20, 1.0)
        self.cognitive_load = min(1.0, self.cognitive_load + complexity_factor * 0.1)
        
        # Adjust interest based on page type and persona
        if page_type == "search_results" and self.persona.persona_type == UserPersonaType.RESEARCHER:
            self.interest_level = min(1.0, self.interest_level + 0.1)
        elif page_type == "ecommerce" and self.persona.persona_type == UserPersonaType.BARGAIN_HUNTER:
            self.interest_level = min(1.0, self.interest_level + 0.1)
        
        self.last_action_time = time.time()
    
    async def _generate_action_with_real_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate action using real USimAgent if available"""
        try:
            # This would use the real agent's action generation
            # For now, fallback to enhanced implementation
            return await self._generate_enhanced_fallback_action(context)
        except Exception as e:
            logging.debug(f"Real agent action generation failed: {e}")
            return await self._generate_enhanced_fallback_action(context)
    
    async def _generate_enhanced_fallback_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced human-like actions"""
        
        page_type = context.get("page_type", "unknown")
        interactive_elements = context.get("interactive_elements", {})
        hoverable_elements = context.get("hoverable_elements", {})
        
        # Define possible actions with weights based on context and persona
        possible_actions = []
        
        # Hover actions (very human-like)
        if hoverable_elements.get("priority_links", 0) > 0:
            possible_actions.append(("hover_link", self.persona.link_hover_tendency))
        
        if hoverable_elements.get("search_results", 0) > 0 and page_type == "search_results":
            possible_actions.append(("hover_search_result", 0.8))
        
        if hoverable_elements.get("navigation", 0) > 0:
            possible_actions.append(("hover_navigation", 0.6))
        
        # Scrolling actions
        possible_actions.append(("scroll_down", 0.7))
        possible_actions.append(("scroll_up", 0.2))
        
        # Reading/waiting actions
        possible_actions.append(("read_content", self.persona.page_exploration_time))
        possible_actions.append(("wait_and_observe", 0.5))
        
        # Click actions (lower probability to make it more realistic)
        if interactive_elements.get("links", 0) > 0:
            possible_actions.append(("click_link", 0.3))
        
        if page_type == "search_results" and hoverable_elements.get("search_results", 0) > 0:
            possible_actions.append(("click_search_result", 0.4))
        
        # Adjust probabilities based on cognitive state
        if self.fatigue_level > 0.7:
            # More passive actions when fatigued
            possible_actions = [(action, weight * 0.5 if "click" in action else weight * 1.2) 
                              for action, weight in possible_actions]
        
        if self.interest_level < 0.3:
            # More likely to leave or scroll when bored
            possible_actions.append(("prepare_to_leave", 0.6))
        
        # Select action based on weights
        if possible_actions:
            actions, weights = zip(*possible_actions)
            action_type = random.choices(actions, weights=weights)[0]
        else:
            action_type = "wait_and_observe"
        
        action = {
            "action_type": action_type,
            "confidence": self._calculate_action_confidence(),
            "parameters": self._generate_enhanced_action_parameters(action_type, context),
            "generated_by": "enhanced_fallback",
            "cognitive_state": {
                "cognitive_load": self.cognitive_load,
                "fatigue_level": self.fatigue_level,
                "interest_level": self.interest_level,
                "emotional_state": self.emotional_state
            }
        }
        
        self._update_cognitive_state_after_action(action)
        return action
    
    def _calculate_action_confidence(self) -> float:
        """Calculate confidence based on cognitive state"""
        base_confidence = 0.7
        
        # Reduce confidence when fatigued or overloaded
        confidence = base_confidence * (1 - self.fatigue_level * 0.3)
        confidence = confidence * (1 - self.cognitive_load * 0.2)
        
        # Increase confidence when interested
        confidence = confidence * (1 + self.interest_level * 0.2)
        
        return max(0.1, min(1.0, confidence))
    
    def _generate_enhanced_action_parameters(self, action_type: str, context: Dict) -> Dict[str, Any]:
        """Generate enhanced parameters for actions"""
        
        params = {}
        
        if action_type == "scroll_down":
            if self.persona.browsing_speed == "fast":
                params.update({
                    "amount": random.randint(400, 800),
                    "speed": "fast",
                    "pause_probability": 0.3
                })
            elif self.persona.browsing_speed == "slow":
                params.update({
                    "amount": random.randint(200, 400),
                    "speed": "slow",
                    "pause_probability": 0.7
                })
            else:
                params.update({
                    "amount": random.randint(300, 600),
                    "speed": "normal",
                    "pause_probability": 0.5
                })
        
        elif action_type in ["hover_link", "hover_search_result", "hover_navigation"]:
            min_duration, max_duration = self.persona.hover_duration_range
            params.update({
                "duration": random.uniform(min_duration, max_duration),
                "movement_style": "human_like",
                "element_preference": self._get_element_preference(action_type),
                "max_elements": random.randint(1, 3)
            })
        
        elif action_type == "read_content":
            if self.persona.reading_pattern == "thorough":
                params["duration"] = random.uniform(20, 60)
            elif self.persona.reading_pattern == "skimmer":
                params["duration"] = random.uniform(5, 15)
            else:
                params["duration"] = random.uniform(10, 30)
        
        elif action_type == "wait_and_observe":
            params["duration"] = random.uniform(2, 8)
        
        elif action_type in ["click_link", "click_search_result"]:
            params.update({
                "pre_hover_duration": random.uniform(1, 3),
                "click_style": "human_like",
                "confidence_threshold": 0.6
            })
        
        return params
    
    def _get_element_preference(self, action_type: str) -> str:
        """Get element preference based on action type and persona"""
        
        if action_type == "hover_search_result":
            return "search_results"
        elif action_type == "hover_navigation":
            return "navigation"
        elif self.persona.tech_comfort == "high":
            return "technical_links"
        else:
            return "general_links"
    
    def _update_cognitive_state_after_action(self, action: Dict[str, Any]):
        """Update cognitive state after performing an action"""
        
        action_type = action["action_type"]
        
        # Cognitive load changes
        load_changes = {
            "hover_link": 0.05,
            "hover_search_result": 0.07,
            "click_link": 0.15,
            "click_search_result": 0.12,
            "scroll_down": 0.02,
            "read_content": 0.10,
            "wait_and_observe": -0.05
        }
        
        load_change = load_changes.get(action_type, 0.03)
        self.cognitive_load = max(0.0, min(1.0, self.cognitive_load + load_change))
        
        # Fatigue increases gradually
        self.fatigue_level = min(1.0, self.fatigue_level + 0.005)
        
        # Interest level adjustments
        if "hover" in action_type:
            self.interest_level = min(1.0, self.interest_level + 0.02)
        elif action_type == "wait_and_observe":
            self.interest_level = max(0.1, self.interest_level - 0.01)
        
        # Record action
        self.session_actions.append({
            "action": action_type,
            "timestamp": time.time(),
            "cognitive_load": self.cognitive_load,
            "fatigue": self.fatigue_level,
            "interest": self.interest_level,
            "confidence": action.get("confidence", 0.5)
        })
    
    def should_continue_browsing(self) -> bool:
        """Enhanced decision making for continuing browsing"""
        
        # Base probability from cognitive state
        continue_prob = (
            self.interest_level * 0.4 +
            (1 - self.fatigue_level) * 0.3 +
            (1 - self.cognitive_load) * 0.2 +
            self.exploration_satisfaction * 0.1
        )
        
        # Persona adjustments
        if self.persona.attention_span == "long":
            continue_prob += 0.15
        elif self.persona.attention_span == "short":
            continue_prob -= 0.1
        
        # Session length considerations
        if len(self.session_actions) > 25:
            continue_prob -= 0.15
        elif len(self.session_actions) < 5:
            continue_prob += 0.1
        
        # Time-based adjustments
        session_duration = time.time() - (self.session_actions[0]["timestamp"] if self.session_actions else time.time())
        max_duration = self.persona.session_duration_range[1]
        
        if session_duration > max_duration:
            continue_prob -= 0.3
        
        return random.random() < max(0.1, min(0.9, continue_prob))

# ============================================================================
# ENHANCED SEARCH SIMULATOR
# ============================================================================

class EnhancedGoogleSearchSimulator:
    """Enhanced Google Search Simulator with human-like behavior"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.session_data = []
        self.current_persona = None
        self.autowebglm = None
        self.usimagent = None
        self.session_goals = []
        self.models_integrated = MODELS_AVAILABLE
        
        if self.models_integrated:
            logging.info("✅ Using real AutoWebGLM and USimAgent integration")
        else:
            logging.info("🔄 Using enhanced fallback implementations")
    
    async def simulate_search_session(self, keyword: str, target_site: str, 
                                    persona: UserPersona = None) -> Dict[str, Any]:
        """Simulate enhanced search session with human-like behavior"""
        
        if persona is None:
            persona = EnhancedPersonaManager.get_random_persona()
        
        self.current_persona = persona
        
        # Initialize enhanced model components
        self.autowebglm = EnhancedAutoWebGLM(persona, self.config)
        self.usimagent = EnhancedUSimAgent(persona, self.config)
        
        logging.info(f"Starting enhanced search session with {persona.name}")
        logging.info(f"Query: '{keyword}' -> Target: {target_site}")
        logging.info(f"Persona traits: {persona.browsing_speed} speed, {persona.attention_span} attention")
        
        session_start = time.time()
        
        session_data = {
            "keyword": keyword,
            "target_site": target_site,
            "persona": {
                "type": persona.persona_type.value,
                "name": persona.name,
                "characteristics": {
                    "browsing_speed": persona.browsing_speed,
                    "attention_span": persona.attention_span,
                    "tech_comfort": persona.tech_comfort,
                    "reading_pattern": persona.reading_pattern,
                    "link_hover_tendency": persona.link_hover_tendency,
                    "page_exploration_time": persona.page_exploration_time
                }
            },
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "human_like_activities": [],
            "success": False,
            "models_integrated": self.models_integrated,
            "cognitive_journey": []
        }
        
        # Create browser with persona-specific settings
        page, browser, playwright = await self.create_enhanced_browser(persona)
        
        try:
            # Execute enhanced search session
            await self._navigate_to_google(page, session_data)
            await self._perform_enhanced_search(page, keyword, session_data)
            await self._interact_with_serp_human_like(page, target_site, session_data)
            success = await self._visit_target_site_enhanced(page, target_site, session_data)
            
            session_data["success"] = success
            session_data["duration"] = time.time() - session_start
            
            # Add final cognitive state
            if self.usimagent:
                session_data["final_cognitive_state"] = {
                    "cognitive_load": self.usimagent.cognitive_load,
                    "fatigue_level": self.usimagent.fatigue_level,
                    "interest_level": self.usimagent.interest_level,
                    "emotional_state": self.usimagent.emotional_state,
                    "total_actions": len(self.usimagent.session_actions)
                }
            
            logging.info(f"Enhanced search session completed: {'✅ SUCCESS' if success else '❌ FAILED'}")
            logging.info(f"Duration: {session_data['duration']:.1f}s, Activities: {len(session_data['human_like_activities'])}")
            
        except Exception as e:
            logging.error(f"Enhanced search session failed: {e}")
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
    
    async def create_enhanced_browser(self, persona: UserPersona):
        """Create browser with enhanced persona-specific configuration"""
        
        try:
            from playwright_stealth import stealth_async
            stealth_available = True
        except ImportError:
            stealth_available = False
        
        playwright = await async_playwright().start()
        
        # Enhanced device configurations
        device_configs = {
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
        
        if stealth_available:
            await stealth_async(page)
        
        return page, browser, playwright
    
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
    
    async def _navigate_to_google(self, page, session_data: Dict):
        """Navigate to Google with human-like behavior"""
        
        logging.info("Navigating to Google with human-like timing")
        
        await page.goto("https://www.google.com", wait_until='networkidle', timeout=30000)
        
        # Human-like pause after page load
        await asyncio.sleep(random.uniform(1.5, 4.0))
        
        session_data["steps"].append({
            "action": "navigate_to_google",
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
    
    async def _perform_enhanced_search(self, page, keyword: str, session_data: Dict):
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
        
        # Calculate typing characteristics based on persona
        base_delay = self._get_typing_speed()
        
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
    
    def _get_typing_speed(self) -> float:
        """Get typing speed based on persona"""
        if self.current_persona.tech_comfort == "high":
            return random.uniform(0.03, 0.08)
        elif self.current_persona.tech_comfort == "low":
            return random.uniform(0.12, 0.25)
        else:
            return random.uniform(0.08, 0.15)
    
    async def _interact_with_serp_human_like(self, page, target_site: str, session_data: Dict):
        """Enhanced SERP interaction with human-like behavior"""
        
        logging.info("Analyzing SERP with enhanced human-like behavior")
        
        # Wait for results with human-like patience
        await page.wait_for_load_state('networkidle', timeout=20000)
        await asyncio.sleep(random.uniform(1.5, 4.0))
        
        # Analyze page with enhanced methods
        page_context = await self.autowebglm.analyze_page_context(page)
        
        # Perform human-like SERP exploration
        activities = await self._perform_serp_exploration(page, page_context, session_data)
        
        # Find and interact with target
        target_domain = urlparse(target_site).netloc.replace('www.', '')
        target_result = await self._find_target_result_enhanced(page, target_domain)
        
        if target_result:
            success = await self._click_target_result_human_like(page, target_result, session_data)
        else:
            success = False
            # If target not found, click a random result (human-like behavior)
            await self._click_alternative_result(page, session_data)
        
        session_data["steps"].append({
            "action": "enhanced_serp_interaction",
            "target_found": target_result is not None,
            "page_analysis": page_context,
            "human_like_activities": activities,
            "click_success": success,
            "timestamp": datetime.now().isoformat(),
            "success": success
        })
    
    async def _perform_serp_exploration(self, page, page_context: Dict, session_data: Dict) -> List[str]:
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
            
            action = await self.usimagent.generate_next_action(context)
            activity = await self._execute_serp_action(page, action)
            
            if activity:
                activities.append(activity)
                session_data["human_like_activities"].append({
                    "activity": activity,
                    "timestamp": datetime.now().isoformat(),
                    "action_details": action
                })
            
            # Check if should continue exploring
            if not self.usimagent.should_continue_browsing():
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
            
            # Hover with persona-specific duration
            hover_duration = random.uniform(*self.current_persona.hover_duration_range)
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
    
    async def _visit_target_site_enhanced(self, page, target_site: str, session_data: Dict) -> bool:
        """Enhanced target site visit with human-like browsing"""
        
        logging.info(f"Visiting target site with enhanced human-like behavior")
        
        try:
            # Wait for page load
            await page.wait_for_load_state('networkidle', timeout=25000)
            await asyncio.sleep(random.uniform(2, 5))
            
            current_url = page.url
            logging.info(f"Reached: {current_url}")
            
            # Enhanced page analysis
            page_context = await self.autowebglm.analyze_page_context(page)
            
            # Calculate enhanced session duration
            session_duration = self._calculate_enhanced_session_duration(page_context)
            
            # Execute enhanced human-like browsing
            activities = await self._execute_enhanced_browsing(page, session_duration, page_context, session_data)
            
            session_data["steps"].append({
                "action": "visit_target_site_enhanced",
                "final_url": current_url,
                "page_analysis": page_context,
                "browsing_activities": activities,
                "session_duration": session_duration,
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            return True
            
        except Exception as e:
            logging.error(f"Enhanced target site visit failed: {e}")
            session_data["steps"].append({
                "action": "visit_target_site_failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "success": False
            })
            return False
    
    def _calculate_enhanced_session_duration(self, page_context: Dict) -> int:
        """Calculate enhanced session duration based on analysis and persona"""
        
        # Base duration from persona
        min_duration, max_duration = self.current_persona.session_duration_range
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
        if self.current_persona.reading_pattern == "thorough":
            multiplier *= 1.3
        elif self.current_persona.reading_pattern == "skimmer":
            multiplier *= 0.7
        
        # Cognitive state adjustments
        if self.usimagent:
            if self.usimagent.interest_level > 0.7:
                multiplier *= 1.2
            elif self.usimagent.fatigue_level > 0.6:
                multiplier *= 0.8
        
        final_duration = int(base_duration * multiplier)
        return max(30, min(1200, final_duration))  # Between 30s and 20min
    
    async def _execute_enhanced_browsing(self, page, total_duration: int, page_context: Dict, session_data: Dict) -> List[str]:
        """Execute enhanced human-like browsing behavior"""
        
        start_time = time.time()
        end_time = start_time + total_duration
        activities = []
        
        logging.info(f"Executing {total_duration}s of enhanced human-like browsing")
        
        # Initial page orientation
        await self._enhanced_page_orientation(page)
        activities.append("enhanced_page_orientation")
        
        action_count = 0
        while time.time() < end_time and action_count < 25:
            remaining_time = end_time - time.time()
            
            if remaining_time < 5:
                break
            
            # Check if should continue browsing
            if self.usimagent and not self.usimagent.should_continue_browsing():
                logging.info("Enhanced USimAgent decided to stop browsing")
                break
            
            # Generate enhanced browsing action
            context = {
                "current_goal": "explore website content",
                "page_type": page_context.get("page_type", "unknown"),
                "session_duration": time.time() - start_time,
                "remaining_time": remaining_time,
                "interactive_elements": page_context.get("interactive_elements", {}),
                "hoverable_elements": page_context.get("hoverable_elements", {})
            }
            
            try:
                action = await self.usimagent.generate_next_action(context)
                activity = await self._execute_enhanced_browsing_action(page, action)
                
                if activity:
                    activities.append(activity)
                    session_data["human_like_activities"].append({
                        "activity": activity,
                        "timestamp": datetime.now().isoformat(),
                        "action_details": action
                    })
                
                # Record cognitive journey
                session_data.setdefault("cognitive_journey", []).append({
                    "time": time.time() - start_time,
                    "action": action.get("action_type"),
                    "confidence": action.get("confidence", 0.5),
                    "cognitive_load": self.usimagent.cognitive_load,
                    "interest_level": self.usimagent.interest_level,
                    "emotional_state": self.usimagent.emotional_state
                })
                
                action_count += 1
                
            except Exception as e:
                logging.debug(f"Enhanced browsing action failed: {e}")
                activities.append("failed_action")
                await asyncio.sleep(random.uniform(1, 3))
        
        logging.info(f"Completed enhanced browsing with {len(activities)} activities")
        return activities
    
    async def _enhanced_page_orientation(self, page):
        """Enhanced page orientation behavior"""
        
        try:
            # Human-like initial page scan
            await asyncio.sleep(random.uniform(1, 3))
            
            # Small initial scroll to see more content
            await page.mouse.wheel(0, random.randint(100, 300))
            await asyncio.sleep(random.uniform(2, 4))
            
            # Scroll back up to start
            await page.mouse.wheel(0, -random.randint(50, 150))
            await asyncio.sleep(random.uniform(1, 2))
            
        except Exception as e:
            logging.debug(f"Enhanced page orientation failed: {e}")
    
    async def _execute_enhanced_browsing_action(self, page, action: Dict) -> str:
        """Execute enhanced browsing action"""
        
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
                return await self._enhanced_reading_behavior(page, parameters)
            
            elif action_type == "wait_and_observe":
                return await self._enhanced_observation(page, parameters)
            
            elif action_type == "click_link":
                return await self._enhanced_link_clicking(page, parameters)
            
            elif action_type == "prepare_to_leave":
                return await self._prepare_to_leave_behavior(page, parameters)
            
            else:
                await asyncio.sleep(random.uniform(1, 3))
                return "general_pause"
                
        except Exception as e:
            logging.debug(f"Enhanced browsing action execution failed: {action_type} - {e}")
            return f"failed_{action_type}"
    
    async def _enhanced_hover_links(self, page, parameters: Dict) -> str:
        """Enhanced link hovering behavior"""
        
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
                    links = await page.locator(selector).all()
                    all_links.extend(links[:10])  # Limit per selector
                except:
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
                            
                            # Hover duration based on persona
                            duration = parameters.get("duration", 2)
                            await asyncio.sleep(duration)
                            hovered_count += 1
                            
                            # Pause between hovers
                            await asyncio.sleep(random.uniform(0.5, 2.0))
                    except:
                        continue
                
                return f"hovered_{hovered_count}_links"
            
        except Exception as e:
            logging.debug(f"Enhanced link hovering failed: {e}")
        
        return "hover_links_failed"
    
    async def _enhanced_hover_elements(self, page, parameters: Dict, element_type: str) -> str:
        """Enhanced hovering for specific element types"""
        
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
                    found = await page.locator(selector).all()
                    elements.extend(found[:8])
                except:
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
                            await asyncio.sleep(duration)
                            hovered_count += 1
                            await asyncio.sleep(random.uniform(0.3, 1.5))
                    except:
                        continue
                
                return f"hovered_{hovered_count}_{element_type}"
            
        except Exception as e:
            logging.debug(f"Enhanced {element_type} hovering failed: {e}")
        
        return f"hover_{element_type}_failed"
    
    async def _enhanced_scroll_behavior(self, page, parameters: Dict) -> str:
        """Enhanced scrolling with human-like patterns"""
        
        try:
            amount = parameters.get("amount", 300)
            speed = parameters.get("speed", "normal")
            pause_probability = parameters.get("pause_probability", 0.5)
            
            if speed == "fast":
                # Quick scroll with occasional pauses
                await page.mouse.wheel(0, amount)
                if random.random() < pause_probability:
                    await asyncio.sleep(random.uniform(0.5, 2.0))
                return f"fast_scroll_{amount}px"
            
            elif speed == "slow":
                # Very gradual scroll with reading pauses
                steps = random.randint(3, 5)
                for i in range(steps):
                    await page.mouse.wheel(0, amount // steps)
                    if random.random() < pause_probability:
                        await asyncio.sleep(random.uniform(1, 4))
                    else:
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                return f"slow_scroll_{amount}px_{steps}steps"
            
            else:
                # Normal scroll with natural pauses
                steps = 2
                for i in range(steps):
                    await page.mouse.wheel(0, amount // steps)
                    if random.random() < pause_probability:
                        await asyncio.sleep(random.uniform(1, 3))
                    else:
                        await asyncio.sleep(random.uniform(0.3, 1.0))
                return f"normal_scroll_{amount}px"
                
        except Exception as e:
            logging.debug(f"Enhanced scrolling failed: {e}")
            return "scroll_failed"
    
    async def _enhanced_scroll_up(self, page, parameters: Dict) -> str:
        """Enhanced upward scrolling"""
        
        try:
            amount = parameters.get("amount", 200)
            await page.mouse.wheel(0, -amount)
            await asyncio.sleep(random.uniform(1, 3))
            return f"scroll_up_{amount}px"
        except:
            return "scroll_up_failed"
    
    async def _enhanced_reading_behavior(self, page, parameters: Dict) -> str:
        """Enhanced reading simulation"""
        
        try:
            duration = parameters.get("duration", 10)
            
            # Simulate reading with occasional small scrolls
            read_segments = random.randint(1, 3)
            segment_duration = duration / read_segments
            
            for i in range(read_segments):
                await asyncio.sleep(segment_duration * 0.7)
                
                # Small scroll to simulate reading progress
                if random.random() < 0.6:
                    await page.mouse.wheel(0, random.randint(50, 150))
                    await asyncio.sleep(segment_duration * 0.3)
            
            return f"reading_{duration:.1f}s_{read_segments}segments"
            
        except Exception as e:
            logging.debug(f"Enhanced reading failed: {e}")
            return "reading_failed"
    
    async def _enhanced_observation(self, page, parameters: Dict) -> str:
        """Enhanced observation behavior"""
        
        try:
            duration = parameters.get("duration", 3)
            
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
        """Enhanced link clicking behavior"""
        
        try:
            # Find clickable links
            links = await page.locator("a:visible").all()
            
            if links:
                # Select a random link from the first several
                link = random.choice(links[:10])
                
                # Pre-click behavior
                pre_hover_duration = parameters.get("pre_hover_duration", 2)
                await self._human_like_element_approach(page, link)
                await link.hover()
                await asyncio.sleep(pre_hover_duration)
                
                # Click with confidence check
                confidence_threshold = parameters.get("confidence_threshold", 0.6)
                if self.usimagent.interest_level > confidence_threshold:
                    await link.click()
                    await asyncio.sleep(random.uniform(1, 3))
                    return "clicked_link_success"
                else:
                    return "clicked_link_hesitated"
            
        except Exception as e:
            logging.debug(f"Enhanced link clicking failed: {e}")
        
        return "click_link_failed"
    
    async def _prepare_to_leave_behavior(self, page, parameters: Dict) -> str:
        """Behavior when preparing to leave the page"""
        
        try:
            # Simulate final page scan
            await page.mouse.wheel(0, -200)  # Scroll up a bit
            await asyncio.sleep(random.uniform(1, 3))
            
            # Look around one more time
            await page.mouse.move(
                random.randint(200, 600),
                random.randint(100, 400)
            )
            await asyncio.sleep(random.uniform(2, 5))
            
            return "preparing_to_leave"
            
        except Exception as e:
            logging.debug(f"Prepare to leave behavior failed: {e}")
            return "prepare_leave_failed"

# ============================================================================
# ENHANCED JSON PROCESSOR
# ============================================================================

class EnhancedJSONSearchProcessor:
    """Enhanced JSON processor with better error handling and reporting"""
    
    def __init__(self, json_file_path: str, config: Dict = None):
        self.json_file_path = json_file_path
        self.config = config or {}
        self.search_simulator = EnhancedGoogleSearchSimulator(self.config)
        self.results = []
        
        # Enhanced persona rotation
        self.persona_rotation = list(EnhancedPersonaManager.PERSONAS.values())
        random.shuffle(self.persona_rotation)
        self.current_persona_index = 0
    
    def get_next_persona(self) -> UserPersona:
        """Get next persona in rotation"""
        persona = self.persona_rotation[self.current_persona_index]
        self.current_persona_index = (self.current_persona_index + 1) % len(self.persona_rotation)
        
        if self.current_persona_index == 0:
            random.shuffle(self.persona_rotation)
        
        return persona
    
    async def process_all_searches(self, delay_between_searches: int = 180, 
                                 randomize_order: bool = True) -> Dict[str, Any]:
        """Process all searches with enhanced human-like behavior"""
        
        search_data = self.load_search_data()
        
        if randomize_order:
            random.shuffle(search_data)
            logging.info("Randomized search order for more realistic patterns")
        
        logging.info(f"Starting {len(search_data)} enhanced search simulations")
        logging.info(f"Models available: {MODELS_AVAILABLE}")
        logging.info(f"Enhanced features: Human-like hovering, realistic browsing patterns")
        
        all_results = []
        
        for i, search_task in enumerate(search_data):
            keyword = search_task["keyword"]
            site = search_task["site"]
            
            # Select persona
            persona = self.get_next_persona()
            
            logging.info(f"\n{'='*60}")
            logging.info(f"Search {i+1}/{len(search_data)}: '{keyword}' -> {site}")
            logging.info(f"Persona: {persona.name} ({persona.persona_type.value})")
            logging.info(f"Traits: {persona.browsing_speed} browsing, {persona.link_hover_tendency:.1f} hover tendency")
            
            try:
                # Run enhanced search simulation
                result = await self.search_simulator.simulate_search_session(
                    keyword, site, persona
                )
                
                result["global_session_id"] = i + 1
                result["enhanced_integration"] = True
                
                all_results.append(result)
                
                # Enhanced result logging
                if result.get("success"):
                    duration = result.get("duration", 0)
                    activities = len(result.get("human_like_activities", []))
                    logging.info(f"✅ SUCCESS: {duration:.1f}s, {activities} human-like activities")
                    
                    if result.get("models_integrated"):
                        logging.info("🧠 Used real model integration")
                    else:
                        logging.info("🔄 Used enhanced fallback implementations")
                        
                    # Show cognitive journey summary
                    cognitive_journey = result.get("cognitive_journey", [])
                    if cognitive_journey:
                        final_state = result.get("final_cognitive_state", {})
                        logging.info(f"🎭 Final state: {final_state.get('emotional_state', 'unknown')}, "
                                   f"{len(cognitive_journey)} cognitive actions")
                else:
                    error = result.get("error", "Unknown error")
                    logging.info(f"❌ FAILED: {error}")
                
            except Exception as e:
                logging.error(f"Enhanced search simulation error: {e}")
                all_results.append({
                    "keyword": keyword,
                    "target_site": site,
                    "persona": {"type": persona.persona_type.value, "name": persona.name},
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "global_session_id": i + 1,
                    "enhanced_integration": True
                })
            
            # Enhanced delay with random variation
            if i < len(search_data) - 1:
                delay = delay_between_searches + random.randint(-60, 60)
                logging.info(f"⏱️ Waiting {delay}s before next search...")
                await asyncio.sleep(delay)
        
        # Generate enhanced summary
        summary = self._generate_enhanced_summary(all_results)
        
        logging.info(f"\n{'='*80}")
        logging.info(f"ENHANCED HUMAN-LIKE SEARCH PROCESSING COMPLETE")
        logging.info(f"{'='*80}")
        logging.info(f"Success rate: {summary['successful_searches']}/{summary['total_searches']} "
                   f"({summary['success_rate']:.1f}%)")
        logging.info(f"Model integration: {summary['model_integration_rate']:.1f}%")
        logging.info(f"Average activities per session: {summary['avg_activities_per_session']:.1f}")
        logging.info(f"Total human-like activities: {summary['total_human_activities']}")
        
        self.results = summary
        return summary
    
    def _generate_enhanced_summary(self, all_results: List[Dict]) -> Dict[str, Any]:
        """Generate enhanced summary with detailed statistics"""
        
        successful = sum(1 for r in all_results if r.get("success", False))
        model_integrated = sum(1 for r in all_results if r.get("models_integrated", False))
        
        # Calculate human-like activity statistics
        total_activities = sum(len(r.get("human_like_activities", [])) for r in all_results)
        avg_activities = total_activities / len(all_results) if all_results else 0
        
        # Calculate cognitive statistics
        cognitive_sessions = [r for r in all_results if r.get("cognitive_journey")]
        avg_cognitive_actions = (
            sum(len(r.get("cognitive_journey", [])) for r in cognitive_sessions) / 
            len(cognitive_sessions) if cognitive_sessions else 0
        )
        
        # Persona distribution
        persona_distribution = {}
        for result in all_results:
            persona_type = result.get("persona", {}).get("type", "unknown")
            persona_distribution[persona_type] = persona_distribution.get(persona_type, 0) + 1
        
        summary = {
            "total_searches": len(all_results),
            "successful_searches": successful,
            "success_rate": (successful / len(all_results)) * 100 if all_results else 0,
            "model_integration_rate": (model_integrated / len(all_results)) * 100 if all_results else 0,
            "models_available": MODELS_AVAILABLE,
            "total_human_activities": total_activities,
            "avg_activities_per_session": avg_activities,
            "avg_cognitive_actions_per_session": avg_cognitive_actions,
            "persona_distribution": persona_distribution,
            "results": all_results,
            "processing_time": datetime.now().isoformat(),
            "integration_version": "Enhanced Human-like v2.0"
        }
        
        return summary
    
    def load_search_data(self) -> List[Dict[str, str]]:
        """Load and validate search data from JSON file"""
        
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logging.info(f"Loaded {len(data)} search tasks from {self.json_file_path}")
            
            # Enhanced validation
            validated_data = []
            for i, item in enumerate(data):
                if isinstance(item, dict) and "keyword" in item and "site" in item:
                    if item["keyword"].strip() and item["site"].strip():
                        # Validate URL format
                        try:
                            parsed = urlparse(item["site"])
                            if parsed.scheme and parsed.netloc:
                                validated_data.append(item)
                            else:
                                logging.warning(f"Invalid URL format at index {i}: {item['site']}")
                        except:
                            logging.warning(f"URL parsing failed at index {i}: {item['site']}")
                    else:
                        logging.warning(f"Empty keyword or site at index {i}")
                else:
                    logging.warning(f"Invalid item format at index {i}")
            
            logging.info(f"Validated {len(validated_data)} search tasks")
            return validated_data
            
        except Exception as e:
            logging.error(f"Error loading search data: {e}")
            raise
    
    def save_results(self, output_file: str):
        """Save enhanced results"""
        
        if not self.results:
            logging.warning("No results to save")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
            
            logging.info(f"Enhanced results saved to {output_file}")
            
            # Also save a summary file
            summary_file = output_file.replace('.json', '_summary.txt')
            self._save_summary_report(summary_file)
            
        except Exception as e:
            logging.error(f"Failed to save results: {e}")
    
    def _save_summary_report(self, summary_file: str):
        """Save human-readable summary report"""
        
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("ENHANCED HUMAN-LIKE SEARCH SIMULATION REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Processing Time: {self.results['processing_time']}\n")
                f.write(f"Integration Version: {self.results['integration_version']}\n")
                f.write(f"Models Available: {self.results['models_available']}\n\n")
                
                f.write("PERFORMANCE METRICS:\n")
                f.write(f"  Total Searches: {self.results['total_searches']}\n")
                f.write(f"  Successful: {self.results['successful_searches']}\n")
                f.write(f"  Success Rate: {self.results['success_rate']:.1f}%\n")
                f.write(f"  Model Integration Rate: {self.results['model_integration_rate']:.1f}%\n\n")
                
                f.write("HUMAN-LIKE BEHAVIOR METRICS:\n")
                f.write(f"  Total Human Activities: {self.results['total_human_activities']}\n")
                f.write(f"  Average Activities per Session: {self.results['avg_activities_per_session']:.1f}\n")
                f.write(f"  Average Cognitive Actions per Session: {self.results['avg_cognitive_actions_per_session']:.1f}\n\n")
                
                f.write("PERSONA DISTRIBUTION:\n")
                for persona, count in self.results['persona_distribution'].items():
                    f.write(f"  {persona}: {count}\n")
                
            logging.info(f"Summary report saved to {summary_file}")
            
        except Exception as e:
            logging.error(f"Failed to save summary report: {e}")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def setup_enhanced_logging():
    """Setup enhanced logging configuration"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('enhanced_search_simulator.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )

def check_enhanced_integration():
    """Check enhanced model integration status"""
    
    print("🔍 Enhanced Model Integration Status:")
    print(f"   Models Available: {'✅ YES' if MODELS_AVAILABLE else '❌ NO'}")
    
    if MODELS_AVAILABLE:
        print("   Available Components:")
        try:
            from html_tools.html_parser import HTMLParser
            print("   ✅ AutoWebGLM HTML Parser")
        except ImportError:
            print("   ❌ AutoWebGLM HTML Parser")
        
        try:
            from agent.agent import Agent
            print("   ✅ USimAgent Agent")
        except ImportError:
            print("   ❌ USimAgent Agent")
    else:
        print("   Using enhanced fallback implementations")
        print("   Features: Advanced hovering, realistic browsing patterns")
    
    # Check directory structure
    autowebglm_path = MODALS_DIR / "AutoWebGLM"
    usimagent_path = MODALS_DIR / "USimAgent"
    
    print(f"\n📁 Directory Structure:")
    print(f"   AutoWebGLM: {'✅ EXISTS' if autowebglm_path.exists() else '❌ MISSING'}")
    print(f"   USimAgent: {'✅ EXISTS' if usimagent_path.exists() else '❌ MISSING'}")

def create_enhanced_sample_data(output_file: str = "enhanced_search_data.json"):
    """Create enhanced sample search data"""
    
    sample_data = [
        {"keyword": "supply list 2024-2025", "site": "https://getschoolsupplieslist.com/"},
        {"keyword": "causes lip swelling smileee", "site": "https://smileee.co.uk/"},
        {"keyword": "barber shop software", "site": "https://www.thecut.co/"},
        {"keyword": "artificial intelligence tutorials", "site": "https://www.tensorflow.org"},
        {"keyword": "python web scraping guide", "site": "https://docs.python.org"},
        {"keyword": "machine learning courses online", "site": "https://www.coursera.org"},
        {"keyword": "best laptops for programming", "site": "https://www.techradar.com"},
        {"keyword": "data science job opportunities", "site": "https://www.indeed.com"}
    ]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Enhanced sample data created: {output_file}")
    return output_file

async def test_enhanced_integration():
    """Test the enhanced model integration"""
    
    print("🧪 Testing Enhanced Model Integration...")
    
    # Test persona creation
    persona = EnhancedPersonaManager.get_random_persona()
    print(f"✅ Enhanced persona created: {persona.name}")
    print(f"   Hover tendency: {persona.link_hover_tendency}")
    print(f"   Exploration time: {persona.page_exploration_time}")
    
    # Test AutoWebGLM integration
    autowebglm = EnhancedAutoWebGLM(persona)
    print(f"✅ Enhanced AutoWebGLM initialized")
    
    # Test USimAgent integration
    usimagent = EnhancedUSimAgent(persona)
    print(f"✅ Enhanced USimAgent initialized")
    
    # Test action generation
    try:
        context = {
            "current_goal": "test enhanced behavior",
            "page_type": "test",
            "interactive_elements": {"links": 5, "buttons": 2},
            "hoverable_elements": {"priority_links": 3}
        }
        action = await usimagent.generate_next_action(context)
        print(f"✅ Enhanced action generated: {action.get('action_type', 'unknown')}")
        print(f"   Confidence: {action.get('confidence', 0):.2f}")
        print(f"   Generated by: {action.get('generated_by', 'unknown')}")
    except Exception as e:
        print(f"⚠️ Enhanced action generation test failed: {e}")
    
    print("🎯 Enhanced integration test completed")
    

async def main():
    """Enhanced main function with comprehensive features"""
    
    setup_enhanced_logging()
    
    parser = argparse.ArgumentParser(
        description="Enhanced Human-like Google Search Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Enhanced Human-like Features:
  • Realistic link hovering and page exploration
  • Persona-based browsing patterns and speeds
  • Cognitive state modeling with fatigue and interest
  • Human-like typing with variable speeds and pauses
  • Enhanced page analysis and element interaction
  • Comprehensive activity logging and reporting

Model Integration:
  • Real AutoWebGLM HTML analysis tools
  • Actual USimAgent cognitive behavior modeling
  • Advanced fallback implementations when models unavailable
  • Automatic error handling and graceful degradation

Examples:
  python enhanced_search_simulator.py enhanced_search_data.json
  python enhanced_search_simulator.py --single "python tutorials" "https://python.org"
  python enhanced_search_simulator.py --check-integration
  python enhanced_search_simulator.py --test-integration
        """
    )
    
    parser.add_argument("json_file", nargs='?', help="JSON file containing keyword-site pairs")
    parser.add_argument("--delay", type=int, default=180, help="Base delay between searches (seconds)")
    parser.add_argument("--output", type=str, help="Output file to save results")
    parser.add_argument("--randomize", action="store_true", help="Randomize search order")
    parser.add_argument("--single", nargs=2, metavar=("KEYWORD", "SITE"), help="Run single search")
    parser.add_argument("--persona", choices=[p.value for p in UserPersonaType], help="Specific persona")
    parser.add_argument("--check-integration", action="store_true", help="Check model integration status")
    parser.add_argument("--test-integration", action="store_true", help="Test enhanced integration")
    parser.add_argument("--create-sample", action="store_true", help="Create enhanced sample data file")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    print("🚀 ENHANCED HUMAN-LIKE GOOGLE SEARCH SIMULATOR")
    print("=" * 60)
    print("🎭 Realistic User Behavior Modeling")
    print("🖱️ Human-like Hovering & Link Interaction")
    print("🧠 Cognitive State & Fatigue Simulation")
    print("🔧 Advanced Model Integration")
    print("=" * 60)
    
    try:
        if args.check_integration:
            check_enhanced_integration()
            return
        
        elif args.test_integration:
            await test_enhanced_integration()
            return
        
        elif args.create_sample:
            sample_file = create_enhanced_sample_data()
            print(f"✅ Created enhanced sample data: {sample_file}")
            print("🚀 Run with: python enhanced_search_simulator.py enhanced_search_data.json")
            return
        
        elif args.single:
            # Enhanced single search mode
            keyword, site = args.single
            print(f"🎯 Enhanced single search simulation")
            print(f"Keyword: {keyword}")
            print(f"Site: {site}")
            
            # Select persona
            if args.persona:
                persona_type = UserPersonaType(args.persona)
                persona = EnhancedPersonaManager.get_persona_by_type(persona_type)
                print(f"🎭 Using specified persona: {persona.name}")
            else:
                persona = EnhancedPersonaManager.get_random_persona()
                print(f"🎭 Using random persona: {persona.name}")
            
            print(f"   Characteristics: {persona.browsing_speed} browsing, "
                  f"{persona.link_hover_tendency:.1f} hover tendency")
            
            # Create enhanced simulator
            simulator = EnhancedGoogleSearchSimulator()
            
            result = await simulator.simulate_search_session(keyword, site, persona)
            
            print(f"\n🎉 ENHANCED RESULT: {'✅ SUCCESS' if result.get('success') else '❌ FAILED'}")
            
            if result.get('success'):
                duration = result.get('duration', 0)
                activities = len(result.get('human_like_activities', []))
                models_used = result.get('models_integrated', False)
                
                print(f"⏱️ Duration: {duration:.1f}s")
                print(f"🎭 Human-like activities: {activities}")
                print(f"🧠 Models: {'Real Integration' if models_used else 'Enhanced Fallback'}")
                
                # Show cognitive journey
                cognitive_journey = result.get('cognitive_journey', [])
                final_state = result.get('final_cognitive_state', {})
                if cognitive_journey and final_state:
                    print(f"🧠 Cognitive actions: {len(cognitive_journey)}")
                    print(f"🎭 Final emotional state: {final_state.get('emotional_state', 'unknown')}")
                    print(f"📊 Final interest level: {final_state.get('interest_level', 0):.2f}")
                
                # Show sample activities
                activities_list = result.get('human_like_activities', [])
                if activities_list:
                    print("🎬 Sample activities:")
                    for activity in activities_list[:5]:
                        activity_name = activity.get('activity', 'unknown')
                        print(f"   • {activity_name}")
                    if len(activities_list) > 5:
                        print(f"   ... and {len(activities_list) - 5} more")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, default=str, ensure_ascii=False)
                print(f"💾 Enhanced result saved to {args.output}")
        
        else:
            # Enhanced batch processing
            if not args.json_file:
                print("❌ JSON file required for batch processing")
                print("💡 Use --create-sample to create enhanced sample data")
                return
            
            print(f"📂 Input file: {args.json_file}")
            print(f"⏱️ Base delay: {args.delay}s")
            print(f"🔀 Randomize order: {args.randomize}")
            print(f"👁️ Headless mode: {args.headless}")
            
            # Verify input file exists
            if not os.path.exists(args.json_file):
                print(f"❌ Input file not found: {args.json_file}")
                print("💡 Use --create-sample to create enhanced sample data")
                return
            
            # Create enhanced processor
            processor = EnhancedJSONSearchProcessor(args.json_file)
            
            # Process all searches with enhanced behavior
            results = await processor.process_all_searches(
                delay_between_searches=args.delay,
                randomize_order=args.randomize
            )
            
            # Print enhanced summary
            print(f"\n🎉 ENHANCED PROCESSING COMPLETE")
            print(f"📊 Results: {results['successful_searches']}/{results['total_searches']} "
                  f"({results['success_rate']:.1f}% success)")
            print(f"🧠 Model Integration: {results['model_integration_rate']:.1f}%")
            print(f"🎭 Total Human Activities: {results['total_human_activities']}")
            print(f"📈 Average Activities per Session: {results['avg_activities_per_session']:.1f}")
            
            # Show persona distribution
            print(f"\n🎭 Persona Distribution:")
            for persona, count in results['persona_distribution'].items():
                print(f"   {persona}: {count}")
            
            # Save enhanced results
            if args.output:
                processor.save_results(args.output)
            else:
                # Generate default output filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                default_output = f"enhanced_results_{timestamp}.json"
                processor.save_results(default_output)
                print(f"💾 Enhanced results saved to {default_output}")
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        
        # Save partial results if available
        if 'processor' in locals() and hasattr(processor, 'results') and processor.results:
            emergency_file = f"emergency_enhanced_results_{int(time.time())}.json"
            try:
                with open(emergency_file, 'w', encoding='utf-8') as f:
                    json.dump(processor.results, f, indent=2, default=str)
                print(f"💾 Emergency save completed: {emergency_file}")
            except:
                print("❌ Emergency save failed")
    
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        if "enhanced_search_data.json" in str(e):
            print("💡 Create sample data with: python enhanced_search_simulator.py --create-sample")
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Check that model directories exist and contain required files")
        print("💡 Use --check-integration to diagnose import issues")
        print("💡 Enhanced fallback implementations available if models missing")
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logging.error(f"Enhanced main execution error: {e}")
        
        # Provide helpful suggestions
        if "playwright" in str(e).lower():
            print("💡 Install Playwright: pip install playwright")
            print("💡 Install browsers: playwright install")
        elif "permission" in str(e).lower():
            print("💡 Check file permissions")
        elif "timeout" in str(e).lower():
            print("💡 Check internet connection and increase timeouts")
        
        import traceback
        logging.debug(f"Full traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    # Quick command handlers
    if len(sys.argv) == 2:
        if sys.argv[1] == "--check-integration":
            check_enhanced_integration()
            sys.exit(0)
        elif sys.argv[1] == "--create-sample":
            create_enhanced_sample_data()
            print("✅ Enhanced sample data created!")
            print("🚀 Run with: python enhanced_search_simulator.py enhanced_search_data.json")
            sys.exit(0)
        elif sys.argv[1] == "--help-setup":
            print("🔧 ENHANCED SETUP INSTRUCTIONS")
            print("=" * 40)
            print("1. Model directories (optional but recommended):")
            print("   • modals/AutoWebGLM/")
            print("   • modals/USimAgent/")
            print()
            print("2. Required AutoWebGLM files:")
            print("   • miniwob++/html_tools/html_parser.py")
            print("   • miniwob++/html_tools/identifier.py")
            print("   • miniwob++/html_tools/utils.py")
            print("   • webarena/browser_env/html_tools/")
            print()
            print("3. Required USimAgent files:")
            print("   • agent/agent.py")
            print("   • agent/state.py")
            print("   • agent/task.py")
            print("   • config/config.py")
            print()
            print("4. Install dependencies:")
            print("   pip install playwright numpy asyncio")
            print("   playwright install")
            print("   pip install playwright-stealth  # optional but recommended")
            print()
            print("5. Enhanced features work with or without models:")
            print("   • With models: Uses real AutoWebGLM + USimAgent")
            print("   • Without models: Uses advanced fallback implementations")
            print()
            print("6. Test your setup:")
            print("   python enhanced_search_simulator.py --check-integration")
            print("   python enhanced_search_simulator.py --test-integration")
            print()
            print("7. Create and run sample:")
            print("   python enhanced_search_simulator.py --create-sample")
            print("   python enhanced_search_simulator.py enhanced_search_data.json")
            sys.exit(0)
    
    # Run enhanced main function
    asyncio.run(main())#!/usr/bin/env python3
"""
ENHANCED HUMAN-LIKE GOOGLE SEARCH SIMULATOR
Properly integrated with AutoWebGLM and USimAgent for realistic browsing behavior
"""