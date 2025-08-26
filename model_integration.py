#model_integration.py
"""
MODEL INTEGRATION MODULE
Handles AutoWebGLM and USimAgent integration with enhanced fallback implementations
"""

import sys
import logging
import time
import random
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional, Union

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
        
        UserPersonaType.PROFESSIONAL: UserPersona(
            persona_type=UserPersonaType.PROFESSIONAL,
            name="Business Pro",
            age_range=(28, 55),
            device_preferences=["laptop", "desktop", "mobile"],
            browsing_speed="medium",
            attention_span="medium",
            tech_comfort="high",
            reading_pattern="focused",
            social_media_usage="low",
            online_shopping_frequency="medium",
            search_query_style="specific",
            multitasking_tendency="high",
            privacy_consciousness="medium",
            click_through_rate=0.7,
            bounce_rate=0.3,
            scroll_depth_preference=0.7,
            form_completion_rate=0.8,
            social_sharing_likelihood=0.2,
            ad_interaction_rate=0.1,
            link_hover_tendency=0.7,
            page_exploration_time=0.6,
            session_duration_range=(180, 600),
            page_dwell_time_range=(30, 120),
            search_refinement_likelihood=0.5,
            back_button_usage=0.4,
            new_tab_usage=0.8,
            hover_duration_range=(1.5, 4),
            scroll_pause_frequency=0.5
        ),
        
        UserPersonaType.STUDENT: UserPersona(
            persona_type=UserPersonaType.STUDENT,
            name="Student Learner",
            age_range=(16, 28),
            device_preferences=["laptop", "mobile", "desktop"],
            browsing_speed="medium",
            attention_span="medium",
            tech_comfort="high",
            reading_pattern="thorough",
            social_media_usage="high",
            online_shopping_frequency="low",
            search_query_style="exploratory",
            multitasking_tendency="high",
            privacy_consciousness="low",
            click_through_rate=0.8,
            bounce_rate=0.3,
            scroll_depth_preference=0.8,
            form_completion_rate=0.6,
            social_sharing_likelihood=0.6,
            ad_interaction_rate=0.2,
            link_hover_tendency=0.8,
            page_exploration_time=0.7,
            session_duration_range=(240, 720),
            page_dwell_time_range=(45, 150),
            search_refinement_likelihood=0.6,
            back_button_usage=0.6,
            new_tab_usage=0.9,
            hover_duration_range=(2, 5),
            scroll_pause_frequency=0.6
        ),
        
        UserPersonaType.SENIOR: UserPersona(
            persona_type=UserPersonaType.SENIOR,
            name="Senior User",
            age_range=(55, 80),
            device_preferences=["desktop", "laptop"],
            browsing_speed="slow",
            attention_span="long",
            tech_comfort="low",
            reading_pattern="thorough",
            social_media_usage="low",
            online_shopping_frequency="low",
            search_query_style="simple",
            multitasking_tendency="low",
            privacy_consciousness="high",
            click_through_rate=0.5,
            bounce_rate=0.4,
            scroll_depth_preference=0.6,
            form_completion_rate=0.4,
            social_sharing_likelihood=0.1,
            ad_interaction_rate=0.1,
            link_hover_tendency=0.7,
            page_exploration_time=0.9,
            session_duration_range=(300, 1200),
            page_dwell_time_range=(90, 300),
            search_refinement_likelihood=0.3,
            back_button_usage=0.8,
            new_tab_usage=0.2,
            hover_duration_range=(3, 8),
            scroll_pause_frequency=0.8
        ),
        
        UserPersonaType.BARGAIN_HUNTER: UserPersona(
            persona_type=UserPersonaType.BARGAIN_HUNTER,
            name="Deal Seeker",
            age_range=(25, 55),
            device_preferences=["mobile", "desktop", "laptop"],
            browsing_speed="fast",
            attention_span="short",
            tech_comfort="medium",
            reading_pattern="scanner",
            social_media_usage="medium",
            online_shopping_frequency="high",
            search_query_style="specific",
            multitasking_tendency="high",
            privacy_consciousness="low",
            click_through_rate=0.9,
            bounce_rate=0.6,
            scroll_depth_preference=0.4,
            form_completion_rate=0.6,
            social_sharing_likelihood=0.5,
            ad_interaction_rate=0.4,
            link_hover_tendency=0.5,
            page_exploration_time=0.3,
            session_duration_range=(60, 240),
            page_dwell_time_range=(20, 60),
            search_refinement_likelihood=0.8,
            back_button_usage=0.9,
            new_tab_usage=0.8,
            hover_duration_range=(0.5, 2),
            scroll_pause_frequency=0.3
        )
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
# MODEL INTEGRATION CLASSES
# ============================================================================

