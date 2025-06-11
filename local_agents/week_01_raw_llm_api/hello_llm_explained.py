"""Understanding LLM Connection vs Loading - Step by Step"""

import requests
import time
from rich.console import Console

console = Console()
OLLAMA_BASE_URL = "http://host.docker.internal:11434"

def step1_basic_connection():
    """Step 1: Test if Ollama service is running and reachable."""
    console.print("🔍 Step 1: Testing Basic Connection", style="bold blue")
    
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        
        if response.status_code == 200:
            console.print("  ✅ Ollama service is RUNNING and REACHABLE", style="green")
            console.print("  📡 Network path: Dev Container → host.docker.internal:11434 → Windows Host", style="dim")
            return True
        else:
            console.print(f"  ❌ Service responded but with error: {response.status_code}", style="red")
            return False
            
    except Exception as e:
        console.print(f"  ❌ Cannot reach Ollama service: {e}", style="red")
        console.print("  💡 Check: Is Ollama running on Windows host?", style="yellow")
        return False

def step2_model_availability():
    """Step 2: Check what models are AVAILABLE (downloaded but not in memory)."""
    console.print("\n📦 Step 2: Checking Model Availability", style="bold blue")
    
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        models = response.json().get("models", [])
        
        console.print(f"  Found {len(models)} models on disk:", style="cyan")
        
        for model in models:
            name = model.get("name", "unknown")
            size_bytes = model.get("size", 0)
            size_gb = size_bytes / (1024**3)
            modified = model.get("modified_at", "")[:19]  # Date only
            
            console.print(f"    📁 {name}")
            console.print(f"       Size: {size_gb:.1f}GB on disk")
            console.print(f"       Modified: {modified}")
            console.print(f"       Status: AVAILABLE (but not necessarily loaded)")
        
        console.print("\n  💡 Key Point: These models exist on disk but may not be in RAM!", style="yellow")
        return models
        
    except Exception as e:
        console.print(f"  ❌ Error checking models: {e}", style="red")
        return []

def step3_model_loading_status():
    """Step 3: Check what models are LOADED (currently in RAM/VRAM)."""
    console.print("\n🧠 Step 3: Checking Model Loading Status", style="bold blue")
    
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/ps", timeout=5)
        loaded_models = response.json().get("models", [])
        
        if loaded_models:
            console.print(f"  Found {len(loaded_models)} models LOADED in memory:", style="green")
            
            for model in loaded_models:
                name = model.get("name", "unknown")
                size_vram = model.get("size_vram", 0) / (1024**2)  # MB
                until = model.get("expires_at", "unknown")
                
                console.print(f"    🟢 {name}")
                console.print(f"       Memory usage: {size_vram:.0f}MB")
                console.print(f"       Will unload at: {until[:19] if until != 'unknown' else 'unknown'}")
        else:
            console.print("  🔴 NO models currently loaded in memory", style="red")
            console.print("  💡 First request will trigger model loading (slow!)", style="yellow")
        
        return loaded_models
        
    except Exception as e:
        console.print(f"  ❌ Error checking loaded models: {e}", style="red")
        return []

def step4_understand_cold_warm():
    """Step 4: Demonstrate cold start vs warm performance."""
    console.print("\n🌡️  Step 4: Cold Start vs Warm Performance", style="bold blue")
    
    MODEL = "qwen3:latest"
    
    # Check if model is already loaded
    loaded_models = step3_model_loading_status()
    is_loaded = any(model.get("name") == MODEL for model in loaded_models)
    
    if is_loaded:
        console.print(f"  🟢 {MODEL} is already WARM (loaded in memory)", style="green")
        console.print("  ⚡ Next request should be fast (~1-3 seconds)", style="dim")
    else:
        console.print(f"  🔴 {MODEL} is COLD (not in memory)", style="red")
        console.print("  🐌 Next request will be slow (~15-30 seconds for loading)", style="dim")
    
    console.print("\n  📚 Understanding Cold vs Warm:", style="cyan")
    console.print("     Cold Start: Model not in memory → Load from disk → Generate response")
    console.print("     Warm Request: Model in memory → Generate response immediately")
    console.print("     Loading Time: 15-30 seconds (depends on model size & hardware)")
    console.print("     Generation Time: 1-5 seconds per request")

