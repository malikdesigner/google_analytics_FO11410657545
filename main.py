# main.py
"""
ENHANCED HUMAN-LIKE GOOGLE SEARCH SIMULATOR - MAIN ENTRY POINT
Updated for JSON input and browser choice argument
"""

import sys
import asyncio
import argparse
import logging
import json
import os
import time
from pathlib import Path
from datetime import datetime

# Import our modules
from model_integration import ModelIntegration, EnhancedPersonaManager, UserPersonaType
from google_activity import GoogleSearchSimulator
from site_activity import SiteActivityManager
from utils import setup_enhanced_logging, create_enhanced_sample_data
from browserless_connection import BrowserlessConnection

class EnhancedSearchProcessor:
    """Main processor that orchestrates all components"""
    
    def __init__(self, json_file_path: str, browser_type: str = "browserless"):
        self.json_file_path = json_file_path
        self.browser_type = browser_type.lower()
        self.results = []
        
        # Create configuration based on browser type
        if self.browser_type == "chromium":
            self.config = {"use_browserless": False}
            logging.info("🖥️ Browser Backend: Chromium")
        else:
            self.config = {"use_browserless": True}
            logging.info("🌐 Browser Backend: Browserless with ProxyJet")
        
        # Initialize components
        self.model_integration = ModelIntegration(self.config)
        self.google_simulator = GoogleSearchSimulator(self.config)
        self.site_manager = SiteActivityManager(self.config)
        
        # Enhanced persona rotation
        self.persona_rotation = list(EnhancedPersonaManager.PERSONAS.values())
        self.current_persona_index = 0
        
        # Browserless connection manager
        self.browserless_connection = None
        if self.browser_type == "browserless":
            self.browserless_connection = BrowserlessConnection(use_proxy=True)
    
    def get_next_persona(self):
        """Get next persona in rotation"""
        persona = self.persona_rotation[self.current_persona_index]
        self.current_persona_index = (self.current_persona_index + 1) % len(self.persona_rotation)
        return persona
    
    async def process_all_searches(self, delay_between_searches: int = 180, 
                                 randomize_order: bool = True) -> dict:
        """Process all searches with enhanced human-like behavior"""
        
        search_data = self.load_search_data()
        
        if randomize_order:
            import random
            random.shuffle(search_data)
            logging.info("🔀 Randomized search order for more realistic patterns")
        
        logging.info(f"🚀 Starting {len(search_data)} enhanced search simulations using {self.browser_type.title()}")
        logging.info(f"🧠 Models available: {self.model_integration.models_available}")
        
        # Create Browserless session if needed
        if self.browser_type == "browserless":
            if not self.browserless_connection.create_session():
                logging.error("❌ Failed to create Browserless session, falling back to Chromium")
                self.browser_type = "chromium"
                self.config = {"use_browserless": False}
                self.google_simulator = GoogleSearchSimulator(self.config)
                self.site_manager = SiteActivityManager(self.config)
        
        all_results = []
        
        for i, search_task in enumerate(search_data):
            keyword = search_task["keyword"]
            site = search_task["site"]
            
            # Select persona
            persona = self.get_next_persona()
            
            logging.info(f"\n{'='*60}")
            logging.info(f"🔍 Search {i+1}/{len(search_data)}: '{keyword}' -> {site}")
            logging.info(f"🎭 Persona: {persona.name} ({persona.persona_type.value})")
            logging.info(f"🌐 Backend: {self.browser_type.title()}")
            
            try:
                # Run enhanced search simulation
                result = await self._simulate_single_search(keyword, site, persona)
                result["global_session_id"] = i + 1
                result["enhanced_integration"] = True
                result["browser_backend"] = self.browser_type
                
                all_results.append(result)
                
                # Enhanced result logging
                if result.get("success"):
                    duration = result.get("duration", 0)
                    activities = len(result.get("human_like_activities", []))
                    logging.info(f"✅ SUCCESS: {duration:.1f}s, {activities} human-like activities")
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
                    "enhanced_integration": True,
                    "browser_backend": self.browser_type
                })
            
            # Enhanced delay with random variation
            if i < len(search_data) - 1:
                import random
                delay = delay_between_searches + random.randint(-60, 60)
                logging.info(f"⏱️ Waiting {delay}s before next search...")
                await asyncio.sleep(delay)
        
        # Clean up Browserless session
        if self.browserless_connection:
            self.browserless_connection.close_session()
        
        # Generate enhanced summary
        summary = self._generate_enhanced_summary(all_results)
        self.results = summary
        return summary
    
    async def _simulate_single_search(self, keyword: str, target_site: str, persona) -> dict:
        """Simulate a single search session"""
        
        session_start = time.time()
        
        session_data = {
            "keyword": keyword,
            "target_site": target_site,
            "browser_backend": self.browser_type,
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
            "models_integrated": self.model_integration.models_available,
            "cognitive_journey": []
        }
        
        # Initialize model components for this session
        autowebglm = self.model_integration.create_autowebglm(persona)
        usimagent = self.model_integration.create_usimagent(persona)
        
        # Create browser based on type
        if self.browser_type == "browserless" and self.browserless_connection:
            page, browser, playwright = await self.browserless_connection.connect_browser()
            if not page:
                logging.error("❌ Browserless connection failed, falling back to Chromium")
                self.browser_type = "chromium"
                self.config = {"use_browserless": False}
                page, browser, playwright = await self.google_simulator.create_enhanced_browser(persona)
        else:
            page, browser, playwright = await self.google_simulator.create_enhanced_browser(persona)
        
        try:
            # Step 1: Navigate to Google and perform search
            await self.google_simulator.navigate_to_google(page, session_data)
            await self.google_simulator.perform_enhanced_search(page, keyword, session_data)
            
            # Step 2: Interact with SERP with human-like behavior
            target_found = await self.google_simulator.interact_with_serp_human_like(
                page, target_site, session_data, autowebglm, usimagent
            )
            
            # Step 3: Visit target site with enhanced browsing
            if target_found:
                success = await self.site_manager.visit_target_site_enhanced(
                    page, target_site, session_data, autowebglm, usimagent, persona
                )
            else:
                success = False
            
            session_data["success"] = success
            session_data["duration"] = time.time() - session_start
            
            # Add final cognitive state if available
            if hasattr(usimagent, 'get_final_state'):
                session_data["final_cognitive_state"] = usimagent.get_final_state()
            
            logging.info(f"Enhanced search session completed: {'✅ SUCCESS' if success else '❌ FAILED'}")
            
        except Exception as e:
            logging.error(f"Enhanced search session failed: {e}")
            session_data["error"] = str(e)
            session_data["duration"] = time.time() - session_start
            
        finally:
            try:
                if self.browser_type != "browserless":  # Don't close Browserless browser, just the page
                    await browser.close()
                    await playwright.stop()
            except Exception as cleanup_error:
                logging.debug(f"Cleanup error: {cleanup_error}")
        
        return session_data
    
    def load_search_data(self) -> list:
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
                            from urllib.parse import urlparse
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
    
    def _generate_enhanced_summary(self, all_results: list) -> dict:
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
        
        # Browser backend statistics
        backend_distribution = {}
        for result in all_results:
            backend = result.get("browser_backend", "unknown")
            backend_distribution[backend] = backend_distribution.get(backend, 0) + 1
        
        summary = {
            "total_searches": len(all_results),
            "successful_searches": successful,
            "success_rate": (successful / len(all_results)) * 100 if all_results else 0,
            "model_integration_rate": (model_integrated / len(all_results)) * 100 if all_results else 0,
            "models_available": self.model_integration.models_available,
            "total_human_activities": total_activities,
            "avg_activities_per_session": avg_activities,
            "avg_cognitive_actions_per_session": avg_cognitive_actions,
            "persona_distribution": persona_distribution,
            "backend_distribution": backend_distribution,
            "results": all_results,
            "processing_time": datetime.now().isoformat(),
            "integration_version": "Enhanced Human-like v2.0 Modular + Browserless"
        }
        
        return summary
    
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
                
                f.write("\nBROWSER BACKEND DISTRIBUTION:\n")
                for backend, count in self.results['backend_distribution'].items():
                    f.write(f"  {backend.title()}: {count}\n")
                
            logging.info(f"Summary report saved to {summary_file}")
            
        except Exception as e:
            logging.error(f"Failed to save summary report: {e}")


