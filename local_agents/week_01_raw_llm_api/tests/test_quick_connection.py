"""Quick connection test for Week 1."""

# Add project root to Python path for imports
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from src.core.config import OllamaConfig, BenchmarkConfig, TestPromptsConfig
from src.core.models import RequestType

def test_config():
    """Test configuration system."""
    print("🧪 Testing configuration...")
    
    try:
        # Test Ollama config
        ollama_config = OllamaConfig()
        print(f"✅ Ollama Config: {ollama_config.base_url} | {ollama_config.model}")
        print(f"   Settings: timeout={ollama_config.timeout}s, temp={ollama_config.temperature}")
        
        # Test benchmark config
        benchmark_config = BenchmarkConfig()
        print(f"✅ Benchmark Config: concurrent_limit={benchmark_config.concurrent_limit}")
        print(f"   Output: {benchmark_config.output_dir}, save={benchmark_config.save_results}")
        
        # Test prompts config
        basic_prompts = TestPromptsConfig.BASIC_PROMPTS
        quick_prompts = TestPromptsConfig.QUICK_PROMPTS
        print(f"✅ Test Prompts: {len(basic_prompts)} basic, {len(quick_prompts)} quick")
        
        # Test enum
        sync_type = RequestType.SYNC
        print(f"✅ RequestType works: {sync_type.value}")
        
        print("🎉 Configuration system working!")
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_host_connectivity():
    """Test basic host connectivity before LLM tests."""
    print("\n🔗 Testing host connectivity...")
    
    ollama_config = OllamaConfig()
    
    try:
        # Test if host.docker.internal is reachable
        response = requests.get(ollama_config.base_url, timeout=5)
        print(f"✅ Host reachable (status: {response.status_code})")
        return True
    except requests.exceptions.ConnectTimeout:
        print("❌ Host connection timeout")
        print("💡 Suggestion: Check if Ollama is running on host with 'ollama ps'")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Host connection refused")
        print("💡 Suggestion: Start Ollama on host with 'ollama serve'")
        return False
    except Exception as e:
        print(f"❌ Host connectivity error: {e}")
        return False

def test_ollama_connection():
    """Test Ollama API connection and model availability."""
    print("\n🔍 Testing Ollama API...")
    
    ollama_config = OllamaConfig()
    
    try:
        # Test models endpoint
        print(f"🔗 Connecting to: {ollama_config.base_url}/api/tags")
        response = requests.get(
            f"{ollama_config.base_url}/api/tags", 
            timeout=ollama_config.timeout
        )
        
        if response.status_code == 200:
            models_data = response.json()
            available_models = [m.get('name', '') for m in models_data.get('models', [])]
            print(f"✅ Connected! Found {len(available_models)} models")
            
            # Check if target model is available
            if ollama_config.model in available_models:
                print(f"✅ Target model '{ollama_config.model}' is available")
                return True
            else:
                print(f"❌ Target model '{ollama_config.model}' not found")
                print(f"💡 Available models: {available_models[:3]}...")  # Show first 3
                print(f"💡 Download model: ollama pull {ollama_config.model}")
                return False
                
        else:
            print(f"❌ API connection failed ({response.status_code}): {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama connection error: {e}")
        return False

def test_llm_generation():
    """Test actual LLM generation using config prompts."""
    print("\n🧪 Testing LLM generation...")
    
    ollama_config = OllamaConfig()
    
    # Use a quick prompt from config
    test_prompt = TestPromptsConfig.QUICK_PROMPTS[0]  # "Say hello in one word"
    
    try:
        print(f"🔤 Using test prompt: '{test_prompt.content}'")
        print(f"   Category: {test_prompt.category}, Expected tokens: {test_prompt.expected_tokens}")
        
        gen_response = requests.post(
            f"{ollama_config.base_url}/api/generate",
            json={
                "model": ollama_config.model,
                "prompt": test_prompt.content,
                "stream": False,
                "options": {
                    "temperature": ollama_config.temperature,
                    "num_predict": ollama_config.max_tokens
                }
            },
            timeout=ollama_config.timeout
        )
        
        if gen_response.status_code == 200:
            result = gen_response.json()
            response_text = result.get('response', 'No response').strip()
            print(f"✅ Generation successful: '{response_text}'")
            
            # Basic validation
            if len(response_text) > 0:
                actual_tokens = len(response_text.split())
                print(f"✅ Response validation passed (tokens: {actual_tokens})")
                return True
            else:
                print(f"❌ Empty response received")
                return False
        else:
            print(f"❌ Generation failed ({gen_response.status_code}): {gen_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False

def test_prompt_categories():
    """Test different prompt categories."""
    print("\n📝 Testing prompt categories...")
    
    try:
        basic_prompts = TestPromptsConfig.BASIC_PROMPTS
        quick_prompts = TestPromptsConfig.QUICK_PROMPTS
        
        # Check basic prompts
        categories = set(prompt.category for prompt in basic_prompts)
        print(f"✅ Basic prompt categories: {categories}")
        
        # Check quick prompts  
        quick_categories = set(prompt.category for prompt in quick_prompts)
        print(f"✅ Quick prompt categories: {quick_categories}")
        
        # Validate prompt structure
        for prompt in basic_prompts[:2]:  # Test first 2
            if hasattr(prompt, 'content') and hasattr(prompt, 'category'):
                print(f"✅ Prompt structure valid: {prompt.description}")
            else:
                print(f"❌ Invalid prompt structure")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt category test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests in sequence."""
    print("🚀 Week 1 Comprehensive Connection Test")
    print("=" * 50)
    
    test_results = []
    
    # Test 1: Configuration
    test_results.append(("Configuration", test_config()))
    
    # Test 2: Prompt categories
    test_results.append(("Prompt Categories", test_prompt_categories()))
    
    # Test 3: Host connectivity
    test_results.append(("Host Connectivity", test_host_connectivity()))
    
    # Test 4: Ollama connection
    test_results.append(("Ollama API", test_ollama_connection()))
    
    # Test 5: LLM generation (only if previous tests pass)
    if all(result[1] for result in test_results):
        test_results.append(("LLM Generation", test_llm_generation()))
    else:
        print("\n⏭️ Skipping LLM generation test due to previous failures")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} | {status}")
    
    all_passed = all(result[1] for result in test_results)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("🎯 Ready to implement full Week 1 benchmark system")
        print(f"🔧 Config ready: {OllamaConfig().model} @ {OllamaConfig().base_url}")
    else:
        print("\n🛠️ ISSUES DETECTED - Troubleshooting needed")
        print("📋 Common fixes:")
        print("   1. Start Ollama: ollama serve")
        print("   2. Download model: ollama pull qwen3:latest")
        print("   3. Check host connectivity from dev container")
    
    return all_passed

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)