def step5_demonstrate_loading():
    """Step 5: Actually demonstrate the loading process."""
    console.print("\n🔄 Step 5: Live Loading Demonstration", style="bold blue")
    
    MODEL = "qwen3:latest"
    
    console.print("  Making a request to trigger loading...", style="yellow")
    console.print("  ⏱️  Watch the timing difference!", style="dim")
    
    # First request (potentially cold)
    start_time = time.perf_counter()
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": "Hi",
                "stream": False,
                "options": {"num_predict": 5}  # Just 5 tokens
            },
            timeout=60
        )
        
        first_request_time = time.perf_counter() - start_time
        
        if response.status_code == 200:
            console.print(f"  ✅ First request completed in {first_request_time:.1f}s", style="green")
            
            if first_request_time > 10:
                console.print("    🐌 This was a COLD start (model loading took most of the time)", style="red")
            else:
                console.print("    ⚡ This was a WARM request (model was already loaded)", style="green")
        
        # Second request (should be warm)
        console.print("\n  Making second request (should be warm)...", style="yellow")
        start_time = time.perf_counter()
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": "Hello again",
                "stream": False,
                "options": {"num_predict": 5}
            },
            timeout=30
        )
        
        second_request_time = time.perf_counter() - start_time
        
        if response.status_code == 200:
            console.print(f"  ✅ Second request completed in {second_request_time:.1f}s", style="green")
            
            if first_request_time > second_request_time * 2:
                speedup = first_request_time / second_request_time
                console.print(f"    🚀 Warm speedup: {speedup:.1f}x faster!", style="green")
            else:
                console.print("    ⚡ Both requests were warm", style="green")
    
    except Exception as e:
        console.print(f"  ❌ Request failed: {e}", style="red")

def option1_preload_strategy():
    """Option 1: Pre-load model before benchmarking for fair comparison."""
    console.print("\n🔥 Option 1: Pre-loading Strategy", style="bold magenta")
    
    MODEL = "qwen3:latest"
    
    console.print("  💡 Strategy: Load model once, then benchmark warm performance", style="cyan")
    console.print("  📈 Benefit: All benchmark requests will be fast and comparable", style="green")
    console.print("  ⚠️  Trade-off: Hides real-world cold start costs", style="yellow")
    
    def preload_model():
        """Actually pre-load the model."""
        console.print("\n  🔄 Pre-loading model...", style="yellow")
        
        start_time = time.perf_counter()
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": "Loading",  # Simple prompt
                    "stream": False,
                    "options": {"num_predict": 1}  # Minimal generation
                },
                timeout=60
            )
            
            load_time = time.perf_counter() - start_time
            
            if response.status_code == 200:
                console.print(f"    ✅ Model pre-loaded in {load_time:.1f}s", style="green")
                console.print("    🎯 Now all benchmark requests will be warm!", style="dim")
                return True
            else:
                console.print(f"    ❌ Pre-load failed: {response.status_code}", style="red")
                return False
                
        except Exception as e:
            console.print(f"    ❌ Pre-load error: {e}", style="red")
            return False
    
    # Demonstrate the strategy
    if preload_model():
        console.print("\n  📊 Your benchmark would now show:", style="cyan")
        console.print("     Sync requests: ~2-5 seconds each")
        console.print("     Async requests: ~2-5 seconds each")
        console.print("     Concurrent: ~2-5 seconds total (true speedup!)")

def option2_cold_warm_analysis():
    """Option 2: Measure and analyze both cold and warm performance."""
    console.print("\n📊 Option 2: Cold vs Warm Analysis", style="bold magenta")
    
    console.print("  💡 Strategy: Measure everything, analyze separately", style="cyan")
    console.print("  📈 Benefit: Shows real-world performance characteristics", style="green")
    console.print("  🎯 Use case: Understanding production behavior", style="blue")
    
    console.print("\n  📋 Analysis approach:", style="cyan")
    console.print("     1. First request = Cold start time (loading + generation)")
    console.print("     2. Subsequent requests = Warm generation time")
    console.print("     3. Calculate: Cold overhead = First - Average(Subsequent)")
    console.print("     4. Report both metrics separately")
    
    console.print("\n  📊 Example analysis output:", style="dim")
    console.print("     Cold Start Performance:")
    console.print("       - First sync request: 25.3s (20s loading + 5.3s generation)")
    console.print("       - Model loading overhead: 20s")
    console.print("     ")
    console.print("     Warm Performance:")
    console.print("       - Avg sync request: 3.2s")
    console.print("       - Avg async request: 3.1s") 
    console.print("       - Concurrent speedup: 2.8x")