async def main():
    """Enhanced main function with JSON input and browser choice"""
    
    setup_enhanced_logging()
    
    parser = argparse.ArgumentParser(
        description="Enhanced Human-like Google Search Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  python main.py searches.json                    # Use Browserless (default)
  python main.py searches.json browserless        # Use Browserless explicitly  
  python main.py searches.json chromium           # Use Chromium
  python main.py --single "keyword" "site"        # Single search with Browserless
  python main.py --single "keyword" "site" chromium # Single search with Chromium

JSON Format:
  [
    {"keyword": "search term", "site": "https://example.com"},
    {"keyword": "another term", "site": "https://target.com"}
  ]
        """
    )
    
    parser.add_argument("json_file", nargs='?', help="JSON file containing keyword-site pairs")
    parser.add_argument("browser_type", nargs='?', default="browserless", 
                       choices=["browserless", "chromium"],
                       help="Browser type: browserless (default) or chromium")
    
    parser.add_argument("--delay", type=int, default=180, help="Base delay between searches (seconds)")
    parser.add_argument("--output", type=str, help="Output file to save results")
    parser.add_argument("--randomize", action="store_true", help="Randomize search order")
    parser.add_argument("--single", nargs=2, metavar=("KEYWORD", "SITE"), help="Run single search")
    parser.add_argument("--persona", choices=[p.value for p in UserPersonaType], help="Specific persona")
    parser.add_argument("--validate", action="store_true", help="Validate Browserless connection")
    parser.add_argument("--create-sample", action="store_true", help="Create sample JSON file")
    
    args = parser.parse_args()
    
    print("🚀 ENHANCED HUMAN-LIKE GOOGLE SEARCH SIMULATOR")
    print("=" * 55)
    print("🎭 Realistic User Behavior Modeling")
    print("🖱️ Human-like Hovering & Link Interaction")
    print("🧠 Cognitive State & Fatigue Simulation")
    print("🔧 Advanced Model Integration")
    print("📦 Modular Architecture")
    print("🌐 Browserless & Chromium Support")
    print("=" * 55)
    
    try:
        if args.validate:
            from browserless_connection import validate_configuration
            validate_configuration()
            return
        
        elif args.create_sample:
            sample_data = [
                {"keyword": "mesiodens invislondon", "site": "https://invislondon.co.uk"},
                {"keyword": "Invisalign london invis", "site": "https://invislondon.co.uk"},
                {"keyword": "sulfur burps invislondon", "site": "https://invislondon.co.uk"},
                {"keyword": "torus mandibularis invislondon", "site": "https://invislondon.co.uk"}
            ]
            
            with open('sample_searches.json', 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
            
            print("✅ Created sample_searches.json")
            print("🚀 Run with: python main.py sample_searches.json")
            return
        
        elif args.single:
            # Single search mode
            keyword, site = args.single
            browser_type = args.browser_type if hasattr(args, 'browser_type') else 'browserless'
            
            print(f"🎯 Single search simulation")
            print(f"🔍 Keyword: {keyword}")
            print(f"🌐 Site: {site}")
            print(f"🖥️ Browser: {browser_type.title()}")
            
            # Select persona
            if args.persona:
                persona_type = UserPersonaType(args.persona)
                persona = EnhancedPersonaManager.get_persona_by_type(persona_type)
                print(f"🎭 Using specified persona: {persona.name}")
            else:
                persona = EnhancedPersonaManager.get_random_persona()
                print(f"🎭 Using random persona: {persona.name}")
            
            # Create processor for single search
            processor = EnhancedSearchProcessor("", browser_type)
            result = await processor._simulate_single_search(keyword, site, persona)
            
            print(f"\n🎉 RESULT: {'✅ SUCCESS' if result.get('success') else '❌ FAILED'}")
            
            if result.get('success'):
                duration = result.get('duration', 0)
                activities = len(result.get('human_like_activities', []))
                
                print(f"⏱️ Duration: {duration:.1f}s")
                print(f"🎭 Human-like activities: {activities}")
                print(f"🌐 Browser: {browser_type.title()}")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, default=str, ensure_ascii=False)
                print(f"💾 Result saved to {args.output}")
        
        else:
            # Batch processing
            if not args.json_file:
                print("❌ JSON file required for batch processing")
                print("💡 Use --create-sample to create sample data")
                print("💡 Usage: python main.py searches.json [browserless|chromium]")
                return
            
            # Verify input file exists
            if not os.path.exists(args.json_file):
                print(f"❌ Input file not found: {args.json_file}")
                print("💡 Use --create-sample to create sample data")
                return
            
            browser_type = args.browser_type
            print(f"📂 Input file: {args.json_file}")
            print(f"🌐 Browser type: {browser_type.title()}")
            print(f"⏱️ Base delay: {args.delay}s")
            print(f"🔀 Randomize order: {args.randomize}")
            
            # Create enhanced processor
            processor = EnhancedSearchProcessor(args.json_file, browser_type)
            
            # Process all searches with enhanced behavior
            results = await processor.process_all_searches(
                delay_between_searches=args.delay,
                randomize_order=args.randomize
            )
            
            # Print enhanced summary
            print(f"\n🎉 PROCESSING COMPLETE")
            print(f"📊 Results: {results['successful_searches']}/{results['total_searches']} "
                  f"({results['success_rate']:.1f}% success)")
            print(f"🧠 Model Integration: {results['model_integration_rate']:.1f}%")
            print(f"🎭 Total Human Activities: {results['total_human_activities']}")
            
            # Print backend distribution
            backend_dist = results.get('backend_distribution', {})
            for backend, count in backend_dist.items():
                print(f"🌐 {backend.title()}: {count} sessions")
            
            # Save enhanced results
            if args.output:
                processor.save_results(args.output)
            else:
                # Generate default output filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                browser_suffix = browser_type
                default_output = f"results_{browser_suffix}_{timestamp}.json"
                processor.save_results(default_output)
                print(f"💾 Results saved to {default_output}")
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logging.error(f"Main execution error: {e}")
        
        # Provide helpful suggestions
        if "browserless" in str(e).lower():
            print("💡 Try using Chromium: python main.py searches.json chromium")
        elif "playwright" in str(e).lower():
            print("💡 Install Playwright: pip install playwright")
            print("💡 Install browsers: playwright install")
        elif "json" in str(e).lower():
            print("💡 Check JSON file format")
            print("💡 Use --create-sample to create valid sample")

if __name__ == "__main__":
    asyncio.run(main())