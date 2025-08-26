# setup_models.py
#!/usr/bin/env python3
"""
Setup script for AI-enhanced search simulator models
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_directories():
    """Setup required directory structure"""
    
    script_dir = Path(__file__).parent
    modals_dir = script_dir / "modals"
    
    # Create main directories
    directories = [
        modals_dir,
        modals_dir / "AutoWebGLM",
        modals_dir / "AutoWebGLM" / "miniwob++",
        modals_dir / "AutoWebGLM" / "miniwob++" / "html_tools",
        modals_dir / "AutoWebGLM" / "webarena",
        modals_dir / "AutoWebGLM" / "webarena" / "llms",
        modals_dir / "AutoWebGLM" / "webarena" / "llms" / "providers",
        modals_dir / "USimAgent",
        modals_dir / "USimAgent" / "agent",
        modals_dir / "USimAgent" / "config",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py files
        init_file = directory / "__init__.py"
        if not init_file.exists():
            init_file.touch()
    
    print("✅ Directory structure created")
    return modals_dir

def create_fallback_implementations(modals_dir):
    """Create fallback implementations for missing model components"""
    
    # AutoWebGLM HTML Parser fallback
    html_parser_content = '''
class HTMLParser:
    """Fallback HTML parser"""
    
    def __init__(self):
        self.parsed_data = {}
    
    def parse(self, html_content):
        """Parse HTML content"""
        return {
            "content": html_content,
            "length": len(html_content),
            "elements": self._extract_basic_elements(html_content)
        }
    
    def _extract_basic_elements(self, html_content):
        """Extract basic elements"""
        import re
        
        elements = []
        
        # Find links
        links = re.findall(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html_content, re.IGNORECASE | re.DOTALL)
        for href, text in links:
            elements.append({"tag": "a", "href": href, "text": text.strip()})
        
        # Find buttons
        buttons = re.findall(r'<button[^>]*>(.*?)</button>', html_content, re.IGNORECASE | re.DOTALL)
        for text in buttons:
            elements.append({"tag": "button", "text": text.strip()})
        
        # Find forms
        forms = re.findall(r'<form[^>]*>', html_content, re.IGNORECASE)
        for form in forms:
            elements.append({"tag": "form", "attributes": form})
        
        return elements
'''
    
    # Element Identifier fallback
    identifier_content = '''
class ElementIdentifier:
    """Fallback element identifier"""
    
    def __init__(self):
        self.clickable_tags = ["a", "button", "input", "select"]
    
    def identify_clickable(self, elements):
        """Identify clickable elements"""
        clickable = []
        
        for element in elements:
            if element.get("tag") in self.clickable_tags:
                clickable.append(element)
            elif "onclick" in element.get("attributes", ""):
                clickable.append(element)
        
        return clickable
'''
    
    # HTML Utils fallback
    utils_content = '''
def extract_elements(parsed_html):
    """Extract elements from parsed HTML"""
    return parsed_html.get("elements", [])

def classify_page_type(url, content):
    """Classify page type"""
    url_lower = url.lower()
    
    if "search" in url_lower:
        return "search_results"
    elif "shop" in url_lower:
        return "ecommerce"
    elif "blog" in url_lower:
        return "content_page"
    else:
        return "general_page"
'''
    
    # USimAgent fallbacks
    agent_content = '''
class Agent:
    """Fallback USimAgent"""
    
    def __init__(self, config):
        self.config = config
        self.state = None
    
    def get_next_action(self, state, task):
        """Get next action"""
        import random
        
        actions = ["scroll_down", "hover_element", "wait", "read_content"]
        selected_action = random.choice(actions)
        
        return ActionResult(
            action_type=selected_action,
            confidence=random.uniform(0.5, 0.9),
            reasoning=f"Selected {selected_action} based on fallback logic"
        )

class ActionResult:
    """Action result container"""
    
    def __init__(self, action_type, confidence, reasoning):
        self.action_type = action_type
        self.confidence = confidence
        self.reasoning = reasoning
'''
    
    state_content = '''
class State:
    """Fallback state management"""
    
    def __init__(self):
        self.context = {}
        self.history = []
    
    def update_context(self, context):
        """Update state context"""
        self.context.update(context)
        self.history.append(context)
'''
    
    task_content = '''
class Task:
    """Fallback task representation"""
    
    def __init__(self, description):
        self.description = description
        self.status = "active"
        self.progress = 0.0
'''
    
    config_content = '''
class Config:
    """Fallback configuration"""
    
    def __init__(self):
        self.model_params = {
            "temperature": 0.7,
            "max_tokens": 512,
            "timeout": 30
        }
        
        self.behavior_params = {
            "action_variety": 0.8,
            "decision_speed": 1.0,
            "attention_span": 1.0
        }
'''
    
    gpt_provider_content = '''
class GPTProvider:
    """Fallback GPT provider"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.model = "gpt-3.5-turbo"
    
    def generate_response(self, prompt, **kwargs):
        """Generate response (fallback)"""
        import random
        
        responses = [
            "scroll down to explore more content",
            "hover over interesting elements",
            "wait and observe the page",
            "read the content carefully"
        ]
        
        return {
            "response": random.choice(responses),
            "confidence": random.uniform(0.6, 0.9),
            "tokens_used": random.randint(50, 200)
        }