def step3_then_step5_scenario():
    """What happens when you check loading status, then demonstrate loading."""
    console.print("\n🔍 Scenario: Step 3 → Step 5", style="bold cyan")
    
    # Step 3: Check current loading status
    loaded_models = step3_model_loading_status()
    MODEL = "qwen3:latest"
    is_loaded = any(model.get("name") == MODEL for model in loaded_models)
    
    if is_loaded:
        console.print("  📊 Current state: Model is LOADED", style="green")
        console.print("  🔮 Step 5 prediction: Both requests will be WARM (fast)", style="dim")
    else:
        console.print("  📊 Current state: Model is NOT loaded", style="red")
        console.print("  🔮 Step 5 prediction: First request COLD (slow), second WARM (fast)", style="dim")
    
    # Now Step 5 will demonstrate based on current state
    console.print("\n  ⚡ Running Step 5 based on current state...")
    step5_demonstrate_loading()

def step5_then_step3_scenario():
    """What happens when you demonstrate loading, then check status."""
    console.print("\n🔍 Scenario: Step 5 → Step 3", style="bold cyan")
    
    console.print("  📊 Current state: Unknown (haven't checked yet)", style="yellow")
    console.print("  🔮 Step 5 will show: Cold vs Warm difference (if model not loaded)", style="dim")
    
    # Step 5: Demonstrate loading (this WILL load the model)
    step5_demonstrate_loading()
    
    console.print("\n  ⚡ Now checking status after Step 5...")
    # Step 3: Check status (model should now be loaded)
    loaded_models = step3_model_loading_status()
    console.print("  📊 Expected result: Model should now be LOADED", style="green")

def understand_state_changes():
    """Understand how each step affects system state."""
    console.print("\n🧠 Understanding State Changes", style="bold magenta")
    
    console.print("  📖 Read-only steps (don't change state):", style="green")
    console.print("     Step 1: test_connection() - just checks if service is running")
    console.print("     Step 2: model_availability() - just lists what's on disk") 
    console.print("     Step 3: model_loading_status() - just checks what's in memory")
    console.print("     Step 4: understand_cold_warm() - just explains concepts")
    
    console.print("\n  ✏️  Write/Action steps (change state):", style="red")
    console.print("     Step 5: demonstrate_loading() - MAKES REQUESTS → loads model")
    
    console.print("\n  🔄 State Transition:", style="cyan")
    console.print("     Before Step 5: Model may or may not be loaded")
    console.print("     During Step 5: If model not loaded → gets loaded")
    console.print("     After Step 5: Model is definitely loaded")
    
    console.print("\n  🎯 Strategy Options:", style="yellow")
    console.print("     Option A: Steps 1,2,3,4,5 - See current state, then demonstrate")
    console.print("     Option B: Steps 1,2,4,5,3 - Demonstrate, then verify final state") 
    console.print("     Option C: Just Step 5 - Focus on demonstrating performance difference")

def main():
    """Complete LLM logistics walkthrough with options."""
    console.print("🎓 LLM Performance Logistics - Complete Guide", style="bold white")
    
    # Basic connection always first
    if not step1_basic_connection():
        return
    
    # Always check what's available
    step2_model_availability()
    
    # Give user choice about order
    console.print("\n🤔 Choose your learning path:", style="bold yellow")
    console.print("  A) Check current state first, then demonstrate (comprehensive)")
    console.print("  B) Jump to demonstration (action-focused)")
    console.print("  C) Full diagnostic (check → demo → check again)")
    
    choice = input("\nEnter A, B, or C (or press Enter for A): ").upper() or 'A'
    
    if choice == 'A':
        console.print("\n📋 Path A: Check State → Demonstrate", style="bold blue")
        step3_model_loading_status()
        step4_understand_cold_warm()
        step5_demonstrate_loading()
        
    elif choice == 'B':
        console.print("\n📋 Path B: Jump to Demonstration", style="bold blue")
        step4_understand_cold_warm()
        step5_demonstrate_loading()
        
    elif choice == 'C':
        console.print("\n📋 Path C: Full Diagnostic", style="bold blue")
        console.print("Before demonstration:")
        step3_model_loading_status()
        step4_understand_cold_warm()
        step5_demonstrate_loading()
        console.print("\nAfter demonstration:")
        step3_model_loading_status()
    
    console.print("\n" + "="*60, style="dim")
    console.print("🎯 You can run any combination - each step teaches something different!", style="bold green")

if __name__ == "__main__":
    main()