class ModelIntegration:
    """Main model integration manager"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.models_available = MODELS_AVAILABLE
        self.component_status = self._check_component_availability()
        
        if self.models_available:
            logging.info("✅ Using real AutoWebGLM and USimAgent integration")
        else:
            logging.info("🔄 Using enhanced fallback implementations")
    
    def _check_component_availability(self) -> Dict[str, bool]:
        """Check availability of individual model components"""
        
        status = {}
        
        # Check AutoWebGLM components
        try:
            from html_tools.html_parser import HTMLParser
            status["AutoWebGLM HTML Parser"] = True
        except ImportError:
            status["AutoWebGLM HTML Parser"] = False
        
        try:
            from html_tools.identifier import ElementIdentifier
            status["AutoWebGLM Element Identifier"] = True
        except ImportError:
            status["AutoWebGLM Element Identifier"] = False
        
        # Check USimAgent components
        try:
            from agent.agent import Agent
            status["USimAgent Agent"] = True
        except ImportError:
            status["USimAgent Agent"] = False
        
        try:
            from agent.state import State
            status["USimAgent State"] = True
        except ImportError:
            status["USimAgent State"] = False
        
        try:
            from config.config import Config
            status["USimAgent Config"] = True
        except ImportError:
            status["USimAgent Config"] = False
        
        return status
    
    def create_autowebglm(self, persona: UserPersona):
        """Create AutoWebGLM instance"""
        return EnhancedAutoWebGLM(persona, self.config)
    
    def create_usimagent(self, persona: UserPersona):
        """Create USimAgent instance"""
        return EnhancedUSimAgent(persona, self.config)

class EnhancedAutoWebGLM:
    """Enhanced AutoWebGLM integration with better page analysis"""
    
    def __init__(self, persona: UserPersona, config: Dict = None):
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
    
    def __init__(self, persona: UserPersona, config: Dict = None):
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
        elif self.persona.persona_type == UserPersonaType.BARGAIN_HUNTER:
            return 0.9
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
            "generated_by": "enhanced_fallback" if not MODELS_AVAILABLE else "real_agent_fallback",
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
        if self.session_actions:
            session_duration = time.time() - self.session_actions[0]["timestamp"]
            max_duration = self.persona.session_duration_range[1]
            
            if session_duration > max_duration:
                continue_prob -= 0.3
        
        return random.random() < max(0.1, min(0.9, continue_prob))
    
    def get_final_state(self) -> Dict[str, Any]:
        """Get final cognitive state"""
        return {
            "cognitive_load": self.cognitive_load,
            "fatigue_level": self.fatigue_level,
            "interest_level": self.interest_level,
            "emotional_state": self.emotional_state,
            "total_actions": len(self.session_actions),
            "exploration_satisfaction": self.exploration_satisfaction,
            "working_memory_capacity": getattr(self, 'working_memory_capacity', 5),
            "attention_decay_rate": getattr(self, 'attention_decay_rate', 0.03),
            "decision_speed": getattr(self, 'decision_speed', 1.0),
            "exploration_tendency": getattr(self, 'exploration_tendency', 0.6)
        }
    
    def reset_cognitive_state(self):
        """Reset cognitive state for new session"""
        self.cognitive_load = 0.0
        self.fatigue_level = 0.0
        self.interest_level = 1.0
        self.session_actions = []
        self.emotional_state = "neutral"
        self.exploration_satisfaction = 0.5
        self.last_action_time = time.time()
    
    def update_emotional_state(self, new_state: str):
        """Update emotional state"""
        valid_states = ["neutral", "interested", "bored", "frustrated", "satisfied", "confused"]
        if new_state in valid_states:
            self.emotional_state = new_state
            
            # Adjust other states based on emotion
            if new_state == "interested":
                self.interest_level = min(1.0, self.interest_level + 0.1)
            elif new_state == "bored":
                self.interest_level = max(0.1, self.interest_level - 0.2)
            elif new_state == "frustrated":
                self.cognitive_load = min(1.0, self.cognitive_load + 0.1)
                self.fatigue_level = min(1.0, self.fatigue_level + 0.1)
            elif new_state == "satisfied":
                self.exploration_satisfaction = min(1.0, self.exploration_satisfaction + 0.2)
    
    def get_action_history(self) -> List[Dict[str, Any]]:
        """Get action history"""
        return self.session_actions.copy()
    
    def calculate_session_metrics(self) -> Dict[str, Any]:
        """Calculate metrics for current session"""
        if not self.session_actions:
            return {}
        
        session_duration = time.time() - self.session_actions[0]["timestamp"]
        
        # Calculate average states
        avg_cognitive_load = sum(action["cognitive_load"] for action in self.session_actions) / len(self.session_actions)
        avg_fatigue = sum(action["fatigue"] for action in self.session_actions) / len(self.session_actions)
        avg_interest = sum(action["interest"] for action in self.session_actions) / len(self.session_actions)
        avg_confidence = sum(action["confidence"] for action in self.session_actions) / len(self.session_actions)
        
        # Count action types
        action_counts = {}
        for action in self.session_actions:
            action_type = action["action"]
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        return {
            "session_duration": session_duration,
            "total_actions": len(self.session_actions),
            "actions_per_minute": (len(self.session_actions) / (session_duration / 60)) if session_duration > 0 else 0,
            "average_states": {
                "cognitive_load": avg_cognitive_load,
                "fatigue_level": avg_fatigue,
                "interest_level": avg_interest,
                "confidence": avg_confidence
            },
            "action_distribution": action_counts,
            "final_state": {
                "cognitive_load": self.cognitive_load,
                "fatigue_level": self.fatigue_level,
                "interest_level": self.interest_level,
                "emotional_state": self.emotional_state,
                "exploration_satisfaction": self.exploration_satisfaction
            },
            "persona_type": self.persona.persona_type.value,
            "persona_name": self.persona.name
        }

# ============================================================================
# UTILITY FUNCTIONS FOR MODEL INTEGRATION
# ============================================================================

def check_model_availability() -> Dict[str, bool]:
    """Check availability of model components"""
    
    availability = {
        "models_base": MODELS_AVAILABLE,
        "autowebglm_html_parser": False,
        "autowebglm_identifier": False,
        "autowebglm_utils": False,
        "usimagent_agent": False,
        "usimagent_state": False,
        "usimagent_config": False
    }
    
    if MODELS_AVAILABLE:
        try:
            from html_tools.html_parser import HTMLParser
            availability["autowebglm_html_parser"] = True
        except ImportError:
            pass
        
        try:
            from html_tools.identifier import ElementIdentifier
            availability["autowebglm_identifier"] = True
        except ImportError:
            pass
        
        try:
            from html_tools.utils import extract_elements
            availability["autowebglm_utils"] = True
        except ImportError:
            pass
        
        try:
            from agent.agent import Agent
            availability["usimagent_agent"] = True
        except ImportError:
            pass
        
        try:
            from agent.state import State
            availability["usimagent_state"] = True
        except ImportError:
            pass
        
        try:
            from config.config import Config
            availability["usimagent_config"] = True
        except ImportError:
            pass
    
    return availability

def get_model_status_report() -> str:
    """Get detailed model status report"""
    
    availability = check_model_availability()
    
    report = ["MODEL INTEGRATION STATUS REPORT", "=" * 40, ""]
    
    if availability["models_base"]:
        report.append("✅ Base model integration: AVAILABLE")
        report.append("")
        report.append("AutoWebGLM Components:")
        report.append(f"  HTML Parser: {'✅ Available' if availability['autowebglm_html_parser'] else '❌ Missing'}")
        report.append(f"  Element Identifier: {'✅ Available' if availability['autowebglm_identifier'] else '❌ Missing'}")
        report.append(f"  Utils: {'✅ Available' if availability['autowebglm_utils'] else '❌ Missing'}")
        report.append("")
        report.append("USimAgent Components:")
        report.append(f"  Agent: {'✅ Available' if availability['usimagent_agent'] else '❌ Missing'}")
        report.append(f"  State: {'✅ Available' if availability['usimagent_state'] else '❌ Missing'}")
        report.append(f"  Config: {'✅ Available' if availability['usimagent_config'] else '❌ Missing'}")
    else:
        report.append("⚠️ Base model integration: NOT AVAILABLE")
        report.append("Using enhanced fallback implementations")
        report.append("")
        report.append("Features available in fallback mode:")
        report.append("  ✅ Enhanced page analysis")
        report.append("  ✅ Cognitive state modeling")
        report.append("  ✅ Human-like behavior generation")
        report.append("  ✅ Persona-based interactions")
    
    report.append("")
    report.append("Directory Structure:")
    
    modals_dir = Path("modals")
    autowebglm_dir = modals_dir / "AutoWebGLM"
    usimagent_dir = modals_dir / "USimAgent"
    
    report.append(f"  modals/: {'✅ Exists' if modals_dir.exists() else '❌ Missing'}")
    report.append(f"  modals/AutoWebGLM/: {'✅ Exists' if autowebglm_dir.exists() else '❌ Missing'}")
    report.append(f"  modals/USimAgent/: {'✅ Exists' if usimagent_dir.exists() else '❌ Missing'}")
    
    if autowebglm_dir.exists():
        miniwob_dir = autowebglm_dir / "miniwob++"
        webarena_dir = autowebglm_dir / "webarena"
        report.append(f"  AutoWebGLM/miniwob++/: {'✅ Exists' if miniwob_dir.exists() else '❌ Missing'}")
        report.append(f"  AutoWebGLM/webarena/: {'✅ Exists' if webarena_dir.exists() else '❌ Missing'}")
    
    if usimagent_dir.exists():
        agent_dir = usimagent_dir / "agent"
        config_dir = usimagent_dir / "config"
        report.append(f"  USimAgent/agent/: {'✅ Exists' if agent_dir.exists() else '❌ Missing'}")
        report.append(f"  USimAgent/config/: {'✅ Exists' if config_dir.exists() else '❌ Missing'}")
    
    return "\n".join(report)

def initialize_models(config: Dict = None) -> ModelIntegration:
    """Initialize model integration with configuration"""
    
    return ModelIntegration(config)

def create_test_persona() -> UserPersona:
    """Create a test persona for development"""
    
    return UserPersona(
        persona_type=UserPersonaType.TECH_SAVVY,
        name="Test User",
        age_range=(25, 35),
        device_preferences=["desktop"],
        browsing_speed="medium",
        attention_span="medium",
        tech_comfort="high",
        reading_pattern="scanner",
        social_media_usage="medium",
        online_shopping_frequency="medium",
        search_query_style="precise",
        multitasking_tendency="medium",
        privacy_consciousness="medium",
        click_through_rate=0.7,
        bounce_rate=0.3,
        scroll_depth_preference=0.6,
        form_completion_rate=0.7,
        social_sharing_likelihood=0.4,
        ad_interaction_rate=0.2,
        link_hover_tendency=0.8,
        page_exploration_time=0.6,
        session_duration_range=(120, 300),
        page_dwell_time_range=(30, 90),
        search_refinement_likelihood=0.5,
        back_button_usage=0.4,
        new_tab_usage=0.7,
        hover_duration_range=(1, 3),
        scroll_pause_frequency=0.5
    )