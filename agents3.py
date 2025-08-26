#!/usr/bin/env python3
"""
ENHANCED GOOGLE SEARCH SIMULATOR - INTEGRATED WITH USIMAGENT AND AUTOWEBGLM
Prevents pattern detection through diverse, AI-driven browsing behaviors
"""

import asyncio
import random
import time
import json
import logging
import argparse
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from urllib.parse import urlparse
from playwright.async_api import async_playwright
import sys
import os
import numpy as np
from dataclasses import dataclass
from enum import Enum
import re

# ============================================================================
# ENHANCED USER PERSONA SYSTEM
# ============================================================================

class UserPersonaType(Enum):
    RESEARCHER = "researcher"
    CASUAL_BROWSER = "casual_browser"
    PROFESSIONAL = "professional"
    STUDENT = "student"
    SENIOR = "senior"
    MOBILE_FIRST = "mobile_first"
    TECH_SAVVY = "tech_savvy"
    BARGAIN_HUNTER = "bargain_hunter"

@dataclass
class UserPersona:
    """Extended user persona with detailed behavioral patterns"""
    persona_type: UserPersonaType
    name: str
    age_range: tuple
    device_preferences: List[str]
    browsing_speed: str  # slow, medium, fast
    attention_span: str  # short, medium, long
    tech_comfort: str   # low, medium, high
    reading_pattern: str # skimmer, normal, thorough
    social_media_usage: str # low, medium, high
    online_shopping_frequency: str
    search_query_style: str # brief, detailed, conversational
    multitasking_tendency: str # low, medium, high
    privacy_consciousness: str # low, medium, high
    
    # Behavioral weights (0.0 to 1.0)
    click_through_rate: float
    bounce_rate: float
    scroll_depth_preference: float
    form_completion_rate: float
    social_sharing_likelihood: float
    ad_interaction_rate: float
    
    # Timing patterns
    session_duration_range: tuple  # min, max seconds
    page_dwell_time_range: tuple
    search_refinement_likelihood: float
    back_button_usage: float
    new_tab_usage: float