'''
    
    # Write fallback files
    files_to_create = {
        modals_dir / "AutoWebGLM" / "miniwob++" / "html_tools" / "html_parser.py": html_parser_content,
        modals_dir / "AutoWebGLM" / "miniwob++" / "html_tools" / "identifier.py": identifier_content,
        modals_dir / "AutoWebGLM" / "miniwob++" / "html_tools" / "utils.py": utils_content,
        modals_dir / "AutoWebGLM" / "webarena" / "llms" / "providers" / "gpt.py": gpt_provider_content,
        modals_dir / "USimAgent" / "agent" / "agent.py": agent_content,
        modals_dir / "USimAgent" / "agent" / "state.py": state_content,
        modals_dir / "USimAgent" / "agent" / "task.py": task_content,
        modals_dir / "USimAgent" / "config" / "config.py": config_content,
    }
    
    for file_path, content in files_to_create.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✅ Fallback implementations created")

def install_dependencies():
    """Install required dependencies"""
    
    print("📦 Installing dependencies...")
    
    try:
        # Install Python packages
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python packages installed")
        
        # Install Playwright browsers
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("✅ Playwright browsers installed")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Dependency installation failed: {e}")
        return False
    
    return True

def clone_real_repositories(modals_dir):
    """Attempt to clone real repositories if available"""
    
    repositories = [
        {
            "name": "AutoWebGLM",
            "url": "https://github.com/THUDM/AutoWebGLM.git",
            "path": modals_dir / "AutoWebGLM"
        },
        # Note: USimAgent repository URL would need to be provided
        # {
        #     "name": "USimAgent", 
        #     "url": "https://github.com/example/USimAgent.git",
        #     "path": modals_dir / "USimAgent"
        # }
    ]
    
    cloned_any = False
    
    for repo in repositories:
        try:
            print(f"🔄 Attempting to clone {repo['name']}...")
            
            # Remove existing directory if empty
            if repo['path'].exists() and not any(repo['path'].iterdir()):
                shutil.rmtree(repo['path'])
            
            if not repo['path'].exists():
                subprocess.run([
                    "git", "clone", repo['url'], str(repo['path'])
                ], check=True, capture_output=True)
                
                print(f"✅ {repo['name']} cloned successfully")
                cloned_any = True
            else:
                print(f"ℹ️ {repo['name']} directory already exists")
                
        except subprocess.CalledProcessError:
            print(f"⚠️ Could not clone {repo['name']} (using fallback)")
        except FileNotFoundError:
            print(f"⚠️ Git not available for cloning {repo['name']} (using fallback)")
    
    return cloned_any

def main():
    """Main setup function"""
    
    print("🚀 AI-Enhanced Search Simulator Setup")
    print("=" * 40)
    
    # Setup directories
    modals_dir = setup_directories()
    
    # Try to clone real repositories
    print("\n📂 Setting up model repositories...")
    cloned_repos = clone_real_repositories(modals_dir)
    
    # Create fallback implementations
    print("\n🔄 Creating fallback implementations...")
    create_fallback_implementations(modals_dir)
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    deps_installed = install_dependencies()
    
    print("\n🎉 Setup Complete!")
    print("=" * 20)
    
    if cloned_repos:
        print("✅ Real model repositories cloned")
    else:
        print("🔄 Using fallback implementations")
    
    if deps_installed:
        print("✅ Dependencies installed successfully")
    else:
        print("⚠️ Some dependencies may need manual installation")
    
    print("\n🚀 Next Steps:")
    print("1. Test integration: python fixed_integrated_agent.py --check-integration")
    print("2. Create sample data: python fixed_integrated_agent.py --create-sample")
    print("3. Run simulation: python fixed_integrated_agent.py sample_search_data.json")
    
    print("\n📖 For more help: python fixed_integrated_agent.py --help-setup")

if __name__ == "__main__":
    main()