class PersonaManager:
    """Manages different user personas and their behaviors"""
    
    PERSONAS = {
        UserPersonaType.RESEARCHER: UserPersona(
            persona_type=UserPersonaType.RESEARCHER,
            name="Dr. Academic",
            age_range=(25, 65),
            device_preferences=["desktop", "laptop"],
            browsing_speed="medium",
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
            session_duration_range=(180, 600),
            page_dwell_time_range=(45, 120),
            search_refinement_likelihood=0.7,
            back_button_usage=0.4,
            new_tab_usage=0.8
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
            session_duration_range=(30, 180),
            page_dwell_time_range=(10, 45),
            search_refinement_likelihood=0.3,
            back_button_usage=0.7,
            new_tab_usage=0.5
        ),
        
        UserPersonaType.PROFESSIONAL: UserPersona(
            persona_type=UserPersonaType.PROFESSIONAL,
            name="Business Professional",
            age_range=(25, 55),
            device_preferences=["desktop", "laptop", "mobile"],
            browsing_speed="medium",
            attention_span="medium",
            tech_comfort="high",
            reading_pattern="normal",
            social_media_usage="medium",
            online_shopping_frequency="medium",
            search_query_style="detailed",
            multitasking_tendency="high",
            privacy_consciousness="medium",
            click_through_rate=0.7,
            bounce_rate=0.3,
            scroll_depth_preference=0.7,
            form_completion_rate=0.8,
            social_sharing_likelihood=0.4,
            ad_interaction_rate=0.2,
            session_duration_range=(90, 300),
            page_dwell_time_range=(30, 90),
            search_refinement_likelihood=0.5,
            back_button_usage=0.5,
            new_tab_usage=0.6
        ),
        
        UserPersonaType.STUDENT: UserPersona(
            persona_type=UserPersonaType.STUDENT,
            name="College Student",
            age_range=(18, 25),
            device_preferences=["laptop", "mobile", "tablet"],
            browsing_speed="fast",
            attention_span="medium",
            tech_comfort="high",
            reading_pattern="normal",
            social_media_usage="high",
            online_shopping_frequency="low",
            search_query_style="conversational",
            multitasking_tendency="high",
            privacy_consciousness="medium",
            click_through_rate=0.65,
            bounce_rate=0.35,
            scroll_depth_preference=0.6,
            form_completion_rate=0.5,
            social_sharing_likelihood=0.8,
            ad_interaction_rate=0.25,
            session_duration_range=(60, 240),
            page_dwell_time_range=(20, 70),
            search_refinement_likelihood=0.6,
            back_button_usage=0.6,
            new_tab_usage=0.9
        ),
        
        UserPersonaType.SENIOR: UserPersona(
            persona_type=UserPersonaType.SENIOR,
            name="Senior Citizen",
            age_range=(55, 80),
            device_preferences=["desktop", "tablet"],
            browsing_speed="slow",
            attention_span="long",
            tech_comfort="low",
            reading_pattern="thorough",
            social_media_usage="low",
            online_shopping_frequency="low",
            search_query_style="detailed",
            multitasking_tendency="low",
            privacy_consciousness="high",
            click_through_rate=0.5,
            bounce_rate=0.5,
            scroll_depth_preference=0.8,
            form_completion_rate=0.4,
            social_sharing_likelihood=0.2,
            ad_interaction_rate=0.4,
            session_duration_range=(120, 480),
            page_dwell_time_range=(60, 180),
            search_refinement_likelihood=0.4,
            back_button_usage=0.8,
            new_tab_usage=0.2
        ),
        
        UserPersonaType.BARGAIN_HUNTER: UserPersona(
            persona_type=UserPersonaType.BARGAIN_HUNTER,
            name="Deal Seeker",
            age_range=(25, 50),
            device_preferences=["mobile", "desktop", "tablet"],
            browsing_speed="medium",
            attention_span="medium",
            tech_comfort="medium",
            reading_pattern="normal",
            social_media_usage="medium",
            online_shopping_frequency="high",
            search_query_style="brief",
            multitasking_tendency="medium",
            privacy_consciousness="low",
            click_through_rate=0.75,
            bounce_rate=0.25,
            scroll_depth_preference=0.65,
            form_completion_rate=0.6,
            social_sharing_likelihood=0.5,
            ad_interaction_rate=0.4,
            session_duration_range=(90, 360),
            page_dwell_time_range=(25, 80),
            search_refinement_likelihood=0.8,
            back_button_usage=0.6,
            new_tab_usage=0.7
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
# USIMAGENT INTEGRATION - HUMAN SIMULATION PATTERNS
# ============================================================================

class USimAgent:
    """
    USimAgent integration for realistic user simulation
    Mimics human cognitive patterns and decision-making
    """
    
    def __init__(self, persona: UserPersona):
        self.persona = persona
        self.cognitive_load = 0.0
        self.fatigue_level = 0.0
        self.interest_level = 1.0
        self.session_goals = []
        self.completed_actions = []
        self.emotional_state = "neutral"  # neutral, frustrated, excited, bored
        
        # Cognitive patterns
        self.working_memory_capacity = self._calculate_working_memory()
        self.attention_decay_rate = self._calculate_attention_decay()
        self.decision_making_speed = self._calculate_decision_speed()
        
    def _calculate_working_memory(self) -> int:
        """Calculate working memory capacity based on persona"""
        base_capacity = {
            "low": 3, "medium": 5, "high": 7
        }
        return base_capacity[self.persona.tech_comfort] + random.randint(-1, 1)
    
    def _calculate_attention_decay(self) -> float:
        """Calculate how quickly attention decays"""
        attention_map = {
            "short": 0.05, "medium": 0.03, "long": 0.01
        }
        return attention_map[self.persona.attention_span]
    
    def _calculate_decision_speed(self) -> float:
        """Calculate decision making speed multiplier"""
        speed_map = {
            "slow": 1.5, "medium": 1.0, "fast": 0.7
        }
        return speed_map[self.persona.browsing_speed]
    
    def update_cognitive_state(self, action_complexity: float, time_spent: float):
        """Update cognitive state based on actions performed"""
        # Increase cognitive load
        self.cognitive_load += action_complexity * 0.1
        self.cognitive_load = min(1.0, self.cognitive_load)
        
        # Increase fatigue over time
        self.fatigue_level += time_spent * 0.001
        self.fatigue_level = min(1.0, self.fatigue_level)
        
        # Decay interest over time
        self.interest_level -= self.attention_decay_rate * time_spent
        self.interest_level = max(0.1, self.interest_level)
        
        # Update emotional state
        self._update_emotional_state()
    
    def _update_emotional_state(self):
        """Update emotional state based on cognitive factors"""
        if self.fatigue_level > 0.7:
            self.emotional_state = "frustrated"
        elif self.cognitive_load > 0.8:
            self.emotional_state = "overwhelmed"
        elif self.interest_level < 0.3:
            self.emotional_state = "bored"
        elif self.interest_level > 0.8 and self.cognitive_load < 0.4:
            self.emotional_state = "engaged"
        else:
            self.emotional_state = "neutral"
    
    def should_continue_browsing(self) -> bool:
        """Decide whether to continue browsing based on cognitive state"""
        continue_probability = (
            self.interest_level * 0.4 +
            (1 - self.fatigue_level) * 0.3 +
            (1 - self.cognitive_load) * 0.3
        )
        
        # Adjust for persona characteristics
        if self.persona.attention_span == "long":
            continue_probability += 0.1
        elif self.persona.attention_span == "short":
            continue_probability -= 0.1
            
        return random.random() < continue_probability
    
    def get_action_timing_modifier(self) -> float:
        """Get timing modifier based on current cognitive state"""
        base_modifier = self.decision_making_speed
        
        # Slower when fatigued or overloaded
        fatigue_modifier = 1 + (self.fatigue_level * 0.5)
        cognitive_modifier = 1 + (self.cognitive_load * 0.3)
        
        # Faster when highly interested
        interest_modifier = 1 - (self.interest_level * 0.2)
        
        return base_modifier * fatigue_modifier * cognitive_modifier * interest_modifier
    
    def get_click_probability(self, element_relevance: float) -> float:
        """Calculate click probability based on cognitive state and element relevance"""
        base_probability = self.persona.click_through_rate
        
        # Adjust for cognitive state
        interest_bonus = self.interest_level * 0.2
        fatigue_penalty = self.fatigue_level * 0.1
        
        # Adjust for element relevance
        relevance_bonus = element_relevance * 0.3
        
        final_probability = base_probability + interest_bonus - fatigue_penalty + relevance_bonus
        return max(0.05, min(0.95, final_probability))
    
    def generate_search_refinement(self, original_query: str, results_satisfaction: float) -> Optional[str]:
        """Generate search refinement based on cognitive patterns"""
        if random.random() > self.persona.search_refinement_likelihood:
            return None
        
        if results_satisfaction > 0.7:
            return None  # Satisfied with results
        
        # Generate refinement based on persona and satisfaction
        refinement_strategies = {
            "add_specificity": lambda q: f"{q} {random.choice(['guide', 'tutorial', 'how to', 'best', 'review'])}",
            "add_context": lambda q: f"{q} {random.choice(['2024', 'latest', 'new', 'updated'])}",
            "broaden_search": lambda q: re.sub(r'\b\w+\b', random.choice(['alternative', 'similar', 'related']), q, count=1),
            "add_qualifier": lambda q: f"{random.choice(['cheap', 'free', 'professional', 'beginner'])} {q}"
        }
        
        strategy = random.choice(list(refinement_strategies.keys()))
        return refinement_strategies[strategy](original_query)

# ============================================================================
# AUTOWEBGLM INTEGRATION - INTELLIGENT WEB AUTOMATION
# ============================================================================

class AutoWebGLM:
    """
    AutoWebGLM integration for intelligent web automation
    Provides context-aware, goal-driven browsing behavior
    """
    
    def __init__(self, persona: UserPersona):
        self.persona = persona
        self.current_goal = None
        self.page_context = {}
        self.navigation_history = []
        self.learned_patterns = {}
        
    async def analyze_page_context(self, page) -> Dict[str, Any]:
        """Analyze page context using AutoWebGLM patterns"""
        try:
            context = {
                "page_type": await self._classify_page_type(page),
                "content_density": await self._analyze_content_density(page),
                "interactive_elements": await self._catalog_interactive_elements(page),
                "visual_hierarchy": await self._analyze_visual_hierarchy(page),
                "semantic_content": await self._extract_semantic_content(page),
                "user_flow_indicators": await self._detect_user_flow_indicators(page),
                "trust_signals": await self._evaluate_trust_signals(page)
            }
            
            self.page_context = context
            return context
            
        except Exception as e:
            logging.debug(f"Page context analysis failed: {e}")
            return {"page_type": "unknown", "content_density": "medium"}
    
    async def _classify_page_type(self, page) -> str:
        """Classify the type of page"""
        try:
            title = await page.title()
            url = page.url
            
            # Get page structure indicators
            has_nav = await page.locator("nav, .navigation, .navbar").count() > 0
            has_main_content = await page.locator("main, .main-content, .content").count() > 0
            has_sidebar = await page.locator(".sidebar, .side-nav, aside").count() > 0
            has_forms = await page.locator("form").count() > 0
            has_products = await page.locator(".product, .item, .listing").count() > 5
            has_articles = await page.locator("article, .post, .blog-post").count() > 0
            
            # Classification logic
            if "search" in url.lower() or "results" in url.lower():
                return "search_results"
            elif has_products and ("shop" in url.lower() or "store" in url.lower()):
                return "ecommerce"
            elif has_articles or "blog" in url.lower():
                return "content/blog"
            elif has_forms and ("contact" in url.lower() or "form" in url.lower()):
                return "contact/form"
            elif "about" in url.lower():
                return "about"
            elif url.count('/') <= 3:
                return "homepage"
            else:
                return "content_page"
                
        except:
            return "unknown"
    
    async def _analyze_content_density(self, page) -> str:
        """Analyze content density of the page"""
        try:
            text_length = len(await page.inner_text("body"))
            link_count = await page.locator("a").count()
            image_count = await page.locator("img").count()
            
            if text_length > 5000 and link_count > 20:
                return "high"
            elif text_length > 2000 and link_count > 10:
                return "medium"
            else:
                return "low"
        except:
            return "medium"
    
    async def _catalog_interactive_elements(self, page) -> Dict[str, int]:
        """Catalog interactive elements on the page"""
        try:
            elements = {
                "buttons": await page.locator("button, .btn, input[type='button'], input[type='submit']").count(),
                "links": await page.locator("a[href]").count(),
                "form_fields": await page.locator("input, textarea, select").count(),
                "dropdown_menus": await page.locator(".dropdown, select").count(),
                "tabs": await page.locator(".tab, [role='tab']").count(),
                "modals": await page.locator(".modal, .popup, .overlay").count(),
                "carousels": await page.locator(".carousel, .slider, .swiper").count(),
                "accordions": await page.locator(".accordion, .collapsible").count()
            }
            return elements
        except:
            return {"buttons": 0, "links": 0, "form_fields": 0}
    
    async def _analyze_visual_hierarchy(self, page) -> Dict[str, Any]:
        """Analyze visual hierarchy of the page"""
        try:
            hierarchy = {
                "has_clear_header": await page.locator("header, .header").count() > 0,
                "has_clear_footer": await page.locator("footer, .footer").count() > 0,
                "heading_structure": {
                    "h1": await page.locator("h1").count(),
                    "h2": await page.locator("h2").count(),
                    "h3": await page.locator("h3").count()
                },
                "has_breadcrumbs": await page.locator(".breadcrumb, .breadcrumbs, nav[aria-label*='breadcrumb']").count() > 0,
                "has_cta_buttons": await page.locator(".cta, .call-to-action, .btn-primary").count() > 0
            }
            return hierarchy
        except:
            return {"has_clear_header": False, "has_clear_footer": False}
    
    async def _extract_semantic_content(self, page) -> Dict[str, Any]:
        """Extract semantic content information"""
        try:
            content = {
                "main_topics": [],
                "keywords": [],
                "content_length": 0,
                "reading_time": 0
            }
            
            # Extract main text content
            main_text = await page.inner_text("main, .main-content, .content, article, .post")
            if not main_text:
                main_text = await page.inner_text("body")
            
            content["content_length"] = len(main_text)
            content["reading_time"] = max(1, len(main_text.split()) / 200)  # Assume 200 WPM
            
            # Extract keywords from headings and prominent text
            headings = await page.locator("h1, h2, h3").all_inner_texts()
            content["main_topics"] = [h.strip()[:50] for h in headings if h.strip()][:5]
            
            return content
        except:
            return {"main_topics": [], "keywords": [], "content_length": 0, "reading_time": 1}
    
    async def _detect_user_flow_indicators(self, page) -> Dict[str, bool]:
        """Detect indicators of user flow and navigation patterns"""
        try:
            indicators = {
                "has_search_bar": await page.locator("input[type='search'], .search-input, #search").count() > 0,
                "has_filters": await page.locator(".filter, .filters, .facet").count() > 0,
                "has_pagination": await page.locator(".pagination, .pager, .page-nav").count() > 0,
                "has_recommendations": await page.locator(".recommended, .suggested, .related").count() > 0,
                "has_social_sharing": await page.locator(".share, .social-share, .social-buttons").count() > 0,
                "has_comments": await page.locator(".comments, .comment-section, #comments").count() > 0,
                "has_newsletter_signup": await page.locator("input[type='email'], .newsletter, .subscribe").count() > 0,
                "has_chat_widget": await page.locator(".chat, .live-chat, .support-chat").count() > 0
            }
            return indicators
        except:
            return {}
    
    async def _evaluate_trust_signals(self, page) -> Dict[str, Any]:
        """Evaluate trust signals on the page"""
        try:
            trust_signals = {
                "has_contact_info": await page.locator(".contact, .phone, .email, .address").count() > 0,
                "has_testimonials": await page.locator(".testimonial, .review, .rating").count() > 0,
                "has_security_badges": await page.locator(".secure, .ssl, .verified, .trust").count() > 0,
                "has_company_info": await page.locator(".about, .company-info, .team").count() > 0,
                "professional_design": True,  # Could be enhanced with ML
                "loading_speed": "normal"  # Could be measured
            }
            return trust_signals
        except:
            return {"professional_design": True}
    
    def generate_intelligent_navigation_plan(self, goal: str, page_context: Dict) -> List[Dict[str, Any]]:
        """Generate intelligent navigation plan based on goal and context"""
        plans = {
            "information_seeking": self._plan_information_seeking,
            "product_research": self._plan_product_research,
            "service_evaluation": self._plan_service_evaluation,
            "entertainment": self._plan_entertainment_browsing,
            "comparison_shopping": self._plan_comparison_shopping
        }
        
        # Determine goal type
        goal_type = self._classify_goal(goal)
        planner = plans.get(goal_type, self._plan_general_browsing)
        
        return planner(page_context)
    
    def _classify_goal(self, goal: str) -> str:
        """Classify the user's goal"""
        goal_lower = goal.lower()
        
        if any(word in goal_lower for word in ["learn", "information", "research", "understand", "guide"]):
            return "information_seeking"
        elif any(word in goal_lower for word in ["buy", "purchase", "product", "price", "review"]):
            return "product_research"
        elif any(word in goal_lower for word in ["service", "company", "business", "hire", "contact"]):
            return "service_evaluation"
        elif any(word in goal_lower for word in ["entertainment", "fun", "game", "video", "music"]):
            return "entertainment"
        elif any(word in goal_lower for word in ["compare", "vs", "versus", "best", "alternative"]):
            return "comparison_shopping"
        else:
            return "general_browsing"
    
    def _plan_information_seeking(self, context: Dict) -> List[Dict[str, Any]]:
        """Plan for information seeking behavior"""
        actions = []
        
        # Focus on content consumption
        if context.get("content_density") == "high":
            actions.extend([
                {"action": "deep_read", "duration": (60, 180), "priority": "high"},
                {"action": "bookmark_consideration", "probability": 0.7},
                {"action": "scroll_thoroughly", "depth": 0.8}
            ])
        
        # Look for related content
        if context.get("user_flow_indicators", {}).get("has_recommendations"):
            actions.append({"action": "explore_recommendations", "probability": 0.6})
        
        return actions
    
    def _plan_product_research(self, context: Dict) -> List[Dict[str, Any]]:
        """Plan for product research behavior"""
        actions = [
            {"action": "scan_reviews", "priority": "high"},
            {"action": "check_pricing", "priority": "high"},
            {"action": "compare_options", "probability": 0.8}
        ]
        
        if context.get("interactive_elements", {}).get("tabs", 0) > 0:
            actions.append({"action": "explore_tabs", "probability": 0.9})
        
        return actions
    
    def _plan_service_evaluation(self, context: Dict) -> List[Dict[str, Any]]:
        """Plan for service evaluation behavior"""
        actions = [
            {"action": "read_about_section", "priority": "medium"},
            {"action": "check_contact_info", "priority": "high"},
            {"action": "evaluate_trust_signals", "priority": "medium"}
        ]
        
        if context.get("trust_signals", {}).get("has_testimonials"):
            actions.append({"action": "read_testimonials", "priority": "high"})
        
        return actions
    
    def _plan_entertainment_browsing(self, context: Dict) -> List[Dict[str, Any]]:
        """Plan for entertainment browsing behavior"""
        return [
            {"action": "casual_browsing", "duration": (30, 120)},
            {"action": "social_sharing_check", "probability": 0.4},
            {"action": "quick_navigation", "speed_multiplier": 1.3}
        ]
    
    def _plan_comparison_shopping(self, context: Dict) -> List[Dict[str, Any]]:
        """Plan for comparison shopping behavior"""
        return [
            {"action": "detailed_comparison", "duration": (90, 240)},
            {"action": "open_multiple_tabs", "probability": 0.8},
            {"action": "price_focus", "priority": "high"},
            {"action": "feature_comparison", "priority": "medium"}
        ]
    
    def _plan_general_browsing(self, context: Dict) -> List[Dict[str, Any]]:
        """Default general browsing plan"""
        return [
            {"action": "general_exploration", "duration": (45, 150)},
            {"action": "adaptive_navigation", "probability": 0.5}
        ]

# ============================================================================
# ENHANCED GOOGLE SEARCH SIMULATOR WITH AI INTEGRATION
# ============================================================================

class EnhancedGoogleSearchSimulator:
    """
    Enhanced Google Search Simulator with USimAgent and AutoWebGLM integration
    """
    
    def __init__(self):
        self.session_data = []
        self.current_persona = None
        self.usim_agent = None
        self.autowebglm = None
        self.session_goals = []
        
        # Pattern variation tracking
        self.used_patterns = []
        self.pattern_weights = self._initialize_pattern_weights()
        
    def _initialize_pattern_weights(self) -> Dict[str, float]:
        """Initialize weights for different behavioral patterns"""
        return {
            "scroll_patterns": {"linear": 0.3, "jump_scroll": 0.2, "careful_read": 0.3, "speed_scan": 0.2},
            "click_patterns": {"immediate": 0.25, "hover_first": 0.4, "hesitant": 0.25, "precision": 0.1},
            "timing_patterns": {"steady": 0.3, "variable": 0.4, "burst": 0.2, "contemplative": 0.1},
            "navigation_patterns": {"linear": 0.3, "exploratory": 0.4, "goal_directed": 0.3}
        }
    
    def select_diverse_pattern(self, pattern_type: str) -> str:
        """Select pattern while ensuring diversity"""
        available_patterns = self.pattern_weights.get(pattern_type, {})
        
        # Reduce weight of recently used patterns
        for used_pattern in self.used_patterns[-10:]:  # Last 10 patterns
            if used_pattern in available_patterns:
                available_patterns[used_pattern] *= 0.5
        
        # Weighted random selection
        patterns = list(available_patterns.keys())
        weights = list(available_patterns.values())
        
        selected_pattern = random.choices(patterns, weights=weights)[0]
        self.used_patterns.append(selected_pattern)
        
        # Reset weights periodically
        if len(self.used_patterns) > 50:
            self.pattern_weights = self._initialize_pattern_weights()
            self.used_patterns = self.used_patterns[-20:]  # Keep last 20
        
        return selected_pattern
    
    async def create_realistic_browser_with_persona(self, persona: UserPersona):
        """Create browser with persona-specific configuration"""
        
        try:
            from playwright_stealth import stealth_async
            stealth_available = True
        except ImportError:
            stealth_available = False
            logging.warning("playwright-stealth not available")
        
        playwright = await async_playwright().start()
        
        # Persona-specific browser configurations
        device_configs = {
            "desktop": [
                {"viewport": {"width": 1920, "height": 1080}, "device_scale_factor": 1},
                {"viewport": {"width": 1366, "height": 768}, "device_scale_factor": 1},
                {"viewport": {"width": 1440, "height": 900}, "device_scale_factor": 1},
                {"viewport": {"width": 2560, "height": 1440}, "device_scale_factor": 1}
            ],
            "laptop": [
                {"viewport": {"width": 1366, "height": 768}, "device_scale_factor": 1},
                {"viewport": {"width": 1440, "height": 900}, "device_scale_factor": 1},
                {"viewport": {"width": 1536, "height": 864}, "device_scale_factor": 1.25}
            ],
            "mobile": [
                {"viewport": {"width": 375, "height": 667}, "device_scale_factor": 2},
                {"viewport": {"width": 414, "height": 896}, "device_scale_factor": 3},
                {"viewport": {"width": 360, "height": 640}, "device_scale_factor": 3}
            ],
            "tablet": [
                {"viewport": {"width": 768, "height": 1024}, "device_scale_factor": 2},
                {"viewport": {"width": 834, "height": 1112}, "device_scale_factor": 2},
                {"viewport": {"width": 1024, "height": 768}, "device_scale_factor": 2}
            ]
        }
        
        # Select device based on persona preferences
        preferred_device = random.choice(persona.device_preferences)
        config = random.choice(device_configs[preferred_device])
        
        # Generate realistic user agent based on device and persona
        user_agent = self._generate_persona_user_agent(persona, preferred_device)
        
        # Persona-specific browser args
        browser_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-automation',
            '--no-sandbox',
            '--disable-extensions',
            '--disable-dev-shm-usage'
        ]
        
        # Privacy-conscious users might have ad blockers
        if persona.privacy_consciousness == "high":
            browser_args.extend([
                '--disable-background-networking',
                '--disable-background-timer-throttling',
                '--disable-client-side-phishing-detection'
            ])
        
        browser = await playwright.chromium.launch(
            headless=False,  # Set to True for production
            slow_mo=self._calculate_persona_slow_mo(persona),
            args=browser_args
        )
        
        # Generate realistic geolocation based on persona
        geolocation = self._generate_persona_geolocation(persona)
        
        context = await browser.new_context(
            viewport=config["viewport"],
            user_agent=user_agent,
            device_scale_factor=config["device_scale_factor"],
            locale=self._get_persona_locale(persona),
            timezone_id=geolocation["timezone"],
            geolocation={"latitude": geolocation["lat"], "longitude": geolocation["lng"]},
            permissions=["geolocation"],
            color_scheme=self._get_persona_color_scheme(persona),
            extra_http_headers=self._generate_persona_headers(persona)
        )
        
        page = await context.new_page()
        
        if stealth_available:
            await stealth_async(page)
        
        # Inject persona-specific behavioral scripts
        await self._inject_persona_behavior_scripts(page, persona)
        
        return page, browser, playwright
    
    def _generate_persona_user_agent(self, persona: UserPersona, device: str) -> str:
        """Generate realistic user agent based on persona and device"""
        
        # Tech-savvy users might have newer browsers
        if persona.tech_comfort == "high":
            chrome_versions = ["120.0.0.0", "119.0.0.0", "121.0.0.0"]
        elif persona.tech_comfort == "medium":
            chrome_versions = ["119.0.0.0", "118.0.0.0", "120.0.0.0"]
        else:
            chrome_versions = ["118.0.0.0", "117.0.0.0", "119.0.0.0"]
        
        version = random.choice(chrome_versions)
        
        if device == "mobile":
            return f"Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{version} Mobile/15E148 Safari/604.1"
        elif device == "tablet":
            return f"Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{version} Mobile/15E148 Safari/604.1"
        else:
            os_options = [
                f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
                f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
            ]
            return random.choice(os_options)
    
    def _calculate_persona_slow_mo(self, persona: UserPersona) -> int:
        """Calculate slow motion based on persona browsing speed"""
        speed_map = {
            "slow": random.randint(100, 200),
            "medium": random.randint(50, 100),
            "fast": random.randint(20, 50)
        }
        return speed_map[persona.browsing_speed]
    
    def _generate_persona_geolocation(self, persona: UserPersona) -> Dict[str, Any]:
        """Generate realistic geolocation based on persona"""
        
        # Major cities with timezones (simplified)
        locations = [
            {"city": "New York", "lat": 40.7128, "lng": -74.0060, "timezone": "America/New_York"},
            {"city": "Los Angeles", "lat": 34.0522, "lng": -118.2437, "timezone": "America/Los_Angeles"},
            {"city": "Chicago", "lat": 41.8781, "lng": -87.6298, "timezone": "America/Chicago"},
            {"city": "Houston", "lat": 29.7604, "lng": -95.3698, "timezone": "America/Chicago"},
            {"city": "Phoenix", "lat": 33.4484, "lng": -112.0740, "timezone": "America/Phoenix"},
            {"city": "Philadelphia", "lat": 39.9526, "lng": -75.1652, "timezone": "America/New_York"},
            {"city": "San Antonio", "lat": 29.4241, "lng": -98.4936, "timezone": "America/Chicago"},
            {"city": "San Diego", "lat": 32.7157, "lng": -117.1611, "timezone": "America/Los_Angeles"},
            {"city": "Dallas", "lat": 32.7767, "lng": -96.7970, "timezone": "America/Chicago"},
            {"city": "Austin", "lat": 30.2672, "lng": -97.7431, "timezone": "America/Chicago"}
        ]
        
        location = random.choice(locations)
        
        # Add small random offset for realism
        location["lat"] += random.uniform(-0.1, 0.1)
        location["lng"] += random.uniform(-0.1, 0.1)
        
        return location
    
    def _get_persona_locale(self, persona: UserPersona) -> str:
        """Get locale based on persona"""
        return "en-US"  # Could be expanded for international personas
    
    def _get_persona_color_scheme(self, persona: UserPersona) -> str:
        """Get color scheme preference based on persona"""
        if persona.tech_comfort == "high":
            return random.choice(["light", "dark"])
        else:
            return "light"  # Less tech-savvy users typically prefer light mode
    
    def _generate_persona_headers(self, persona: UserPersona) -> Dict[str, str]:
        """Generate additional HTTP headers based on persona"""
        headers = {}
        
        # Tech-savvy users might have DNT enabled
        if persona.privacy_consciousness == "high":
            headers["DNT"] = "1"
        
        # Some users might have accept-language variations
        headers["Accept-Language"] = "en-US,en;q=0.9"
        
        return headers
    
    async def _inject_persona_behavior_scripts(self, page, persona: UserPersona):
        """Inject persona-specific behavioral scripts"""
        
        await page.add_init_script(f"""
            // Persona-specific behavior configuration
            window.personaConfig = {{
                techComfort: '{persona.tech_comfort}',
                browsingSpeed: '{persona.browsing_speed}',
                attentionSpan: '{persona.attention_span}',
                privacyConsciousness: '{persona.privacy_consciousness}',
                multitaskingTendency: '{persona.multitasking_tendency}'
            }};
            
            // Enhanced mouse tracking with persona characteristics
            window.mouseTracker = {{
                movements: [],
                clickPatterns: [],
                scrollPatterns: [],
                
                track: function(x, y, eventType) {{
                    const now = Date.now();
                    this.movements.push({{x, y, time: now, type: eventType}});
                    
                    // Keep only recent movements
                    if (this.movements.length > 200) {{
                        this.movements = this.movements.slice(-100);
                    }}
                }},
                
                recordClick: function(x, y, element) {{
                    this.clickPatterns.push({{
                        x, y, 
                        time: Date.now(),
                        element: element.tagName,
                        hesitation: this.calculateHesitation()
                    }});
                }},
                
                recordScroll: function(deltaY) {{
                    this.scrollPatterns.push({{
                        delta: deltaY,
                        time: Date.now(),
                        speed: this.calculateScrollSpeed()
                    }});
                }},
                
                calculateHesitation: function() {{
                    const recentMovements = this.movements.slice(-10);
                    if (recentMovements.length < 5) return 0;
                    
                    const distances = [];
                    for (let i = 1; i < recentMovements.length; i++) {{
                        const prev = recentMovements[i-1];
                        const curr = recentMovements[i];
                        const dist = Math.sqrt(
                            Math.pow(curr.x - prev.x, 2) + 
                            Math.pow(curr.y - prev.y, 2)
                        );
                        distances.push(dist);
                    }}
                    
                    return distances.reduce((a, b) => a + b, 0) / distances.length;
                }},
                
                calculateScrollSpeed: function() {{
                    const recentScrolls = this.scrollPatterns.slice(-5);
                    if (recentScrolls.length < 2) return 0;
                    
                    const timeDiff = recentScrolls[recentScrolls.length - 1].time - recentScrolls[0].time;
                    const totalDelta = recentScrolls.reduce((sum, scroll) => sum + Math.abs(scroll.delta), 0);
                    
                    return timeDiff > 0 ? totalDelta / timeDiff : 0;
                }}
            }};
            
            // Event listeners with persona-aware tracking
            document.addEventListener('mousemove', (e) => {{
                window.mouseTracker.track(e.clientX, e.clientY, 'move');
            }});
            
            document.addEventListener('click', (e) => {{
                window.mouseTracker.recordClick(e.clientX, e.clientY, e.target);
            }});
            
            document.addEventListener('wheel', (e) => {{
                window.mouseTracker.recordScroll(e.deltaY);
            }});
            
            // Persona-specific timing variations
            window.getPersonaDelay = function(baseDelay) {{
                const speedMultiplier = {{
                    'slow': 1.5,
                    'medium': 1.0,
                    'fast': 0.7
                }}[window.personaConfig.browsingSpeed] || 1.0;
                
                const techMultiplier = {{
                    'low': 1.3,
                    'medium': 1.0,
                    'high': 0.8
                }}[window.personaConfig.techComfort] || 1.0;
                
                return baseDelay * speedMultiplier * techMultiplier * (0.8 + Math.random() * 0.4);
            }};
            
            // Remove automation indicators
            Object.defineProperty(navigator, 'webdriver', {{
                get: () => undefined,
            }});
            
            // Realistic chrome object
            window.chrome = {{
                runtime: {{}},
                loadTimes: function() {{
                    return {{
                        commitLoadTime: Date.now() / 1000 - Math.random() * 100,
                        finishDocumentLoadTime: Date.now() / 1000 - Math.random() * 50,
                        finishLoadTime: Date.now() / 1000 - Math.random() * 25,
                        navigationType: "Other",
                        requestTime: Date.now() / 1000 - Math.random() * 150
                    }};
                }}
            }};
        """)
    
    async def simulate_enhanced_search_session(self, keyword: str, target_site: str, 
                                             persona: UserPersona = None) -> Dict[str, Any]:
        """
        Simulate enhanced search session with AI-driven behavior
        """
        
        if persona is None:
            persona = PersonaManager.get_random_persona()
        
        self.current_persona = persona
        self.usim_agent = USimAgent(persona)
        self.autowebglm = AutoWebGLM(persona)
        
        logging.info(f"Starting enhanced search session with {persona.name} persona")
        logging.info(f"Query: '{keyword}' -> Target: {target_site}")
        
        session_start = time.time()
        
        # Generate session goals based on persona and keyword
        self.session_goals = self._generate_session_goals(keyword, persona)
        
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
                    "reading_pattern": persona.reading_pattern
                }
            },
            "session_goals": self.session_goals,
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "success": False,
            "cognitive_journey": [],
            "patterns_used": []
        }
        
        # Create persona-specific browser
        page, browser, playwright = await self.create_realistic_browser_with_persona(persona)
        
        try:
            # Step 1: Navigate to Google with persona-aware behavior
            await self._enhanced_navigate_to_google(page, session_data)
            
            # Step 2: Perform search with cognitive modeling
            await self._enhanced_perform_search(page, keyword, session_data)
            
            # Step 3: Analyze SERP with AutoWebGLM intelligence
            await self._enhanced_interact_with_serp(page, target_site, session_data)
            
            # Step 4: Visit and explore target site with full AI integration
            success = await self._enhanced_visit_target_site(page, target_site, session_data)
            
            session_data["success"] = success
            session_data["duration"] = time.time() - session_start
            
            # Record final cognitive state
            session_data["final_cognitive_state"] = {
                "cognitive_load": self.usim_agent.cognitive_load,
                "fatigue_level": self.usim_agent.fatigue_level,
                "interest_level": self.usim_agent.interest_level,
                "emotional_state": self.usim_agent.emotional_state
            }
            
            logging.info(f"Enhanced search session completed: {success}")
            
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
    
    def _generate_session_goals(self, keyword: str, persona: UserPersona) -> List[str]:
        """Generate realistic session goals based on keyword and persona"""
        
        goals = []
        
        # Primary goal based on keyword intent
        primary_goal = self._analyze_keyword_intent(keyword)
        goals.append(primary_goal)
        
        # Secondary goals based on persona
        if persona.persona_type == UserPersonaType.RESEARCHER:
            goals.extend([
                "gather comprehensive information",
                "verify source credibility",
                "find related studies or papers"
            ])
        elif persona.persona_type == UserPersonaType.BARGAIN_HUNTER:
            goals.extend([
                "compare prices across sites",
                "look for discount codes or deals",
                "read user reviews"
            ])
        elif persona.persona_type == UserPersonaType.PROFESSIONAL:
            goals.extend([
                "find business-relevant information",
                "assess vendor capabilities",
                "gather competitive intelligence"
            ])
        elif persona.persona_type == UserPersonaType.STUDENT:
            goals.extend([
                "understand core concepts",
                "find learning resources",
                "gather information for assignments"
            ])
        
        return goals[:3]  # Limit to 3 main goals
    
    def _analyze_keyword_intent(self, keyword: str) -> str:
        """Analyze keyword to determine primary intent"""
        
        keyword_lower = keyword.lower()
        
        if any(word in keyword_lower for word in ["how to", "tutorial", "guide", "learn"]):
            return "learn how to do something"
        elif any(word in keyword_lower for word in ["buy", "price", "cost", "purchase"]):
            return "research purchase options"
        elif any(word in keyword_lower for word in ["review", "compare", "vs", "best"]):
            return "compare options and read reviews"
        elif any(word in keyword_lower for word in ["near me", "location", "address"]):
            return "find local information"
        elif any(word in keyword_lower for word in ["what is", "define", "meaning"]):
            return "understand concept or definition"
        else:
            return "gather general information"
    
    async def _enhanced_navigate_to_google(self, page, session_data: Dict):
        """Enhanced Google navigation with persona-aware behavior"""
        
        logging.info("Enhanced navigation to Google")
        
        # Persona-specific navigation patterns
        navigation_pattern = self.select_diverse_pattern("navigation_patterns")
        
        if navigation_pattern == "exploratory" and random.random() < 0.3:
            # Sometimes visit Google's homepage first, then navigate to search
            await page.goto("https://www.google.com", wait_until='networkidle', timeout=20000)
            
            # Persona-specific browsing of Google homepage
            if self.current_persona.attention_span == "long":
                await self._simulate_homepage_exploration(page)
        else:
            # Direct navigation to search
            await page.goto("https://www.google.com", wait_until='networkidle', timeout=20000)
        
        # Persona-specific reaction time
        timing_modifier = self.usim_agent.get_action_timing_modifier()
        base_delay = random.uniform(1, 3)
        actual_delay = base_delay * timing_modifier
        
        await asyncio.sleep(actual_delay)
        
        # Record cognitive state change
        self.usim_agent.update_cognitive_state(0.1, actual_delay)
        
        session_data["steps"].append({
            "action": "enhanced_navigate_to_google",
            "navigation_pattern": navigation_pattern,
            "timing_modifier": timing_modifier,
            "cognitive_state": {
                "load": self.usim_agent.cognitive_load,
                "interest": self.usim_agent.interest_level
            },
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
        
        session_data["patterns_used"].append(f"navigation_{navigation_pattern}")
    
    async def _simulate_homepage_exploration(self, page):
        """Simulate brief homepage exploration for exploratory users"""
        
        try:
            # Look around the homepage briefly
            viewport = page.viewport_size
            
            # Simulate reading/scanning behavior
            for _ in range(random.randint(2, 4)):
                x = random.randint(100, viewport["width"] - 100)
                y = random.randint(100, viewport["height"] - 100)
                
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Maybe hover over some elements
            try:
                links = await page.locator("a:visible").all()
                if links and random.random() < 0.4:
                    link = random.choice(links[:5])  # Top 5 links only
                    await link.hover()
                    await asyncio.sleep(random.uniform(1, 2))
            except:
                pass
                
        except Exception as e:
            logging.debug(f"Homepage exploration failed: {e}")
    
    async def _enhanced_perform_search(self, page, keyword: str, session_data: Dict):
        """Enhanced search with cognitive modeling and persona behavior"""
        
        logging.info(f"Enhanced search performance for: '{keyword}'")
        
        # Find search box with enhanced detection
        search_box = await self._find_search_box_enhanced(page)
        if not search_box:
            raise Exception("Enhanced search box detection failed")
        
        # Persona-aware clicking behavior
        click_pattern = self.select_diverse_pattern("click_patterns")
        await self._perform_persona_click(page, search_box, click_pattern)
        
        # Clear and prepare for typing
        await search_box.clear()
        await asyncio.sleep(random.uniform(0.2, 0.8))
        
        # Enhanced typing with persona characteristics
        typed_query = await self._enhanced_typing_behavior(page, keyword, session_data)
        
        # Persona-specific pre-search behavior
        await self._pre_search_behavior(page, session_data)
        
        # Submit search
        await page.keyboard.press("Enter")
        await page.wait_for_load_state('networkidle', timeout=15000)
        
        # Post-search cognitive update
        self.usim_agent.update_cognitive_state(0.3, 5.0)
        
        # Check if query refinement is needed
        if random.random() < self.current_persona.search_refinement_likelihood:
            refined_query = self.usim_agent.generate_search_refinement(keyword, 0.5)
            if refined_query:
                session_data["query_refinement"] = refined_query
        
        session_data["steps"].append({
            "action": "enhanced_perform_search",
            "original_keyword": keyword,
            "typed_query": typed_query,
            "click_pattern": click_pattern,
            "cognitive_load_after": self.usim_agent.cognitive_load,
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
        
        session_data["patterns_used"].append(f"click_{click_pattern}")
    
    async def _find_search_box_enhanced(self, page):
        """Enhanced search box detection with multiple strategies"""
        
        selectors = [
            "input[name='q']",
            "textarea[name='q']", 
            "input[title='Search']",
            ".gLFyf",
            "#APjFqb",
            "input[role='combobox']",
            "input[aria-label*='Search']"
        ]
        
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if await element.count() > 0:
                    # Wait for element to be ready
                    await element.wait_for(state="visible", timeout=5000)
                    if await element.is_visible() and await element.is_enabled():
                        return element
            except:
                continue
        
        return None
    
    async def _perform_persona_click(self, page, element, click_pattern: str):
        """Perform click based on persona and selected pattern"""
        
        if click_pattern == "immediate":
            # Quick, direct click
            await element.click()
            
        elif click_pattern == "hover_first":
            # Hover, then click (most common)
            await element.hover()
            await asyncio.sleep(random.uniform(0.5, 1.5))
            await element.click()
            
        elif click_pattern == "hesitant":
            # Show hesitation with multiple approaches
            await element.hover()
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            # Small mouse movement (hesitation)
            box = await element.bounding_box()
            if box:
                await page.mouse.move(
                    box["x"] + box["width"] * 0.3,
                    box["y"] + box["height"] * 0.5
                )
                await asyncio.sleep(random.uniform(0.3, 0.8))
            
            await element.click()
            
        elif click_pattern == "precision":
            # Very precise, calculated click
            box = await element.bounding_box()
            if box:
                # Click exactly in center
                center_x = box["x"] + box["width"] / 2
                center_y = box["y"] + box["height"] / 2
                
                await page.mouse.move(center_x, center_y)
                await asyncio.sleep(random.uniform(0.2, 0.5))
                await page.mouse.click(center_x, center_y)
            else:
                await element.click()
    
    async def _enhanced_typing_behavior(self, page, keyword: str, session_data: Dict) -> str:
        """Enhanced typing with persona-specific patterns and realistic errors"""
        
        # Determine if user will type exactly or with variations
        will_modify_query = random.random() < 0.3  # 30% chance of modification
        
        typed_query = keyword
        
        if will_modify_query:
            typed_query = self._apply_typing_variations(keyword)
        
        # Persona-specific typing speed
        base_speed = {
            "slow": random.uniform(120, 200),    # ms per character
            "medium": random.uniform(80, 120),
            "fast": random.uniform(50, 80)
        }[self.current_persona.browsing_speed]
        
        # Tech comfort affects typing accuracy and speed
        if self.current_persona.tech_comfort == "high":
            base_speed *= 0.8  # Faster
            error_rate = 0.02  # 2% error rate
        elif self.current_persona.tech_comfort == "low":
            base_speed *= 1.3  # Slower
            error_rate = 0.08  # 8% error rate
        else:
            error_rate = 0.05  # 5% error rate
        
        # Type with realistic patterns
        await self._type_with_realistic_patterns(page, typed_query, base_speed, error_rate)
        
        return typed_query
    
    def _apply_typing_variations(self, keyword: str) -> str:
        """Apply realistic typing variations"""
        
        variations = []
        
        # Common query modifications
        if random.random() < 0.4:
            # Add year for recency
            variations.append(f"{keyword} 2024")
            
        if random.random() < 0.3:
            # Add qualifiers
            qualifiers = ["best", "top", "how to", "guide", "tutorial", "review"]
            qualifier = random.choice(qualifiers)
            if qualifier not in keyword.lower():
                variations.append(f"{qualifier} {keyword}")
        
        if random.random() < 0.2:
            # Add location context
            variations.append(f"{keyword} near me")
        
        return random.choice(variations) if variations else keyword
    
    async def _type_with_realistic_patterns(self, page, text: str, base_speed: float, error_rate: float):
        """Type with realistic human patterns including errors and corrections"""
        
        i = 0
        while i < len(text):
            char = text[i]
            
            # Calculate delay for this character
            char_delay = base_speed / 1000.0  # Convert to seconds
            
            # Add randomness
            char_delay *= random.uniform(0.5, 1.8)
            
            # Longer pauses for word boundaries
            if char == ' ':
                char_delay *= random.uniform(1.5, 3.0)
            
            # Occasional thinking pauses
            if random.random() < 0.1:
                char_delay *= random.uniform(2.0, 4.0)
            
            # Check for typing error
            if random.random() < error_rate and char.isalpha():
                # Type wrong character first
                wrong_chars = "abcdefghijklmnopqrstuvwxyz"
                wrong_char = random.choice(wrong_chars.replace(char.lower(), ''))
                
                await page.keyboard.type(wrong_char)
                await asyncio.sleep(char_delay * 0.5)
                
                # Realize mistake and correct
                await page.keyboard.press("Backspace")
                await asyncio.sleep(char_delay * 0.3)
            
            # Type the correct character
            await page.keyboard.type(char)
            await asyncio.sleep(char_delay)
            
            i += 1
    
    async def _pre_search_behavior(self, page, session_data: Dict):
        """Simulate pre-search behavior based on persona"""
        
        # Thinking pause before submitting
        thinking_time = random.uniform(0.5, 3.0)
        
        # Persona adjustments
        if self.current_persona.attention_span == "long":
            thinking_time *= 1.5
        elif self.current_persona.browsing_speed == "fast":
            thinking_time *= 0.7
        
        # Apply cognitive timing modifier
        thinking_time *= self.usim_agent.get_action_timing_modifier()
        
        await asyncio.sleep(thinking_time)
        
        # Sometimes move cursor or check typed query
        if random.random() < 0.3:
            # Brief cursor movement or text selection
            await page.keyboard.press("Home")
            await asyncio.sleep(random.uniform(0.2, 0.5))
            await page.keyboard.press("End")
            await asyncio.sleep(random.uniform(0.2, 0.5))
    
    async def _enhanced_interact_with_serp(self, page, target_site: str, session_data: Dict):
        """Enhanced SERP interaction with AutoWebGLM intelligence"""
        
        logging.info("Enhanced SERP interaction with AI analysis")
        
        # Wait for results to load
        await page.wait_for_load_state('networkidle', timeout=15000)
        await asyncio.sleep(random.uniform(1, 3))
        
        # Analyze page context with AutoWebGLM
        page_context = await self.autowebglm.analyze_page_context(page)
        
        # Generate intelligent navigation plan
        current_goal = self.session_goals[0] if self.session_goals else "general browsing"
        navigation_plan = self.autowebglm.generate_intelligent_navigation_plan(current_goal, page_context)
        
        # Extract target domain
        target_domain = urlparse(target_site).netloc.replace('www.', '')
        
        # Perform enhanced SERP scanning
        await self._enhanced_serp_scanning(page, session_data)
        
        # Find target result with AI assistance
        target_result = await self._ai_assisted_target_finding(page, target_domain, session_data)
        
        if target_result:
            # Perform pre-click analysis and interaction
            await self._intelligent_pre_click_behavior(page, target_result, navigation_plan, session_data)
            
            # Execute click with enhanced pattern selection
            success = await self._execute_enhanced_click(page, target_result, target_site, session_data)
            
            session_data["steps"].append({
                "action": "enhanced_serp_interaction",
                "target_found": True,
                "page_context": page_context,
                "navigation_plan": [plan.get("action", "unknown") for plan in navigation_plan],
                "click_success": success,
                "timestamp": datetime.now().isoformat(),
                "success": success
            })
        else:
            # Target not found - implement fallback strategies
            await self._handle_target_not_found(page, target_domain, session_data)
    
    async def _enhanced_serp_scanning(self, page, session_data: Dict):
        """Enhanced SERP scanning with persona-aware patterns"""
        
        # Select scanning pattern based on persona
        scanning_pattern = self.select_diverse_pattern("scroll_patterns")
        
        if scanning_pattern == "linear":
            await self._linear_serp_scan(page)
        elif scanning_pattern == "jump_scroll":
            await self._jump_scroll_serp_scan(page)
        elif scanning_pattern == "careful_read":
            await self._careful_read_serp_scan(page)
        elif scanning_pattern == "speed_scan":
            await self._speed_scan_serp_scan(page)
        
        session_data["patterns_used"].append(f"scan_{scanning_pattern}")
        
        # Update cognitive state based on scanning effort
        scan_complexity = {
            "linear": 0.2, "jump_scroll": 0.3, "careful_read": 0.4, "speed_scan": 0.15
        }[scanning_pattern]
        
        self.usim_agent.update_cognitive_state(scan_complexity, random.uniform(5, 15))
    
    async def _linear_serp_scan(self, page):
        """Linear, systematic SERP scanning"""
        # Scroll down gradually, reading each result
        for _ in range(random.randint(3, 6)):
            await page.mouse.wheel(0, random.randint(200, 400))
            await asyncio.sleep(random.uniform(2, 4))
            
            # Simulate reading result titles and snippets
            await self._simulate_result_reading(page)
    
    async def _jump_scroll_serp_scan(self, page):
        """Quick jumps through SERP results"""
        # Quick scrolls with pauses at interesting results
        for _ in range(random.randint(4, 8)):
            await page.mouse.wheel(0, random.randint(300, 600))
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Occasionally pause to read
            if random.random() < 0.4:
                await self._simulate_result_reading(page)
    
    async def _careful_read_serp_scan(self, page):
        """Thorough, careful reading of SERP results"""
        # Slow, methodical scanning
        for _ in range(random.randint(2, 4)):
            await page.mouse.wheel(0, random.randint(150, 300))
            await asyncio.sleep(random.uniform(3, 6))
            
            # Read multiple results carefully
            await self._simulate_detailed_result_reading(page)
    
    async def _speed_scan_serp_scan(self, page):
        """Fast scanning looking for specific information"""
        # Quick, goal-directed scanning
        await page.mouse.wheel(0, random.randint(400, 800))
        await asyncio.sleep(random.uniform(1, 2))
        
        # Quick scan back up
        await page.mouse.wheel(0, -random.randint(200, 400))
        await asyncio.sleep(random.uniform(0.5, 1))
    
    async def _simulate_result_reading(self, page):
        """Simulate reading individual search results"""
        try:
            # Find visible result titles
            result_titles = await page.locator(".g h3:visible, .yuRUbf h3:visible").all()
            
            if result_titles:
                # Hover over 1-2 results
                for _ in range(min(random.randint(1, 2), len(result_titles))):
                    title = random.choice(result_titles)
                    if await title.is_visible():
                        await title.hover()
                        await asyncio.sleep(random.uniform(1, 2.5))
                        
                        # Small mouse movements while reading
                        await self._simulate_reading_mouse_movement(page)
                        
        except Exception as e:
            logging.debug(f"Result reading simulation failed: {e}")
    
    async def _simulate_detailed_result_reading(self, page):
        """Simulate detailed reading of search results"""
        try:
            # Find result containers
            results = await page.locator(".g:visible").all()
            
            for result in results[:3]:  # Read top 3 in detail
                if await result.is_visible():
                    # Hover over title
                    title = result.locator("h3").first
                    if await title.count() > 0:
                        await title.hover()
                        await asyncio.sleep(random.uniform(2, 3))
                    
                    # Read snippet
                    snippet = result.locator(".VwiC3b, .s3v9rd").first
                    if await snippet.count() > 0:
                        await snippet.hover()
                        await asyncio.sleep(random.uniform(1.5, 2.5))
                    
                    # Small pause between results
                    await asyncio.sleep(random.uniform(0.5, 1))
                    
        except Exception as e:
            logging.debug(f"Detailed result reading failed: {e}")
    
    async def _simulate_reading_mouse_movement(self, page):
        """Simulate natural mouse movement while reading"""
        try:
            viewport = page.viewport_size
            
            # Small, natural movements
            for _ in range(random.randint(2, 4)):
                current_x = random.randint(100, viewport["width"] - 100)
                current_y = random.randint(100, viewport["height"] - 100)
                
                await page.mouse.move(current_x, current_y)
                await asyncio.sleep(random.uniform(0.2, 0.5))
                
        except Exception as e:
            logging.debug(f"Reading mouse movement failed: {e}")
    
    async def _ai_assisted_target_finding(self, page, target_domain: str, session_data: Dict):
        """AI-assisted target finding with multiple strategies"""
        
        logging.info(f"AI-assisted search for target: {target_domain}")
        
        # Strategy 1: Intelligent element detection
        target_result = await self._intelligent_element_detection(page, target_domain)
        
        if target_result:
            logging.info("Target found via intelligent element detection")
            return target_result
        
        # Strategy 2: Semantic content analysis
        target_result = await self._semantic_content_search(page, target_domain)
        
        if target_result:
            logging.info("Target found via semantic content analysis")
            return target_result
        
        # Strategy 3: Fallback to enhanced traditional search
        target_result = await self._enhanced_traditional_search(page, target_domain)
        
        if target_result:
            logging.info("Target found via enhanced traditional search")
            return target_result
        
        logging.warning(f"Target {target_domain} not found with AI assistance")
        return None
    
    async def _intelligent_element_detection(self, page, target_domain: str):
        """Intelligent element detection using multiple signals"""
        
        try:
            # Get all potential link candidates
            links = await page.locator("a[href*='http']:visible").all()
            
            candidates = []
            
            for link in links:
                try:
                    href = await link.get_attribute("href")
                    if not href or target_domain not in href:
                        continue
                    
                    # Skip unwanted links
                    if any(skip in href for skip in ['webcache', 'translate', 'ads']):
                        continue
                    
                    # Calculate relevance score
                    relevance_score = await self._calculate_link_relevance(link, target_domain)
                    
                    candidates.append({
                        'element': link,
                        'href': href,
                        'score': relevance_score
                    })
                    
                except Exception as e:
                    continue
            
            # Return highest scoring candidate
            if candidates:
                best_candidate = max(candidates, key=lambda x: x['score'])
                if best_candidate['score'] > 0.5:  # Minimum confidence threshold
                    return best_candidate['element']
            
        except Exception as e:
            logging.debug(f"Intelligent element detection failed: {e}")
        
        return None
    
    async def _calculate_link_relevance(self, link, target_domain: str) -> float:
        """Calculate link relevance score"""
        
        score = 0.0
        
        try:
            # Check position (higher is better for organic results)
            position = await link.evaluate("el => Array.from(el.closest('.g')?.parentNode?.children || []).indexOf(el.closest('.g'))")
            if position >= 0 and position < 10:
                score += (10 - position) * 0.1
            
            # Check if it's in main results area
            is_main_result = await link.evaluate("el => !!el.closest('.g, .yuRUbf')")
            if is_main_result:
                score += 0.3
            
            # Check text content relevance
            text_content = await link.inner_text()
            if target_domain.replace('.com', '').replace('.org', '') in text_content.lower():
                score += 0.2
            
            # Check if it's a title link (most important)
            is_title_link = await link.evaluate("el => el.closest('h3') !== null")
            if is_title_link:
                score += 0.4
            
        except Exception as e:
            logging.debug(f"Relevance calculation failed: {e}")
        
        return min(1.0, score)
    
    async def _semantic_content_search(self, page, target_domain: str):
        """Search using semantic content analysis"""
        
        try:
            # Extract content from result containers
            result_containers = await page.locator(".g:visible, .yuRUbf:visible").all()
            
            for container in result_containers:
                try:
                    # Get all text content
                    content = await container.inner_text()
                    
                    # Check for domain variations
                    domain_variations = [
                        target_domain,
                        target_domain.replace('www.', ''),
                        target_domain.replace('.com', '').replace('.org', '').replace('.net', ''),
                        target_domain.split('.')[0]  # Just the main part
                    ]
                    
                    if any(variation.lower() in content.lower() for variation in domain_variations):
                        # Find the main link in this container
                        main_link = container.locator("a[href*='http']").first
                        if await main_link.count() > 0 and await main_link.is_visible():
                            href = await main_link.get_attribute("href")
                            if href and target_domain in href:
                                return main_link
                                
                except Exception as e:
                    continue
            
        except Exception as e:
            logging.debug(f"Semantic content search failed: {e}")
        
        return None
    
    async def _enhanced_traditional_search(self, page, target_domain: str):
        """Enhanced version of traditional search methods"""
        
        # Multiple selector strategies
        selector_strategies = [
            f"a[href*='{target_domain}']:visible",
            f".g:visible a[href*='{target_domain}']",
            f".yuRUbf:visible a[href*='{target_domain}']",
            f"h3 a[href*='{target_domain}']:visible"
        ]
        
        for strategy in selector_strategies:
            try:
                elements = await page.locator(strategy).all()
                
                for element in elements:
                    if await element.is_visible() and await element.is_enabled():
                        href = await element.get_attribute("href")
                        if href and target_domain in href and not any(x in href for x in ['webcache', 'translate']):
                            # Verify element is actually interactable
                            try:
                                await element.scroll_into_view_if_needed()
                                await asyncio.sleep(0.5)
                                
                                if await element.is_visible():
                                    return element
                            except:
                                continue
            except Exception as e:
                continue
        
        return None
    
    async def _intelligent_pre_click_behavior(self, page, target_result, navigation_plan: List[Dict], session_data: Dict):
        """Intelligent pre-click behavior based on AutoWebGLM plan"""
        
        # Hover on target with persona-specific timing
        hover_duration = random.uniform(1, 3)
        
        # Adjust for persona characteristics
        if self.current_persona.browsing_speed == "slow":
            hover_duration *= 1.5
        elif self.current_persona.tech_comfort == "low":
            hover_duration *= 1.3
        
        try:
            await target_result.hover()
            await asyncio.sleep(hover_duration)
            
            # Simulate decision-making process
            decision_time = self._calculate_decision_time(navigation_plan)
            await asyncio.sleep(decision_time)
            
            # Sometimes check URL in status bar (tech-savvy behavior)
            if (self.current_persona.tech_comfort == "high" and 
                self.current_persona.privacy_consciousness == "high" and 
                random.random() < 0.4):
                
                # Pause to "read" the URL
                await asyncio.sleep(random.uniform(1, 2))
            
        except Exception as e:
            logging.debug(f"Pre-click behavior failed: {e}")
    
    def _calculate_decision_time(self, navigation_plan: List[Dict]) -> float:
        """Calculate decision time based on plan complexity and persona"""
        
        base_time = random.uniform(1, 4)
        
        # More complex plans require more thinking
        plan_complexity = len(navigation_plan) * 0.5
        
        # Persona adjustments
        persona_modifier = {
            "slow": 1.5,
            "medium": 1.0,
            "fast": 0.7
        }[self.current_persona.browsing_speed]
        
        # Cognitive state affects decision time
        cognitive_modifier = self.usim_agent.get_action_timing_modifier()
        
        return (base_time + plan_complexity) * persona_modifier * cognitive_modifier
    
    async def _execute_enhanced_click(self, page, target_result, target_site: str, session_data: Dict) -> bool:
        """Execute click with enhanced error handling and fallback strategies"""
        
        click_success = False
        attempts = []
        
        try:
            # Get href for validation
            href = await target_result.get_attribute("href")
            logging.info(f"Attempting enhanced click on: {href}")
            
            # Strategy 1: Persona-aware click
            try:
                click_pattern = self.select_diverse_pattern("click_patterns")
                await self._perform_persona_click(page, target_result, click_pattern)
                
                # Wait for navigation
                await page.wait_for_load_state('networkidle', timeout=15000)
                
                if await self._verify_successful_navigation(page, target_site):
                    click_success = True
                    attempts.append({"method": f"persona_click_{click_pattern}", "success": True})
                else:
                    attempts.append({"method": f"persona_click_{click_pattern}", "success": False})
                    
            except Exception as e:
                attempts.append({"method": "persona_click", "success": False, "error": str(e)})
            
            # Strategy 2: JavaScript click if persona click failed
            if not click_success:
                try:
                    await target_result.evaluate("element => element.click()")
                    await page.wait_for_load_state('networkidle', timeout=10000)
                    
                    if await self._verify_successful_navigation(page, target_site):
                        click_success = True
                        attempts.append({"method": "javascript_click", "success": True})
                    else:
                        attempts.append({"method": "javascript_click", "success": False})
                        
                except Exception as e:
                    attempts.append({"method": "javascript_click", "success": False, "error": str(e)})
            
            # Strategy 3: Direct navigation if clicks failed
            if not click_success and href:
                try:
                    clean_url = self._clean_google_url(href)
                    await page.goto(clean_url, wait_until='networkidle', timeout=15000)
                    
                    if await self._verify_successful_navigation(page, target_site):
                        click_success = True
                        attempts.append({"method": "direct_navigation", "success": True})
                    else:
                        attempts.append({"method": "direct_navigation", "success": False})
                        
                except Exception as e:
                    attempts.append({"method": "direct_navigation", "success": False, "error": str(e)})
            
        except Exception as e:
            logging.error(f"Enhanced click execution failed: {e}")
        
        # Update session data
        session_data["click_attempts"] = attempts
        session_data["final_click_success"] = click_success
        
        return click_success
    
    async def _verify_successful_navigation(self, page, target_site: str) -> bool:
        """Verify that navigation was successful"""
        
        try:
            current_url = page.url
            target_domain = urlparse(target_site).netloc.replace('www.', '')
            current_domain = urlparse(current_url).netloc.replace('www.', '')
            
            # Flexible domain matching
            is_correct_site = (
                target_domain in current_domain or 
                current_domain in target_domain or
                target_domain.replace('.com', '') in current_domain or
                any(part in current_domain for part in target_domain.split('.') if len(part) > 3)
            )
            
            # Additional checks for error pages
            if is_correct_site:
                try:
                    page_title = await page.title()
                    if any(error in page_title.lower() for error in ['error', '404', '403', '500', 'not found']):
                        return False
                except:
                    pass
            
            return is_correct_site
            
        except Exception as e:
            logging.debug(f"Navigation verification failed: {e}")
            return False
    
    def _clean_google_url(self, google_url: str) -> str:
        """Clean Google's wrapped URLs"""
        
        try:
            if not google_url.startswith('https://www.google.com/url'):
                return google_url
            
            import urllib.parse as urlparse_module
            parsed = urlparse_module.urlparse(google_url)
            query_params = urlparse_module.parse_qs(parsed.query)
            
            if 'url' in query_params:
                return query_params['url'][0]
            elif 'q' in query_params:
                return query_params['q'][0]
                
        except Exception:
            pass
        
        return google_url
    
    async def _handle_target_not_found(self, page, target_domain: str, session_data: Dict):
        """Handle case when target is not found in SERP"""
        
        logging.warning(f"Target {target_domain} not found - implementing fallback strategies")
        
        # Strategy 1: Query refinement
        if self.current_persona.search_refinement_likelihood > 0.5:
            await self._attempt_query_refinement(page, target_domain, session_data)
        
        # Strategy 2: Explore alternative results
        elif random.random() < 0.4:
            await self._explore_alternative_results(page, session_data)
        
        # Strategy 3: Accept failure and record insights
        session_data["steps"].append({
            "action": "target_not_found_handled",
            "target_domain": target_domain,
            "fallback_strategy": "query_refinement" if self.current_persona.search_refinement_likelihood > 0.5 else "explore_alternatives",
            "timestamp": datetime.now().isoformat(),
            "success": False
        })
    
    async def _attempt_query_refinement(self, page, target_domain: str, session_data: Dict):
        """Attempt to refine the search query"""
        
        try:
            # Find search box again
            search_box = await self._find_search_box_enhanced(page)
            if search_box:
                # Clear and try refined query
                refined_query = f"site:{target_domain}"
                
                await search_box.clear()
                await asyncio.sleep(random.uniform(0.5, 1))
                await self._type_with_realistic_patterns(page, refined_query, 100, 0.02)
                await asyncio.sleep(random.uniform(1, 2))
                await page.keyboard.press("Enter")
                
                await page.wait_for_load_state('networkidle', timeout=10000)
                
                session_data["query_refinement_attempted"] = refined_query
                
        except Exception as e:
            logging.debug(f"Query refinement failed: {e}")
    
    async def _explore_alternative_results(self, page, session_data: Dict):
        """Explore alternative results when target not found"""
        
        try:
            # Click on a relevant-looking alternative result
            results = await page.locator(".g:visible h3 a").all()
            
            if results and len(results) > 2:
                # Choose 2nd or 3rd result (avoid ads)
                alternative = results[random.randint(1, min(3, len(results) - 1))]
                
                await alternative.hover()
                await asyncio.sleep(random.uniform(1, 2))
                await alternative.click()
                
                await page.wait_for_load_state('networkidle', timeout=10000)
                
                # Spend some time on alternative site
                await asyncio.sleep(random.uniform(10, 20))
                
                session_data["explored_alternative"] = True
                
        except Exception as e:
            logging.debug(f"Alternative exploration failed: {e}")
    
    async def _enhanced_visit_target_site(self, page, target_site: str, session_data: Dict) -> bool:
        """Enhanced target site visit with full AI integration"""
        
        logging.info(f"Enhanced target site visit: {target_site}")
        
        try:
            # Wait for page to load completely
            await page.wait_for_load_state('networkidle', timeout=20000)
            await asyncio.sleep(random.uniform(1, 3))
            
            # Verify we're on the correct site
            if not await self._verify_successful_navigation(page, target_site):
                logging.warning("Navigation verification failed")
                return False
            
            current_url = page.url
            logging.info(f"Successfully reached: {current_url}")
            
            # Analyze page with AutoWebGLM
            page_context = await self.autowebglm.analyze_page_context(page)
            
            # Generate intelligent browsing plan
            browsing_goals = self.session_goals + ["evaluate page content", "natural browsing behavior"]
            main_goal = browsing_goals[0]
            browsing_plan = self.autowebglm.generate_intelligent_navigation_plan(main_goal, page_context)
            
            # Calculate session duration based on persona and content
            session_duration = self._calculate_intelligent_session_duration(page_context)
            
            # Execute intelligent browsing activities
            activities_performed = await self._execute_intelligent_browsing(
                page, session_duration, browsing_plan, page_context, session_data
            )
            
            # Record detailed session data
            session_data["steps"].append({
                "action": "enhanced_site_visit_complete",
                "final_url": current_url,
                "page_context": page_context,
                "browsing_plan": [plan.get("action", "unknown") for plan in browsing_plan],
                "activities_performed": activities_performed,
                "session_duration": session_duration,
                "cognitive_state_final": {
                    "load": self.usim_agent.cognitive_load,
                    "fatigue": self.usim_agent.fatigue_level,
                    "interest": self.usim_agent.interest_level,
                    "emotion": self.usim_agent.emotional_state
                },
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            return True
            
        except Exception as e:
            logging.error(f"Enhanced site visit failed: {e}")
            session_data["steps"].append({
                "action": "enhanced_site_visit_failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "success": False
            })
            return False
    
    def _calculate_intelligent_session_duration(self, page_context: Dict) -> int:
        """Calculate session duration based on page context and persona"""
        
        # Base duration from persona
        min_duration, max_duration = self.current_persona.session_duration_range
        base_duration = random.randint(min_duration, max_duration)
        
        # Adjust based on page content
        content_multiplier = 1.0
        
        if page_context.get("content_density") == "high":
            content_multiplier *= 1.3
        elif page_context.get("content_density") == "low":
            content_multiplier *= 0.8
        
        # Adjust based on page type
        page_type = page_context.get("page_type", "unknown")
        type_multipliers = {
            "homepage": 0.8,
            "content/blog": 1.4,
            "ecommerce": 1.2,
            "search_results": 0.7,
            "contact/form": 1.1
        }
        content_multiplier *= type_multipliers.get(page_type, 1.0)
        
        # Adjust based on cognitive state
        cognitive_multiplier = 1.0
        if self.usim_agent.interest_level > 0.7:
            cognitive_multiplier *= 1.2
        elif self.usim_agent.fatigue_level > 0.6:
            cognitive_multiplier *= 0.8
        
        final_duration = int(base_duration * content_multiplier * cognitive_multiplier)
        return max(30, min(600, final_duration))  # Clamp between 30 seconds and 10 minutes
    
    async def _execute_intelligent_browsing(self, page, total_duration: int, browsing_plan: List[Dict], 
                                          page_context: Dict, session_data: Dict) -> List[str]:
        """Execute intelligent browsing based on AI-generated plan"""
        
        start_time = time.time()
        end_time = start_time + total_duration
        activities_performed = []
        
        logging.info(f"Executing {total_duration}s of intelligent browsing")
        
        # Initial page orientation
        await self._intelligent_page_orientation(page, page_context)
        activities_performed.append("page_orientation")
        
        # Execute planned activities
        while time.time() < end_time and self.usim_agent.should_continue_browsing():
            remaining_time = end_time - time.time()
            
            if remaining_time < 5:
                break
            
            # Select activity based on plan and remaining time
            activity = self._select_next_activity(browsing_plan, remaining_time, page_context)
            
            try:
                activity_duration = await self._execute_planned_activity(page, activity, page_context)
                activities_performed.append(activity.get("action", "unknown_activity"))
                
                # Update cognitive state
                complexity = activity.get("complexity", 0.3)
                self.usim_agent.update_cognitive_state(complexity, activity_duration)
                
                # Record cognitive journey
                session_data.setdefault("cognitive_journey", []).append({
                    "time": time.time() - start_time,
                    "activity": activity.get("action", "unknown"),
                    "cognitive_load": self.usim_agent.cognitive_load,
                    "interest_level": self.usim_agent.interest_level,
                    "fatigue_level": self.usim_agent.fatigue_level,
                    "emotional_state": self.usim_agent.emotional_state
                })
                
            except Exception as e:
                logging.debug(f"Activity execution failed: {activity.get('action', 'unknown')} - {e}")
                activities_performed.append(f"failed_{activity.get('action', 'unknown')}")
        
        # Final page interaction before leaving
        if random.random() < 0.3:
            await self._final_page_interaction(page, page_context)
            activities_performed.append("final_interaction")
        
        logging.info(f"Completed intelligent browsing with {len(activities_performed)} activities")
        return activities_performed
    
    async def _intelligent_page_orientation(self, page, page_context: Dict):
        """Intelligent page orientation based on page type and persona"""
        
        page_type = page_context.get("page_type", "unknown")
        
        if page_type == "homepage":
            await self._homepage_orientation(page)
        elif page_type == "content/blog":
            await self._content_page_orientation(page)
        elif page_type == "ecommerce":
            await self._ecommerce_orientation(page)
        else:
            await self._general_page_orientation(page)
    
    async def _homepage_orientation(self, page):
        """Homepage-specific orientation behavior"""
        # Quick scan of main navigation and hero area
        await page.mouse.wheel(0, random.randint(100, 300))
        await asyncio.sleep(random.uniform(2, 4))
        
        # Look for main navigation
        try:
            nav_elements = await page.locator("nav, .navigation, .navbar").all()
            if nav_elements:
                nav = nav_elements[0]
                await nav.hover()
                await asyncio.sleep(random.uniform(1, 2))
        except:
            pass
    
    async def _content_page_orientation(self, page):
        """Content/blog page orientation"""
        # Focus on article title and beginning
        try:
            title = page.locator("h1, .title, .post-title").first
            if await title.count() > 0:
                await title.hover()
                await asyncio.sleep(random.uniform(2, 3))
        except:
            pass
        
        # Scroll to start of content
        await page.mouse.wheel(0, random.randint(200, 400))
        await asyncio.sleep(random.uniform(1, 2))
    
    async def _ecommerce_orientation(self, page):
        """E-commerce page orientation"""
        # Look for product information, pricing
        await page.mouse.wheel(0, random.randint(150, 350))
        await asyncio.sleep(random.uniform(1.5, 3))
        
        # Search for price information
        try:
            price_elements = await page.locator(".price, .cost, .amount").all()
            if price_elements:
                price = price_elements[0]
                await price.hover()
                await asyncio.sleep(random.uniform(1, 2))
        except:
            pass
    
    async def _general_page_orientation(self, page):
        """General page orientation"""
        # Basic page scan
        await page.mouse.wheel(0, random.randint(200, 400))
        await asyncio.sleep(random.uniform(2, 3))
    
    def _select_next_activity(self, browsing_plan: List[Dict], remaining_time: float, page_context: Dict) -> Dict:
        """Select next activity based on plan, time, and context"""
        
        # Filter activities that can fit in remaining time
        suitable_activities = []
        
        for activity in browsing_plan:
            activity_duration = activity.get("duration", (30, 60))
            if isinstance(activity_duration, tuple):
                min_duration = activity_duration[0]
            else:
                min_duration = activity_duration
            
            if min_duration <= remaining_time:
                suitable_activities.append(activity)
        
        # If no planned activities fit, use fallback activities
        if not suitable_activities:
            suitable_activities = self._get_fallback_activities(remaining_time)
        
        # Weight activities by priority and persona preferences
        return self._weight_activity_selection(suitable_activities, page_context)
    
    def _get_fallback_activities(self, remaining_time: float) -> List[Dict]:
        """Get fallback activities for remaining time"""
        
        fallback_activities = [
            {"action": "quick_scroll", "duration": (5, 15), "complexity": 0.1},
            {"action": "hover_elements", "duration": (10, 25), "complexity": 0.2},
            {"action": "read_snippets", "duration": (15, 30), "complexity": 0.3}
        ]
        
        return [activity for activity in fallback_activities 
                if activity["duration"][0] <= remaining_time]
    
    def _weight_activity_selection(self, activities: List[Dict], page_context: Dict) -> Dict:
        """Weight activity selection based on persona and context"""
        
        if not activities:
            return {"action": "idle_wait", "duration": 5, "complexity": 0.1}
        
        # Simple weighted selection based on persona characteristics
        weights = []
        
        for activity in activities:
            weight = 1.0
            
            action_type = activity.get("action", "")
            
            # Adjust weights based on persona
            if self.current_persona.reading_pattern == "thorough" and "read" in action_type:
                weight *= 1.5
            elif self.current_persona.browsing_speed == "fast" and "quick" in action_type:
                weight *= 1.3
            elif self.current_persona.tech_comfort == "high" and "explore" in action_type:
                weight *= 1.2
            
            weights.append(weight)
        
        # Weighted random selection
        selected_activity = random.choices(activities, weights=weights)[0]
        return selected_activity
    
    async def _execute_planned_activity(self, page, activity: Dict, page_context: Dict) -> float:
        """Execute a planned activity and return duration"""
        
        action = activity.get("action", "unknown")
        duration_range = activity.get("duration", (30, 60))
        
        if isinstance(duration_range, tuple):
            duration = random.uniform(*duration_range)
        else:
            duration = duration_range
        
        # Apply persona timing modifier
        duration *= self.usim_agent.get_action_timing_modifier()
        
        start_time = time.time()
        
        try:
            if action == "deep_read":
                await self._deep_read_activity(page, duration)
            elif action == "scan_reviews":
                await self._scan_reviews_activity(page, duration)
            elif action == "check_pricing":
                await self._check_pricing_activity(page, duration)
            elif action == "explore_tabs":
                await self._explore_tabs_activity(page, duration)
            elif action == "read_about_section":
                await self._read_about_section_activity(page, duration)
            elif action == "check_contact_info":
                await self._check_contact_info_activity(page, duration)
            elif action == "evaluate_trust_signals":
                await self._evaluate_trust_signals_activity(page, duration)
            elif action == "casual_browsing":
                await self._casual_browsing_activity(page, duration)
            elif action == "detailed_comparison":
                await self._detailed_comparison_activity(page, duration)
            elif action == "general_exploration":
                await self._general_exploration_activity(page, duration)
            elif action == "quick_scroll":
                await self._quick_scroll_activity(page, duration)
            elif action == "hover_elements":
                await self._hover_elements_activity(page, duration)
            elif action == "read_snippets":
                await self._read_snippets_activity(page, duration)
            else:
                # Default fallback activity
                await self._default_activity(page, duration)
                
        except Exception as e:
            logging.debug(f"Activity execution error: {action} - {e}")
        
        actual_duration = time.time() - start_time
        return actual_duration
    
    async def _deep_read_activity(self, page, duration: float):
        """Deep reading activity for information seekers"""
        
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Slow, methodical scrolling
            await page.mouse.wheel(0, random.randint(100, 200))
            await asyncio.sleep(random.uniform(3, 6))
            
            # Simulate careful reading with mouse movement
            await self._simulate_careful_reading(page)
            
            # Occasional back-scrolling to re-read
            if random.random() < 0.3:
                await page.mouse.wheel(0, -random.randint(50, 150))
                await asyncio.sleep(random.uniform(2, 4))
    
    async def _scan_reviews_activity(self, page, duration: float):
        """Scan for reviews and ratings"""
        
        try:
            # Look for review sections
            review_selectors = [
                ".review", ".rating", ".testimonial", 
                ".feedback", ".comment", ".user-review"
            ]
            
            for selector in review_selectors:
                reviews = await page.locator(selector + ":visible").all()
                if reviews:
                    # Focus on reviews
                    for review in reviews[:3]:  # Read first 3 reviews
                        if await review.is_visible():
                            await review.hover()
                            await asyncio.sleep(random.uniform(2, 4))
                    break
                    
        except Exception as e:
            logging.debug(f"Review scanning failed: {e}")
        
        # Fallback to general scrolling if no reviews found
        await asyncio.sleep(duration * 0.5)
    
    async def _check_pricing_activity(self, page, duration: float):
        """Check pricing information"""
        
        try:
            # Look for pricing elements
            price_selectors = [
                ".price", ".cost", ".amount", ".pricing",
                ".fee", ".rate", ".charge", "[class*='price']"
            ]
            
            for selector in price_selectors:
                prices = await page.locator(selector + ":visible").all()
                if prices:
                    for price in prices[:2]:  # Check first 2 price elements
                        if await price.is_visible():
                            await price.hover()
                            await asyncio.sleep(random.uniform(1.5, 3))
                    break
                    
        except Exception as e:
            logging.debug(f"Price checking failed: {e}")
        
        await asyncio.sleep(duration * 0.3)
    
    async def _explore_tabs_activity(self, page, duration: float):
        """Explore tabbed content"""
        
        try:
            # Find tab elements
            tab_selectors = [
                ".tab", "[role='tab']", ".nav-tab", 
                ".tab-button", ".tab-link"
            ]
            
            for selector in tab_selectors:
                tabs = await page.locator(selector + ":visible").all()
                if tabs and len(tabs) > 1:
                    # Click on a different tab
                    tab_to_click = tabs[random.randint(1, min(3, len(tabs) - 1))]
                    
                    await tab_to_click.hover()
                    await asyncio.sleep(random.uniform(1, 2))
                    await tab_to_click.click()
                    await asyncio.sleep(random.uniform(2, 4))
                    
                    # Read content in new tab
                    await page.mouse.wheel(0, random.randint(100, 300))
                    await asyncio.sleep(random.uniform(3, 5))
                    break
                    
        except Exception as e:
            logging.debug(f"Tab exploration failed: {e}")
        
        await asyncio.sleep(duration * 0.4)
    
    async def _read_about_section_activity(self, page, duration: float):
        """Read about section or company information"""
        
        try:
            # Look for about sections
            about_selectors = [
                ".about", ".company-info", ".bio", 
                ".description", ".overview", "[id*='about']"
            ]
            
            for selector in about_selectors:
                about_sections = await page.locator(selector + ":visible").all()
                if about_sections:
                    section = about_sections[0]
                    await section.hover()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Read through the content
                    await page.mouse.wheel(0, random.randint(200, 400))
                    await asyncio.sleep(random.uniform(4, 8))
                    break
                    
        except Exception as e:
            logging.debug(f"About section reading failed: {e}")
        
        await asyncio.sleep(duration * 0.5)
    
    async def _check_contact_info_activity(self, page, duration: float):
        """Check contact information"""
        
        try:
            # Look for contact information
            contact_selectors = [
                ".contact", ".phone", ".email", ".address",
                ".contact-info", "[href*='mailto']", "[href*='tel']"
            ]
            
            for selector in contact_selectors:
                contacts = await page.locator(selector + ":visible").all()
                if contacts:
                    for contact in contacts[:2]:
                        if await contact.is_visible():
                            await contact.hover()
                            await asyncio.sleep(random.uniform(1, 2))
                    break
                    
        except Exception as e:
            logging.debug(f"Contact info checking failed: {e}")
        
        await asyncio.sleep(duration * 0.3)
    
    async def _evaluate_trust_signals_activity(self, page, duration: float):
        """Evaluate trust signals on the page"""
        
        try:
            # Look for trust indicators
            trust_selectors = [
                ".testimonial", ".certification", ".badge",
                ".secure", ".verified", ".guarantee", ".award"
            ]
            
            for selector in trust_selectors:
                trust_elements = await page.locator(selector + ":visible").all()
                if trust_elements:
                    for element in trust_elements[:2]:
                        if await element.is_visible():
                            await element.hover()
                            await asyncio.sleep(random.uniform(1.5, 3))
                    break
                    
        except Exception as e:
            logging.debug(f"Trust signal evaluation failed: {e}")
        
        await asyncio.sleep(duration * 0.4)
    
    async def _casual_browsing_activity(self, page, duration: float):
        """Casual browsing with quick interactions"""
        
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Quick scroll
            await page.mouse.wheel(0, random.randint(200, 500))
            await asyncio.sleep(random.uniform(1, 2))
            
            # Occasional hover on interesting elements
            if random.random() < 0.5:
                try:
                    elements = await page.locator("img:visible, button:visible, a:visible").all()
                    if elements:
                        element = random.choice(elements[:10])
                        await element.hover()
                        await asyncio.sleep(random.uniform(0.5, 1))
                except:
                    pass
    
    async def _detailed_comparison_activity(self, page, duration: float):
        """Detailed comparison browsing"""
        
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Careful scrolling and examination
            await page.mouse.wheel(0, random.randint(150, 300))
            await asyncio.sleep(random.uniform(2, 4))
            
            # Look for comparison elements
            try:
                comparison_elements = await page.locator(
                    ".compare, .vs, .difference, .feature, .spec"
                ).all()
                
                if comparison_elements:
                    element = random.choice(comparison_elements[:5])
                    if await element.is_visible():
                        await element.hover()
                        await asyncio.sleep(random.uniform(2, 4))
                        
            except:
                pass
    
    async def _general_exploration_activity(self, page, duration: float):
        """General page exploration"""
        
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Mixed scrolling patterns
            scroll_direction = random.choice([1, -1])
            scroll_amount = random.randint(200, 400) * scroll_direction
            
            await page.mouse.wheel(0, scroll_amount)
            await asyncio.sleep(random.uniform(1.5, 3))
            
            # Random element interactions
            if random.random() < 0.4:
                await self._random_element_interaction(page)
    
    async def _quick_scroll_activity(self, page, duration: float):
        """Quick scrolling activity"""
        
        num_scrolls = int(duration / 2)
        
        for _ in range(max(1, num_scrolls)):
            await page.mouse.wheel(0, random.randint(300, 600))
            await asyncio.sleep(random.uniform(1, 2))
    
    async def _hover_elements_activity(self, page, duration: float):
        """Hover over various elements"""
        
        try:
            elements = await page.locator("a:visible, button:visible, img:visible").all()
            
            if elements:
                hover_count = min(int(duration / 3), len(elements))
                
                for _ in range(hover_count):
                    element = random.choice(elements)
                    if await element.is_visible():
                        await element.hover()
                        await asyncio.sleep(random.uniform(2, 4))
                        
        except Exception as e:
            logging.debug(f"Hover activity failed: {e}")
    
    async def _read_snippets_activity(self, page, duration: float):
        """Read text snippets on the page"""
        
        try:
            text_elements = await page.locator("p:visible, .text:visible, .description:visible").all()
            
            if text_elements:
                read_count = min(int(duration / 5), len(text_elements))
                
                for _ in range(read_count):
                    element = random.choice(text_elements)
                    if await element.is_visible():
                        await element.hover()
                        await asyncio.sleep(random.uniform(3, 6))
                        
        except Exception as e:
            logging.debug(f"Reading activity failed: {e}")
    
    async def _default_activity(self, page, duration: float):
        """Default fallback activity"""
        
        await page.mouse.wheel(0, random.randint(200, 400))
        await asyncio.sleep(duration)
    
    async def _random_element_interaction(self, page):
        """Random interaction with page elements"""
        
        try:
            interactive_elements = await page.locator(
                "button:visible, a:visible, input:visible, .clickable:visible"
            ).all()
            
            if interactive_elements:
                element = random.choice(interactive_elements[:5])
                if await element.is_visible():
                    await element.hover()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Small chance to actually click non-destructive elements
                    if random.random() < 0.1:
                        tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
                        if tag_name in ['img', 'span', 'div']:
                            await element.click()
                            await asyncio.sleep(random.uniform(1, 2))
                            
        except Exception as e:
            logging.debug(f"Random interaction failed: {e}")
    
    async def _simulate_careful_reading(self, page):
        """Simulate careful reading with natural mouse movements"""
        
        try:
            viewport = page.viewport_size
            
            # Simulate reading lines with mouse following
            for _ in range(random.randint(3, 6)):
                # Start at left side
                x_start = random.randint(50, 200)
                y = random.randint(200, viewport["height"] - 200)
                
                await page.mouse.move(x_start, y)
                await asyncio.sleep(random.uniform(0.1, 0.3))
                
                # Move across line (reading)
                x_end = x_start + random.randint(300, 600)
                x_end = min(x_end, viewport["width"] - 50)
                
                # Simulate reading movement
                for x in range(x_start, x_end, random.randint(20, 40)):
                    await page.mouse.move(x, y + random.randint(-5, 5))
                    await asyncio.sleep(random.uniform(0.05, 0.15))
                
                # Move to next line
                y += random.randint(20, 40)
                await asyncio.sleep(random.uniform(0.2, 0.5))
                
        except Exception as e:
            logging.debug(f"Reading simulation failed: {e}")
    
    async def _final_page_interaction(self, page, page_context: Dict):
        """Final interaction before leaving the page"""
        
        try:
            # Sometimes scroll back to top
            if random.random() < 0.5:
                await page.keyboard.press("Home")
                await asyncio.sleep(random.uniform(1, 2))
            
            # Sometimes check the URL or page title
            if self.current_persona.tech_comfort == "high" and random.random() < 0.3:
                # Simulate checking URL bar
                await page.keyboard.press("F6")  # Focus address bar
                await asyncio.sleep(random.uniform(1, 2))
                await page.keyboard.press("Escape")  # Unfocus
            
        except Exception as e:
            logging.debug(f"Final interaction failed: {e}")


# ============================================================================
# ENHANCED JSON PROCESSOR WITH AI INTEGRATION
# ============================================================================

class EnhancedJSONSearchProcessor:
    """
    Enhanced JSON processor with AI integration and pattern diversification
    """
    
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.search_simulator = EnhancedGoogleSearchSimulator()
        self.results = []
        self.persona_rotation = list(PersonaManager.PERSONAS.values())
        random.shuffle(self.persona_rotation)
        self.current_persona_index = 0
        
        # Pattern tracking for global diversity
        self.global_pattern_usage = {}
        self.session_history = []
    
    def get_next_persona(self) -> UserPersona:
        """Get next persona in rotation to ensure diversity"""
        
        persona = self.persona_rotation[self.current_persona_index]
        self.current_persona_index = (self.current_persona_index + 1) % len(self.persona_rotation)
        
        # Occasionally shuffle to add more randomness
        if self.current_persona_index == 0:
            random.shuffle(self.persona_rotation)
        
        return persona
    
    async def process_all_enhanced_searches(self, delay_between_searches: int = 180, 
                                          randomize_order: bool = True,
                                          use_dynamic_delays: bool = True) -> Dict[str, Any]:
        """
        Process all searches with enhanced AI integration and pattern diversification
        """
        
        search_data = self.load_search_data()
        
        if randomize_order:
            random.shuffle(search_data)
            logging.info("Randomized search order for pattern diversity")
        
        logging.info(f"Starting {len(search_data)} enhanced AI-driven search simulations")
        logging.info(f"Using {len(self.persona_rotation)} different personas")
        
        all_results = []
        
        for i, search_task in enumerate(search_data):
            keyword = search_task["keyword"]
            site = search_task["site"]
            
            # Select persona for this search
            persona = self.get_next_persona()
            
            logging.info(f"\nSearch {i+1}/{len(search_data)}: '{keyword}' -> {site}")
            logging.info(f"Using persona: {persona.name} ({persona.persona_type.value})")
            
            try:
                # Run enhanced search simulation
                result = await self.search_simulator.simulate_enhanced_search_session(
                    keyword, site, persona
                )
                
                # Add global tracking information
                result["global_session_id"] = i + 1
                result["persona_rotation_index"] = self.current_persona_index
                
                all_results.append(result)
                
                # Log result with AI insights
                if result.get("success"):
                    patterns_used = len(result.get("patterns_used", []))
                    cognitive_final = result.get("final_cognitive_state", {})
                    duration = result.get("duration", 0)
                    
                    logging.info(f"✓ Success: {duration:.1f}s, {patterns_used} patterns")
                    logging.info(f"  Final state: interest={cognitive_final.get('interest_level', 0):.2f}, "
                               f"fatigue={cognitive_final.get('fatigue_level', 0):.2f}")
                else:
                    error = result.get("error", "Unknown error")
                    logging.info(f"✗ Failed: {error}")
                
                # Track global pattern usage
                self._update_global_pattern_tracking(result)
                
            except Exception as e:
                logging.error(f"Enhanced search simulation error: {e}")
                all_results.append({
                    "keyword": keyword,
                    "target_site": site,
                    "persona": {"type": persona.persona_type.value, "name": persona.name},
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "global_session_id": i + 1
                })
            
            # Dynamic delay calculation
            if i < len(search_data) - 1:
                if use_dynamic_delays:
                    delay = self._calculate_dynamic_delay(delay_between_searches, persona, i)
                else:
                    delay = delay_between_searches + random.randint(-30, 30)
                
                logging.info(f"Waiting {delay}s before next search (dynamic scheduling)...")
                await asyncio.sleep(delay)
        
        # Generate comprehensive summary with AI insights
        summary = self._generate_enhanced_summary(all_results)
        
        logging.info(f"\n{'='*50}")
        logging.info(f"ENHANCED PROCESSING COMPLETE")
        logging.info(f"{'='*50}")
        logging.info(f"Success rate: {summary['successful_searches']}/{summary['total_searches']} "
                   f"({summary['success_rate']:.1f}%)")
        logging.info(f"Personas used: {len(set(r.get('persona', {}).get('type', 'unknown') for r in all_results))}")
        logging.info(f"Unique patterns: {len(summary.get('pattern_diversity', {}))}")
        
        self.results = summary
        return summary
    
    def _update_global_pattern_tracking(self, result: Dict):
        """Update global pattern usage tracking"""
        
        patterns_used = result.get("patterns_used", [])
        
        for pattern in patterns_used:
            self.global_pattern_usage[pattern] = self.global_pattern_usage.get(pattern, 0) + 1
        
        # Keep session history for analysis
        self.session_history.append({
            "session_id": result.get("global_session_id", 0),
            "persona_type": result.get("persona", {}).get("type", "unknown"),
            "patterns": patterns_used,
            "success": result.get("success", False),
            "duration": result.get("duration", 0)
        })
    
    def _calculate_dynamic_delay(self, base_delay: int, persona: UserPersona, session_index: int) -> int:
        """Calculate dynamic delay based on persona and session patterns"""
        
        # Base delay with persona characteristics
        persona_multiplier = {
            "slow": 1.2,
            "medium": 1.0,
            "fast": 0.8
        }.get(persona.browsing_speed, 1.0)
        
        # Time of day simulation (some personas more active at different times)
        hour_of_day = (session_index * 0.5) % 24  # Simulate time progression
        
        if persona.persona_type in [UserPersonaType.PROFESSIONAL, UserPersonaType.RESEARCHER]:
            # Business hours preference
            if 9 <= hour_of_day <= 17:
                time_multiplier = 0.9
            else:
                time_multiplier = 1.1
        elif persona.persona_type in [UserPersonaType.STUDENT, UserPersonaType.CASUAL_BROWSER]:
            # Evening preference
            if 18 <= hour_of_day <= 23:
                time_multiplier = 0.9
            else:
                time_multiplier = 1.0
        else:
            time_multiplier = 1.0
        
        # Add some randomness to prevent predictability
        randomness = random.uniform(0.7, 1.3)
        
        final_delay = int(base_delay * persona_multiplier * time_multiplier * randomness)
        
        # Ensure reasonable bounds
        return max(60, min(300, final_delay))
    
    def _generate_enhanced_summary(self, all_results: List[Dict]) -> Dict[str, Any]:
        """Generate enhanced summary with AI insights"""
        
        successful = sum(1 for r in all_results if r.get("success", False))
        
        # Persona performance analysis
        persona_performance = {}
        for result in all_results:
            persona_type = result.get("persona", {}).get("type", "unknown")
            
            if persona_type not in persona_performance:
                persona_performance[persona_type] = {"total": 0, "successful": 0}
            
            persona_performance[persona_type]["total"] += 1
            if result.get("success", False):
                persona_performance[persona_type]["successful"] += 1
        
        # Calculate persona success rates
        for persona_type in persona_performance:
            total = persona_performance[persona_type]["total"]
            successful_p = persona_performance[persona_type]["successful"]
            persona_performance[persona_type]["success_rate"] = (successful_p / total * 100) if total > 0 else 0
        
        # Pattern diversity analysis
        pattern_diversity = {}
        for session in self.session_history:
            for pattern in session.get("patterns", []):
                pattern_diversity[pattern] = pattern_diversity.get(pattern, 0) + 1
        
        # Cognitive journey analysis
        cognitive_insights = self._analyze_cognitive_journeys(all_results)
        
        # Timing analysis
        timing_analysis = self._analyze_timing_patterns(all_results)
        
        summary = {
            "total_searches": len(all_results),
            "successful_searches": successful,
            "success_rate": (successful / len(all_results)) * 100 if all_results else 0,
            "persona_performance": persona_performance,
            "pattern_diversity": pattern_diversity,
            "cognitive_insights": cognitive_insights,
            "timing_analysis": timing_analysis,
            "ai_enhancement_metrics": {
                "avg_patterns_per_session": sum(len(r.get("patterns_used", [])) for r in all_results) / len(all_results) if all_results else 0,
                "unique_personas_used": len(set(r.get("persona", {}).get("type", "unknown") for r in all_results)),
                "cognitive_diversity_score": self._calculate_cognitive_diversity_score(all_results)
            },
            "results": all_results,
            "processing_time": datetime.now().isoformat(),
            "enhancement_version": "USimAgent + AutoWebGLM v1.0"
        }
        
        return summary
    
    def _analyze_cognitive_journeys(self, results: List[Dict]) -> Dict[str, Any]:
        """Analyze cognitive journeys across all sessions"""
        
        insights = {
            "avg_final_interest": 0,
            "avg_final_fatigue": 0,
            "emotional_state_distribution": {},
            "cognitive_load_patterns": {}
        }
        
        valid_results = [r for r in results if r.get("final_cognitive_state")]
        
        if not valid_results:
            return insights
        
        # Calculate averages
        total_interest = sum(r["final_cognitive_state"].get("interest_level", 0) for r in valid_results)
        total_fatigue = sum(r["final_cognitive_state"].get("fatigue_level", 0) for r in valid_results)
        
        insights["avg_final_interest"] = total_interest / len(valid_results)
        insights["avg_final_fatigue"] = total_fatigue / len(valid_results)
        
        # Emotional state distribution
        for result in valid_results:
            emotion = result["final_cognitive_state"].get("emotional_state", "unknown")
            insights["emotional_state_distribution"][emotion] = insights["emotional_state_distribution"].get(emotion, 0) + 1
        
        # Cognitive load patterns
        for result in valid_results:
            load = result["final_cognitive_state"].get("cognitive_load", 0)
            load_category = "low" if load < 0.3 else "medium" if load < 0.7 else "high"
            insights["cognitive_load_patterns"][load_category] = insights["cognitive_load_patterns"].get(load_category, 0) + 1
        
        return insights
    
    def _analyze_timing_patterns(self, results: List[Dict]) -> Dict[str, Any]:
        """Analyze timing patterns across sessions"""
        
        durations = [r.get("duration", 0) for r in results if r.get("duration")]
        
        if not durations:
            return {}
        
        return {
            "avg_session_duration": sum(durations) / len(durations),
            "min_session_duration": min(durations),
            "max_session_duration": max(durations),
            "duration_std_dev": np.std(durations) if durations else 0,
            "timing_diversity_score": len(set(int(d/30) for d in durations)) / len(durations) if durations else 0
        }
    
    def _calculate_cognitive_diversity_score(self, results: List[Dict]) -> float:
        """Calculate cognitive diversity score (0-1, higher is more diverse)"""
        
        if not results:
            return 0.0
        
        # Factors contributing to cognitive diversity
        factors = []
        
        # Persona diversity
        unique_personas = len(set(r.get("persona", {}).get("type", "unknown") for r in results))
        persona_diversity = unique_personas / len(PersonaManager.PERSONAS)
        factors.append(persona_diversity)
        
        # Pattern diversity
        all_patterns = []
        for r in results:
            all_patterns.extend(r.get("patterns_used", []))
        
        if all_patterns:
            unique_patterns = len(set(all_patterns))
            pattern_diversity = min(1.0, unique_patterns / 20)  # Normalize against expected max
            factors.append(pattern_diversity)
        
        # Emotional state diversity
        emotions = [r.get("final_cognitive_state", {}).get("emotional_state", "unknown") for r in results]
        unique_emotions = len(set(emotions))
        emotion_diversity = unique_emotions / 5  # 5 main emotional states
        factors.append(emotion_diversity)
        
        # Duration diversity
        durations = [r.get("duration", 0) for r in results if r.get("duration")]
        if durations:
            duration_ranges = len(set(int(d/60) for d in durations))  # Group by minute
            duration_diversity = min(1.0, duration_ranges / 10)  # Normalize
            factors.append(duration_diversity)
        
        return sum(factors) / len(factors) if factors else 0.0
    
    def load_search_data(self) -> List[Dict[str, str]]:
        """Load search data from JSON file with enhanced validation"""
        
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logging.info(f"Loaded {len(data)} search tasks from {self.json_file_path}")
            
            # Enhanced validation
            validated_data = []
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    logging.warning(f"Skipping invalid item at index {i}: not a dict")
                    continue
                
                if "keyword" not in item or "site" not in item:
                    logging.warning(f"Skipping invalid item at index {i}: missing required fields")
                    continue
                
                if not item["keyword"].strip() or not item["site"].strip():
                    logging.warning(f"Skipping invalid item at index {i}: empty fields")
                    continue
                
                validated_data.append(item)
            
            logging.info(f"Validated {len(validated_data)} search tasks")
            return validated_data
            
        except FileNotFoundError:
            logging.error(f"File not found: {self.json_file_path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format: {e}")
            raise
        except Exception as e:
            logging.error(f"Error loading search data: {e}")
            raise
    
    def save_enhanced_results(self, output_file: str):
        """Save enhanced results with comprehensive data"""
        
        if not self.results:
            logging.warning("No results to save")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
            
            logging.info(f"Enhanced results saved to {output_file}")
            
            # Also save a summary report
            summary_file = output_file.replace('.json', '_summary.txt')
            self._save_summary_report(summary_file)
            
        except Exception as e:
            logging.error(f"Failed to save enhanced results: {e}")
    
    def _save_summary_report(self, summary_file: str):
        """Save human-readable summary report"""
        
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("ENHANCED GOOGLE SEARCH SIMULATOR - AI INTEGRATION REPORT\n")
                f.write("=" * 60 + "\n\n")
                
                # Overall statistics
                f.write(f"Total Searches: {self.results['total_searches']}\n")
                f.write(f"Successful: {self.results['successful_searches']}\n")
                f.write(f"Success Rate: {self.results['success_rate']:.1f}%\n\n")
                
                # AI Enhancement Metrics
                ai_metrics = self.results.get('ai_enhancement_metrics', {})
                f.write("AI ENHANCEMENT METRICS:\n")
                f.write("-" * 25 + "\n")
                f.write(f"Average Patterns per Session: {ai_metrics.get('avg_patterns_per_session', 0):.1f}\n")
                f.write(f"Unique Personas Used: {ai_metrics.get('unique_personas_used', 0)}\n")
                f.write(f"Cognitive Diversity Score: {ai_metrics.get('cognitive_diversity_score', 0):.3f}\n\n")
                
                # Persona Performance
                f.write("PERSONA PERFORMANCE:\n")
                f.write("-" * 20 + "\n")
                persona_perf = self.results.get('persona_performance', {})
                for persona_type, stats in persona_perf.items():
                    f.write(f"{persona_type}: {stats['successful']}/{stats['total']} "
                           f"({stats['success_rate']:.1f}%)\n")
                f.write("\n")
                
                # Cognitive Insights
                cognitive = self.results.get('cognitive_insights', {})
                f.write("COGNITIVE INSIGHTS:\n")
                f.write("-" * 18 + "\n")
                f.write(f"Average Final Interest: {cognitive.get('avg_final_interest', 0):.3f}\n")
                f.write(f"Average Final Fatigue: {cognitive.get('avg_final_fatigue', 0):.3f}\n")
                
                emotion_dist = cognitive.get('emotional_state_distribution', {})
                f.write("\nEmotional State Distribution:\n")
                for emotion, count in emotion_dist.items():
                    f.write(f"  {emotion}: {count}\n")
                
                # Timing Analysis
                timing = self.results.get('timing_analysis', {})
                f.write(f"\nTIMING ANALYSIS:\n")
                f.write("-" * 16 + "\n")
                f.write(f"Average Session Duration: {timing.get('avg_session_duration', 0):.1f}s\n")
                f.write(f"Duration Range: {timing.get('min_session_duration', 0):.1f}s - {timing.get('max_session_duration', 0):.1f}s\n")
                f.write(f"Timing Diversity Score: {timing.get('timing_diversity_score', 0):.3f}\n")
                
                # Pattern Diversity
                patterns = self.results.get('pattern_diversity', {})
                f.write(f"\nPATTERN DIVERSITY ({len(patterns)} unique patterns):\n")
                f.write("-" * 25 + "\n")
                sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
                for pattern, count in sorted_patterns[:10]:  # Top 10
                    f.write(f"  {pattern}: {count}\n")
                
                f.write(f"\nReport generated: {datetime.now().isoformat()}\n")
                f.write(f"Enhancement Version: {self.results.get('enhancement_version', 'Unknown')}\n")
            
            logging.info(f"Summary report saved to {summary_file}")
            
        except Exception as e:
            logging.error(f"Failed to save summary report: {e}")


# ============================================================================
# MAIN FUNCTION WITH ENHANCED CLI
# ============================================================================

def setup_enhanced_logging():
    """Setup enhanced logging for AI integration"""
    
    # Create custom formatter
    class EnhancedFormatter(logging.Formatter):
        def format(self, record):
            msg = super().format(record)
            
            # Enhanced emoji/symbol replacements
            replacements = {
                '🔍': '[SEARCH]', '🎭': '[PERSONA]', '🧠': '[AI]', '⚡': '[ENHANCED]',
                '🌐': '[WEB]', '⌨️': '[TYPE]', '👀': '[SCAN]', '🖱️': '[MOUSE]',
                '🎯': '[TARGET]', '✅': '[SUCCESS]', '❌': '[FAIL]', '⚠️': '[WARN]',
                '⏳': '[WAIT]', '📍': '[POS]', '📄': '[PAGE]', '💭': '[COGNITIVE]',
                '🔄': '[BACK]', '🚀': '[START]', '📊': '[ANALYTICS]', '🎉': '[COMPLETE]',
                '⏱️': '[TIME]', '🧪': '[AI-TEST]', '📂': '[DATA]', '💾': '[SAVE]',
                '🔀': '[PATTERN]', '🎪': '[BEHAVIOR]', '🎨': '[DIVERSE]'
            }
            
            for emoji, replacement in replacements.items():
                msg = msg.replace(emoji, replacement)
            
            return msg
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('enhanced_search_simulator.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )
    
    for handler in logging.getLogger().handlers:
        handler.setFormatter(EnhancedFormatter('%(asctime)s - %(levelname)s - %(message)s'))

async def main():
    """Enhanced main function with AI integration"""
    
    setup_enhanced_logging()
    
    parser = argparse.ArgumentParser(
        description="Enhanced Google Search Simulator with USimAgent and AutoWebGLM Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Enhanced Features:
  • USimAgent cognitive modeling for realistic human behavior
  • AutoWebGLM intelligent web automation and context analysis
  • Dynamic persona rotation for pattern diversification
  • Advanced behavioral pattern selection and tracking
  • Cognitive journey analysis and emotional state modeling
  • Intelligent timing and delay calculations
  • Comprehensive AI-driven activity planning

Examples:
  python enhanced_simulator.py search_data.json
  python enhanced_simulator.py search_data.json --delay 300 --output results.json --dynamic-delays
  python enhanced_simulator.py --single "best laptops 2024" "https://www.example.com" --persona researcher
        """
    )
    
    parser.add_argument("json_file", nargs='?', help="JSON file containing keyword-site pairs")
    parser.add_argument("--delay", type=int, default=180, help="Base delay between searches in seconds")
    parser.add_argument("--output", type=str, help="Output file to save results")
    parser.add_argument("--randomize", action="store_true", help="Randomize order of searches")
    parser.add_argument("--dynamic-delays", action="store_true", help="Use dynamic delay calculation")
    parser.add_argument("--single", nargs=2, metavar=("KEYWORD", "SITE"), help="Run single search")
    parser.add_argument("--persona", choices=[p.value for p in UserPersonaType], help="Specific persona for single search")
    parser.add_argument("--test-personas", action="store_true", help="Test all personas with a sample search")
    parser.add_argument("--analyze-patterns", action="store_true", help="Analyze pattern diversity without running searches")
    
    args = parser.parse_args()
    
    print("🚀 ENHANCED GOOGLE SEARCH SIMULATOR - AI INTEGRATION")
    print("=" * 60)
    print("🧠 Features: USimAgent + AutoWebGLM Integration")
    print("🎭 Persona-driven behavior with cognitive modeling")
    print("🔀 Advanced pattern diversification")
    print("📊 Comprehensive analytics and insights")
    print("=" * 60)
    
    try:
        if args.test_personas:
            # Test all personas
            print("🧪 Testing all personas with sample search...")
            await test_all_personas()
            
        elif args.analyze_patterns:
            # Analyze existing results
            if args.output and os.path.exists(args.output):
                analyze_existing_patterns(args.output)
            else:
                print("❌ No results file found for pattern analysis")
                
        elif args.single:
            # Single search mode
            keyword, site = args.single
            print(f"🎯 Single enhanced search mode")
            print(f"Keyword: {keyword}")
            print(f"Site: {site}")
            
            # Select persona
            if args.persona:
                persona_type = UserPersonaType(args.persona)
                persona = PersonaManager.get_persona_by_type(persona_type)
                print(f"🎭 Using specified persona: {persona.name}")
            else:
                persona = PersonaManager.get_random_persona()
                print(f"🎭 Using random persona: {persona.name}")
            
            # Create enhanced simulator
            simulator = EnhancedGoogleSearchSimulator()
            result = await simulator.simulate_enhanced_search_session(keyword, site, persona)
            
            print(f"\n🎉 RESULT: {'✅ SUCCESS' if result.get('success') else '❌ FAILED'}")
            
            if result.get('success'):
                patterns_used = len(result.get('patterns_used', []))
                cognitive_state = result.get('final_cognitive_state', {})
                print(f"📊 Patterns used: {patterns_used}")
                print(f"🧠 Final cognitive state: {cognitive_state.get('emotional_state', 'unknown')}")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, default=str, ensure_ascii=False)
                print(f"💾 Result saved to {args.output}")
        
        else:
            # Batch processing mode
            if not args.json_file:
                print("❌ JSON file required for batch processing")
                return
                
            print(f"📂 Input file: {args.json_file}")
            print(f"⏱️ Base delay: {args.delay}s")
            print(f"🔀 Randomize order: {args.randomize}")
            print(f"⚡ Dynamic delays: {args.dynamic_delays}")
            
            # Create enhanced processor
            processor = EnhancedJSONSearchProcessor(args.json_file)
            
            # Process all searches with AI enhancement
            results = await processor.process_all_enhanced_searches(
                delay_between_searches=args.delay,
                randomize_order=args.randomize,
                use_dynamic_delays=args.dynamic_delays
            )
            
            # Print enhanced summary
            print(f"\n🎉 ENHANCED PROCESSING COMPLETE")
            print(f"📊 Results: {results['successful_searches']}/{results['total_searches']} "
                  f"({results['success_rate']:.1f}% success)")
            
            ai_metrics = results.get('ai_enhancement_metrics', {})
            print(f"🧠 AI Metrics:")
            print(f"   • Cognitive Diversity: {ai_metrics.get('cognitive_diversity_score', 0):.3f}")
            print(f"   • Avg Patterns/Session: {ai_metrics.get('avg_patterns_per_session', 0):.1f}")
            print(f"   • Unique Personas: {ai_metrics.get('unique_personas_used', 0)}")
            
            # Save enhanced results
            if args.output:
                processor.save_enhanced_results(args.output)
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logging.error(f"Main execution error: {e}")

async def test_all_personas():
    """Test all personas with a sample search"""
    
    test_keyword = "best productivity software 2024"
    test_site = "https://www.example.com"
    
    simulator = EnhancedGoogleSearchSimulator()
    
    print(f"Testing {len(PersonaManager.PERSONAS)} personas:")
    
    for persona_type, persona in PersonaManager.PERSONAS.items():
        print(f"\n🎭 Testing {persona.name} ({persona_type.value})...")
        
        try:
            result = await simulator.simulate_enhanced_search_session(
                test_keyword, test_site, persona
            )
            
            success = result.get('success', False)
            patterns = len(result.get('patterns_used', []))
            cognitive = result.get('final_cognitive_state', {})
            
            print(f"   {'✅' if success else '❌'} Success: {success}")
            print(f"   🔀 Patterns: {patterns}")
            print(f"   🧠 Emotion: {cognitive.get('emotional_state', 'unknown')}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")

def analyze_existing_patterns(results_file: str):
    """Analyze patterns from existing results file"""
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Analyzing patterns from {results_file}")
        
        # Extract pattern information
        all_patterns = []
        for result in data.get('results', []):
            all_patterns.extend(result.get('patterns_used', []))
        
        if all_patterns:
            pattern_counts = {}
            for pattern in all_patterns:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
            print(f"\n🔀 Pattern Analysis:")
            print(f"   Total patterns used: {len(all_patterns)}")
            print(f"   Unique patterns: {len(pattern_counts)}")
            
            print(f"\n   Top 10 most used patterns:")
            sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
            for i, (pattern, count) in enumerate(sorted_patterns[:10], 1):
                print(f"   {i:2d}. {pattern}: {count}")
        
        else:
            print("❌ No pattern data found in results file")
            
    except Exception as e:
        print(f"❌ Pattern analysis failed: {e}")

# ============================================================================
# BEHAVIOR TREE INTEGRATION FOR USIMAGENT
# ============================================================================

class BehaviorNode:
    """Base class for behavior tree nodes"""
    
    def __init__(self, name: str):
        self.name = name
        self.children = []
    
    async def execute(self, context: Dict) -> str:
        """Execute the behavior node. Returns: SUCCESS, FAILURE, RUNNING"""
        raise NotImplementedError

class SequenceNode(BehaviorNode):
    """Execute children in sequence until one fails"""
    
    async def execute(self, context: Dict) -> str:
        for child in self.children:
            result = await child.execute(context)
            if result != "SUCCESS":
                return result
        return "SUCCESS"

class SelectorNode(BehaviorNode):
    """Execute children until one succeeds"""
    
    async def execute(self, context: Dict) -> str:
        for child in self.children:
            result = await child.execute(context)
            if result == "SUCCESS":
                return result
        return "FAILURE"

class ActionNode(BehaviorNode):
    """Leaf node that performs an action"""
    
    def __init__(self, name: str, action_func):
        super().__init__(name)
        self.action_func = action_func
    
    async def execute(self, context: Dict) -> str:
        try:
            await self.action_func(context)
            return "SUCCESS"
        except Exception as e:
            logging.debug(f"Action {self.name} failed: {e}")
            return "FAILURE"

class ConditionNode(BehaviorNode):
    """Check a condition"""
    
    def __init__(self, name: str, condition_func):
        super().__init__(name)
        self.condition_func = condition_func
    
    async def execute(self, context: Dict) -> str:
        try:
            if await self.condition_func(context):
                return "SUCCESS"
            return "FAILURE"
        except Exception as e:
            logging.debug(f"Condition {self.name} failed: {e}")
            return "FAILURE"

# ============================================================================
# ENHANCED USIMAGENT WITH BEHAVIOR TREES
# ============================================================================

class EnhancedUSimAgent(USimAgent):
    """Enhanced USimAgent with behavior trees and LLM-powered decision making"""
    
    def __init__(self, persona: UserPersona):
        super().__init__(persona)
        self.behavior_tree = self._build_behavior_tree()
        self.action_history = []
        self.noise_injection_rate = 0.15  # 15% chance of noise actions
        
    def _build_behavior_tree(self) -> BehaviorNode:
        """Build dynamic behavior tree based on persona"""
        
        root = SelectorNode("RootBehavior")
        
        # Main browsing sequence
        main_sequence = SequenceNode("MainBrowsingSequence")
        
        # Navigation behavior
        navigation_selector = SelectorNode("NavigationBehavior")
        navigation_selector.children = [
            ActionNode("DirectNavigation", self._direct_navigation),
            ActionNode("ExploratoryNavigation", self._exploratory_navigation)
        ]
        
        # Content interaction behavior
        content_sequence = SequenceNode("ContentInteraction")
        content_sequence.children = [
            ActionNode("AnalyzePage", self._analyze_page_content),
            ActionNode("PlanInteractions", self._plan_interactions),
            ActionNode("ExecuteInteractions", self._execute_planned_interactions)
        ]
        
        # Noise injection (random actions)
        noise_selector = SelectorNode("NoiseInjection")
        noise_selector.children = [
            ConditionNode("ShouldInjectNoise", self._should_inject_noise),
            ActionNode("InjectNoiseAction", self._inject_noise_action)
        ]
        
        main_sequence.children = [navigation_selector, content_sequence, noise_selector]
        root.children = [main_sequence]
        
        return root
    
    async def execute_behavior_tree(self, context: Dict):
        """Execute the behavior tree with given context"""
        
        result = await self.behavior_tree.execute(context)
        self.action_history.append({
            "timestamp": time.time(),
            "result": result,
            "cognitive_state": {
                "load": self.cognitive_load,
                "fatigue": self.fatigue_level,
                "interest": self.interest_level
            }
        })
        return result
    
    async def _direct_navigation(self, context: Dict):
        """Direct navigation behavior"""
        page = context.get("page")
        target_url = context.get("target_url")
        
        if page and target_url:
            await page.goto(target_url, wait_until='networkidle')
            await asyncio.sleep(random.uniform(1, 3))
    
    async def _exploratory_navigation(self, context: Dict):
        """Exploratory navigation with intermediate steps"""
        page = context.get("page")
        
        if page:
            # Add some exploratory behavior before reaching target
            await page.mouse.wheel(0, random.randint(100, 300))
            await asyncio.sleep(random.uniform(2, 4))
    
    async def _analyze_page_content(self, context: Dict):
        """Analyze current page content"""
        page = context.get("page")
        
        if page:
            # Simulate content analysis time
            analysis_time = self._calculate_analysis_time()
            await asyncio.sleep(analysis_time)
            
            # Store analysis results in context
            context["page_analyzed"] = True
    
    def _calculate_analysis_time(self) -> float:
        """Calculate time needed for page analysis based on persona"""
        
        base_time = {
            "slow": random.uniform(3, 8),
            "medium": random.uniform(2, 5),
            "fast": random.uniform(1, 3)
        }[self.persona.browsing_speed]
        
        # Adjust for cognitive state
        cognitive_modifier = 1 + self.cognitive_load * 0.5
        attention_modifier = 2 - self.interest_level
        
        return base_time * cognitive_modifier * attention_modifier
    
    async def _plan_interactions(self, context: Dict):
        """Plan interactions based on page content and goals"""
        
        # Simulate planning process
        planning_time = random.uniform(0.5, 2)
        await asyncio.sleep(planning_time)
        
        # Generate interaction plan (simplified)
        context["interaction_plan"] = [
            {"action": "scroll", "amount": random.randint(200, 500)},
            {"action": "hover", "target": "random_element"},
            {"action": "click", "target": "target_element"}
        ]
    
    async def _execute_planned_interactions(self, context: Dict):
        """Execute the planned interactions"""
        
        plan = context.get("interaction_plan", [])
        page = context.get("page")
        
        if not page:
            return
        
        for action in plan:
            try:
                if action["action"] == "scroll":
                    await page.mouse.wheel(0, action["amount"])
                    await asyncio.sleep(random.uniform(1, 3))
                
                elif action["action"] == "hover":
                    # Find a random element to hover
                    elements = await page.locator("a:visible, button:visible").all()
                    if elements:
                        element = random.choice(elements[:5])
                        await element.hover()
                        await asyncio.sleep(random.uniform(1, 2))
                
                elif action["action"] == "click":
                    # This would be replaced with actual target clicking logic
                    pass
                    
            except Exception as e:
                logging.debug(f"Interaction execution failed: {e}")
    
    async def _should_inject_noise(self, context: Dict) -> bool:
        """Determine if noise should be injected"""
        return random.random() < self.noise_injection_rate
    
    async def _inject_noise_action(self, context: Dict):
        """Inject a noise action to make behavior less predictable"""
        
        page = context.get("page")
        if not page:
            return
        
        noise_actions = [
            self._noise_random_scroll,
            self._noise_hover_random_element,
            self._noise_right_click,
            self._noise_selection_action,
            self._noise_tab_navigation,
            self._noise_zoom_action
        ]
        
        noise_action = random.choice(noise_actions)
        try:
            await noise_action(page)
        except Exception as e:
            logging.debug(f"Noise action failed: {e}")
    
    async def _noise_random_scroll(self, page):
        """Random scroll noise action"""
        direction = random.choice([1, -1])
        amount = random.randint(50, 200) * direction
        await page.mouse.wheel(0, amount)
        await asyncio.sleep(random.uniform(0.5, 1.5))
    
    async def _noise_hover_random_element(self, page):
        """Hover over a random element briefly"""
        try:
            elements = await page.locator("*:visible").all()
            if elements:
                element = random.choice(elements[:20])
                await element.hover()
                await asyncio.sleep(random.uniform(0.3, 1))
        except:
            pass
    
    async def _noise_right_click(self, page):
        """Random right-click action"""
        viewport = page.viewport_size
        x = random.randint(100, viewport["width"] - 100)
        y = random.randint(100, viewport["height"] - 100)
        
        await page.mouse.click(x, y, button="right")
        await asyncio.sleep(random.uniform(0.5, 1))
        await page.keyboard.press("Escape")  # Close context menu
    
    async def _noise_selection_action(self, page):
        """Random text selection action"""
        try:
            text_elements = await page.locator("p:visible, span:visible, div:visible").all()
            if text_elements:
                element = random.choice(text_elements[:10])
                await element.dblclick()  # Select word
                await asyncio.sleep(random.uniform(0.5, 1))
                await page.keyboard.press("Escape")  # Deselect
        except:
            pass
    
    async def _noise_tab_navigation(self, page):
        """Random tab navigation simulation"""
        tab_presses = random.randint(1, 3)
        for _ in range(tab_presses):
            await page.keyboard.press("Tab")
            await asyncio.sleep(random.uniform(0.2, 0.5))
    
    async def _noise_zoom_action(self, page):
        """Random zoom action"""
        if random.random() < 0.5:
            # Zoom in
            await page.keyboard.press("Control++")
        else:
            # Zoom out
            await page.keyboard.press("Control+-")
        
        await asyncio.sleep(random.uniform(0.5, 1))
        # Reset zoom
        await page.keyboard.press("Control+0")

# ============================================================================
# LLM-POWERED AUTOWEBGLM ENHANCEMENT
# ============================================================================

class LLMPoweredAutoWebGLM(AutoWebGLM):
    """Enhanced AutoWebGLM with LLM-powered decision making"""
    
    def __init__(self, persona: UserPersona, llm_client=None):
        super().__init__(persona)
        self.llm_client = llm_client
        self.action_templates = self._load_action_templates()
        self.adaptation_history = []
    
    def _load_action_templates(self) -> Dict[str, List[Dict]]:
        """Load action templates for different scenarios"""
        
        return {
            "search_scenario": [
                {"action": "navigate", "target": "search_engine"},
                {"action": "type", "target": "search_box", "text": "{query}"},
                {"action": "pause", "duration_range": (1, 3)},
                {"action": "press_key", "key": "Enter"},
                {"action": "analyze_results", "duration_range": (3, 8)},
                {"action": "click", "target": "target_result"}
            ],
            "ecommerce_scenario": [
                {"action": "scroll", "pattern": "product_scan", "duration_range": (5, 15)},
                {"action": "hover", "target": "product_images"},
                {"action": "click", "target": "product_details"},
                {"action": "scroll", "pattern": "detail_read", "duration_range": (10, 30)},
                {"action": "check_reviews", "duration_range": (5, 20)}
            ],
            "content_scenario": [
                {"action": "scroll", "pattern": "reading", "duration_range": (15, 60)},
                {"action": "hover", "target": "article_links"},
                {"action": "pause", "duration_range": (2, 5)},
                {"action": "scroll", "pattern": "skim", "duration_range": (5, 15)}
            ]
        }
    
    async def generate_adaptive_plan(self, goal: str, context: Dict) -> List[Dict]:
        """Generate adaptive plan using LLM or rule-based logic"""
        
        # Determine scenario type
        scenario_type = self._classify_scenario(goal, context)
        
        # Get base template
        base_plan = self.action_templates.get(scenario_type, self.action_templates["search_scenario"])
        
        # Adapt plan based on persona and context
        adapted_plan = self._adapt_plan_to_persona(base_plan.copy(), context)
        
        # Add randomization and noise
        final_plan = self._add_plan_variations(adapted_plan)
        
        return final_plan
    
    def _classify_scenario(self, goal: str, context: Dict) -> str:
        """Classify the scenario based on goal and context"""
        
        goal_lower = goal.lower()
        page_type = context.get("page_type", "unknown")
        
        if "buy" in goal_lower or "purchase" in goal_lower or page_type == "ecommerce":
            return "ecommerce_scenario"
        elif "read" in goal_lower or "article" in goal_lower or page_type == "content/blog":
            return "content_scenario"
        else:
            return "search_scenario"
    
    def _adapt_plan_to_persona(self, plan: List[Dict], context: Dict) -> List[Dict]:
        """Adapt plan based on persona characteristics"""
        
        for action in plan:
            # Adjust timing based on browsing speed
            if "duration_range" in action:
                min_dur, max_dur = action["duration_range"]
                
                speed_multiplier = {
                    "slow": 1.5,
                    "medium": 1.0,
                    "fast": 0.7
                }[self.persona.browsing_speed]
                
                action["duration_range"] = (
                    int(min_dur * speed_multiplier),
                    int(max_dur * speed_multiplier)
                )
            
            # Adjust actions based on tech comfort
            if self.persona.tech_comfort == "low":
                # Add more hesitation and exploration
                if action.get("action") == "click":
                    action["hesitation"] = True
            elif self.persona.tech_comfort == "high":
                # Add more efficient shortcuts
                if action.get("action") == "navigate":
                    action["use_shortcuts"] = True
        
        return plan
    
    def _add_plan_variations(self, plan: List[Dict]) -> List[Dict]:
        """Add variations to prevent predictable patterns"""
        
        # Randomly insert noise actions
        for i in range(len(plan)):
            if random.random() < 0.2:  # 20% chance
                noise_action = {
                    "action": "noise",
                    "type": random.choice(["hover_random", "scroll_adjust", "pause_think"])
                }
                plan.insert(i, noise_action)
        
        # Randomly adjust action order (where appropriate)
        if len(plan) > 3:
            # Swap some non-critical actions
            for _ in range(random.randint(0, 2)):
                idx1, idx2 = random.sample(range(1, len(plan) - 1), 2)
                if self._can_swap_actions(plan[idx1], plan[idx2]):
                    plan[idx1], plan[idx2] = plan[idx2], plan[idx1]
        
        return plan
    
    def _can_swap_actions(self, action1: Dict, action2: Dict) -> bool:
        """Check if two actions can be safely swapped"""
        
        # Don't swap critical sequence actions
        critical_actions = ["navigate", "type", "press_key"]
        
        return (action1.get("action") not in critical_actions and 
                action2.get("action") not in critical_actions)
    
    async def adapt_based_on_feedback(self, plan: List[Dict], execution_feedback: Dict):
        """Adapt future plans based on execution feedback"""
        
        self.adaptation_history.append({
            "plan": plan,
            "feedback": execution_feedback,
            "timestamp": time.time()
        })
        
        # Simple adaptation logic
        if execution_feedback.get("success_rate", 0) < 0.5:
            # Increase hesitation and analysis time
            self.action_templates = self._increase_caution_in_templates()
        elif execution_feedback.get("success_rate", 0) > 0.9:
            # Increase efficiency
            self.action_templates = self._increase_efficiency_in_templates()
    
    def _increase_caution_in_templates(self) -> Dict[str, List[Dict]]:
        """Modify templates to be more cautious"""
        
        modified_templates = {}
        for scenario, template in self.action_templates.items():
            modified_template = []
            for action in template:
                modified_action = action.copy()
                if "duration_range" in modified_action:
                    min_dur, max_dur = modified_action["duration_range"]
                    modified_action["duration_range"] = (
                        int(min_dur * 1.2),
                        int(max_dur * 1.2)
                    )
                modified_template.append(modified_action)
            modified_templates[scenario] = modified_template
        
        return modified_templates
    
    def _increase_efficiency_in_templates(self) -> Dict[str, List[Dict]]:
        """Modify templates to be more efficient"""
        
        modified_templates = {}
        for scenario, template in self.action_templates.items():
            modified_template = []
            for action in template:
                modified_action = action.copy()
                if "duration_range" in modified_action:
                    min_dur, max_dur = modified_action["duration_range"]
                    modified_action["duration_range"] = (
                        max(1, int(min_dur * 0.8)),
                        max(2, int(max_dur * 0.8))
                    )
                modified_template.append(modified_action)
            modified_templates[scenario] = modified_template
        
        return modified_templates

# ============================================================================
# FINGERPRINT RESISTANCE AND TESTING UTILITIES
# ============================================================================

class FingerprintResistance:
    """Utilities for avoiding detection and testing uniqueness"""
    
    @staticmethod
    def generate_unique_browser_config() -> Dict[str, Any]:
        """Generate unique browser configuration to avoid fingerprinting"""
        
        # Rotate through realistic configurations
        configs = [
            {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "viewport": {"width": 1920, "height": 1080},
                "device_scale_factor": 1,
                "timezone": "America/New_York",
                "locale": "en-US"
            },
            {
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "viewport": {"width": 1440, "height": 900},
                "device_scale_factor": 2,
                "timezone": "America/Los_Angeles",
                "locale": "en-US"
            },
            {
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                "viewport": {"width": 1366, "height": 768},
                "device_scale_factor": 1,
                "timezone": "America/Chicago",
                "locale": "en-US"
            }
        ]
        
        config = random.choice(configs)
        
        # Add randomization
        config["viewport"]["width"] += random.randint(-50, 50)
        config["viewport"]["height"] += random.randint(-50, 50)
        
        return config
    
    @staticmethod
    def inject_realistic_network_delays():
        """Inject realistic network delays to simulate human internet usage"""
        
        # Simulate network conditions
        network_conditions = [
            {"delay": 0, "description": "Fast connection"},
            {"delay": random.uniform(0.1, 0.3), "description": "Normal connection"},
            {"delay": random.uniform(0.3, 0.8), "description": "Slow connection"},
            {"delay": random.uniform(0.8, 2.0), "description": "Very slow connection"}
        ]
        
        condition = random.choices(
            network_conditions,
            weights=[0.3, 0.5, 0.15, 0.05]  # Most people have decent internet
        )[0]
        
        if condition["delay"] > 0:
            time.sleep(condition["delay"])
        
        return condition
    
    @staticmethod
    async def test_bot_detection_score(page) -> float:
        """Test how bot-like the current session appears"""
        
        try:
            # Inject a simple bot detection test
            score = await page.evaluate("""
                () => {
                    let score = 0;
                    
                    // Check for webdriver
                    if (navigator.webdriver) score += 0.3;
                    
                    // Check for automation indicators
                    if (window.chrome && window.chrome.runtime && window.chrome.runtime.onConnect) {
                        score += 0.2;
                    }
                    
                    // Check mouse movement history
                    if (window.mouseTracker && window.mouseTracker.movements.length < 10) {
                        score += 0.2;
                    }
                    
                    // Check timing patterns
                    if (window.mouseTracker && window.mouseTracker.movements.length > 5) {
                        const movements = window.mouseTracker.movements;
                        const intervals = [];
                        for (let i = 1; i < movements.length; i++) {
                            intervals.push(movements[i].time - movements[i-1].time);
                        }
                        
                        // Check for too regular timing
                        const avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
                        const variance = intervals.reduce((sum, interval) => sum + Math.pow(interval - avgInterval, 2), 0) / intervals.length;
                        
                        if (variance < 100) { // Too regular
                            score += 0.3;
                        }
                    }
                    
                    return Math.min(1.0, score);
                }
            """)
            
            return score
            
        except Exception as e:
            logging.debug(f"Bot detection test failed: {e}")
            return 0.5  # Unknown score

class SessionUniquenessAnalyzer:
    """Analyze and ensure session uniqueness"""
    
    def __init__(self):
        self.session_fingerprints = []
    
    def generate_session_fingerprint(self, session_data: Dict) -> str:
        """Generate a fingerprint for a session"""
        
        # Extract key characteristics
        characteristics = {
            "persona_type": session_data.get("persona", {}).get("type", "unknown"),
            "patterns_used": sorted(session_data.get("patterns_used", [])),
            "duration_bucket": int(session_data.get("duration", 0) / 30),  # 30-second buckets
            "steps_count": len(session_data.get("steps", [])),
            "cognitive_final": session_data.get("final_cognitive_state", {}).get("emotional_state", "unknown")
        }
        
        # Create hash
        import hashlib
        fingerprint_str = json.dumps(characteristics, sort_keys=True)
        fingerprint = hashlib.md5(fingerprint_str.encode()).hexdigest()[:16]
        
        return fingerprint
    
    def calculate_uniqueness_score(self, new_session: Dict) -> float:
        """Calculate how unique a new session is compared to previous ones"""
        
        new_fingerprint = self.generate_session_fingerprint(new_session)
        
        if not self.session_fingerprints:
            self.session_fingerprints.append(new_fingerprint)
            return 1.0
        
        # Check similarity to existing sessions
        similar_count = self.session_fingerprints.count(new_fingerprint)
        uniqueness_score = 1.0 - (similar_count / len(self.session_fingerprints))
        
        self.session_fingerprints.append(new_fingerprint)
        
        # Keep only recent fingerprints to avoid memory bloat
        if len(self.session_fingerprints) > 1000:
            self.session_fingerprints = self.session_fingerprints[-500:]
        
        return uniqueness_score

# ============================================================================
# QUEUE SYSTEM FOR DISTRIBUTED EXECUTION
# ============================================================================

class DistributedSimulationQueue:
    """Queue system for distributing simulations across multiple instances"""
    
    def __init__(self, redis_client=None):
        self.redis_client = redis_client  # Optional Redis for distributed queue
        self.local_queue = []
        self.persona_assignments = {}
    
    def add_tasks(self, search_tasks: List[Dict]):
        """Add tasks to the queue with persona assignments"""
        
        # Distribute personas evenly
        personas = list(PersonaManager.PERSONAS.values())
        
        for i, task in enumerate(search_tasks):
            persona = personas[i % len(personas)]
            
            enriched_task = {
                **task,
                "task_id": f"task_{i}_{int(time.time())}",
                "assigned_persona": persona.persona_type.value,
                "priority": random.uniform(0.5, 1.0),
                "estimated_duration": random.randint(180, 600)
            }
            
            self.local_queue.append(enriched_task)
        
        # Sort by priority
        self.local_queue.sort(key=lambda x: x["priority"], reverse=True)
        
        logging.info(f"Added {len(search_tasks)} tasks to simulation queue")
    
    def get_next_task(self) -> Optional[Dict]:
        """Get next task from queue"""
        
        if self.local_queue:
            return self.local_queue.pop(0)
        return None
    
    def mark_task_complete(self, task_id: str, result: Dict):
        """Mark a task as complete"""
        
        # In a distributed system, this would update the central store
        logging.info(f"Task {task_id} completed with success: {result.get('success', False)}")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        asyncio.run(test_all_personas())
    elif len(sys.argv) == 2 and sys.argv[1] == "--test-resistance":
        # Test fingerprint resistance
        print("🧪 Testing fingerprint resistance...")
        config = FingerprintResistance.generate_unique_browser_config()
        print(f"Generated config: {config}")
        
        analyzer = SessionUniquenessAnalyzer()
        
        # Test with sample sessions
        for i in range(5):
            sample_session = {
                "persona": {"type": random.choice(list(PersonaManager.PERSONAS.keys())).value},
                "patterns_used": [f"pattern_{random.randint(1, 10)}" for _ in range(random.randint(3, 8))],
                "duration": random.randint(60, 300),
                "steps": [{"step": i} for i in range(random.randint(5, 15))],
                "final_cognitive_state": {"emotional_state": random.choice(["neutral", "engaged", "frustrated"])}
            }
            
            uniqueness = analyzer.calculate_uniqueness_score(sample_session)
            print(f"Session {i+1} uniqueness score: {uniqueness:.3f}")
    
    else:
        asyncio.run(main())
                    