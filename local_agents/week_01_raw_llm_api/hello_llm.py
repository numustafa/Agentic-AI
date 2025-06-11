"""
Week 1: Raw LLM API Benchmark Script. The script compares 3 different approaches to interacting with a local LLM API:

1. Synchronous requests using `requests` - Traditional blocking HTTP requests
2. Asynchronous requests using `httpx` - Non-blocking HTTPx requests
3. Concurrent requests using `asyncio` and `httpx` - Multiple concurrent HTTPx requests

This script benchmarks the performance of these methods against a local Ollama LLM API.
It also tests the connection to the Ollama API and prints a summary of the results.

idea: Intelligent Model State Management
"""

import asyncio
import time
import requests
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
OLLAMA_BASE_URL = "http://host.docker.internal:11434"
MODEL = "qwen3:latest"
TEST_PROMPTS = [
    "Say hello",
    "What is 2+2?", 
    "Explain Python in one sentence"
]

# STRATEGY 1: Intelligent Model State Management
class ModelStateManager:
    """Manages model loading state and provides optimization insights."""
    
    def __init__(self):
        self.is_warm = False
        self.warmup_time = None
    
    def check_model_state(self):
        """Check if model is currently loaded in memory."""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/ps", timeout=5)
            if response.status_code == 200:
                loaded_models = response.json().get("models", [])
                self.is_warm = any(model.get("name") == MODEL for model in loaded_models)
                
                if self.is_warm:
                    console.print("🟢 Model is WARM (loaded in memory)", style="green")
                    return "warm"
                else:
                    console.print("🔴 Model is COLD (not loaded)", style="red")
                    console.print("  💡 First request will include loading time", style="dim")
                    return "cold"
            else:
                console.print(f"⚠️  Cannot check model status: {response.status_code}", style="yellow")
                return "unknown"
        except Exception as e:
            console.print(f"⚠️  Error checking model status: {e}", style="yellow")
            return "unknown"
    
    def offer_warmup_choice(self):
        """Offer user choice for model warmup."""
        console.print("\n🔥 Model Warmup Options:", style="bold yellow")
        console.print("  1. Continue with cold start (measure real-world performance)")
        console.print("  2. Warm up model first (optimize for consistent benchmarking)")
        
        choice = input("Choose 1 or 2 (or press Enter for 1): ").strip() or "1"
        return choice == "2"
    
    def warmup_model(self):
        """Warm up the model with a simple request."""
        console.print("🔄 Warming up model...", style="yellow")
        
        start_time = time.perf_counter()
        try:
            result = sync_request_basic("Hi")  # Simple warmup
            self.warmup_time = time.perf_counter() - start_time
            
            if result["success"]:
                console.print(f"✅ Model warmed up in {self.warmup_time:.1f}s", style="green")
                self.is_warm = True
                return True
            else:
                console.print("❌ Warmup failed", style="red")
                return False
        except Exception as e:
            console.print(f"❌ Warmup error: {e}", style="red")
            return False

# STRATEGY 2: Adaptive Timeout Management
class AdaptiveTimeoutManager:
    """Manages timeouts based on model state and performance history."""
    
    def __init__(self):
        self.cold_timeout = 45    # First request with model loading
        self.warm_timeout = 15    # Subsequent requests
        self.performance_history = []
    
    def get_timeout(self, is_first_request: bool, model_state: str) -> int:
        """Get appropriate timeout based on context."""
        if model_state == "cold" and is_first_request:
            console.print(f"  ⏱️  Using cold start timeout: {self.cold_timeout}s", style="dim")
            return self.cold_timeout
        elif self.performance_history:
            # Adaptive based on history
            avg_time = sum(self.performance_history) / len(self.performance_history)
            adaptive_timeout = max(int(avg_time * 1.5), self.warm_timeout)
            console.print(f"  ⏱️  Using adaptive timeout: {adaptive_timeout}s (based on {avg_time:.1f}s avg)", style="dim")
            return adaptive_timeout
        else:
            console.print(f"  ⏱️  Using warm timeout: {self.warm_timeout}s", style="dim")
            return self.warm_timeout
    
    def record_success(self, latency_seconds: float):
        """Record successful request for adaptive learning."""
        self.performance_history.append(latency_seconds)
        # Keep only last 5 measurements
        if len(self.performance_history) > 5:
            self.performance_history.pop(0)

# Enhanced request functions with adaptive timeouts
def sync_request_basic(prompt: str) -> dict:
    """Basic sync request for warmup (no adaptive features)."""
    start_time = time.perf_counter()
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 1, "temperature": 0.1}
            },
            timeout=30
        )
        response.raise_for_status()
        
        elapsed = (time.perf_counter() - start_time) * 1000
        result = response.json()
        
        return {
            "prompt": prompt,
            "response": result.get("response", "")[:50] + "...",
            "latency_ms": elapsed,
            "success": True,
            "method": "warmup"
        }
    except Exception as e:
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "prompt": prompt,
            "response": f"Error: {str(e)}",
            "latency_ms": elapsed,
            "success": False,
            "method": "warmup"
        }

def enhanced_sync_request(prompt: str, timeout: int, timeout_manager: AdaptiveTimeoutManager) -> dict:
    """Enhanced sync request with adaptive timeout management."""
    start_time = time.perf_counter()
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 20,      # Limit response length
                    "temperature": 0.1,     # Lower = faster
                    "top_p": 0.9,          # Reduce sampling complexity
                    "top_k": 10,           # Limit vocabulary
                    "num_ctx": 1024,       # Smaller context window
                    "num_thread": -1       # Use all CPU threads
                }
            },
            timeout=timeout # Use adaptive timeout
        )
        response.raise_for_status()
        
        elapsed = (time.perf_counter() - start_time) * 1000
        elapsed_seconds = elapsed / 1000
        
        # Record success for adaptive learning
        timeout_manager.record_success(elapsed_seconds)
        
        result = response.json()
        
        return {
            "prompt": prompt,
            "response": result.get("response", "")[:100] + "...",
            "latency_ms": elapsed,
            "success": True,
            "method": "sync"
        }
    except requests.exceptions.Timeout:
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "prompt": prompt,
            "response": f"Timeout after {timeout}s",
            "latency_ms": elapsed,
            "success": False,
            "method": "sync",
            "error_type": "timeout"
        }
    except Exception as e:
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "prompt": prompt,
            "response": f"Error: {str(e)}",
            "latency_ms": elapsed,
            "success": False,
            "method": "sync",
            "error_type": type(e).__name__
        }

async def enhanced_async_request(prompt: str, timeout: int) -> dict:
    """Enhanced async request with timeout handling."""
    start_time = time.perf_counter()
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 20,
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "top_k": 10,
                        "num_ctx": 1024,
                        "num_thread": -1
                    }
                }
            )
            response.raise_for_status()
            
            elapsed = (time.perf_counter() - start_time) * 1000
            result = response.json()
            
            return {
                "prompt": prompt,
                "response": result.get("response", "")[:100] + "...",
                "latency_ms": elapsed,
                "success": True,
                "method": "async"
            }
    except httpx.TimeoutException:
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "prompt": prompt,
            "response": f"Timeout after {timeout}s",
            "latency_ms": elapsed,
            "success": False,
            "method": "async",
            "error_type": "timeout"
        }
    except Exception as e:
        elapsed = (time.perf_counter() - start_time) * 1000
        return {
            "prompt": prompt,
            "response": f"Error: {str(e)}",
            "latency_ms": elapsed,
            "success": False,
            "method": "async",
            "error_type": type(e).__name__
        }

# Test connection to Ollama API for basic functionality
def test_connection():
    """
    Test basic connection to Ollama, if its API is reachable b4 running benchmarks.
    uses /api/tags endpoint to check if the API is up and running.
    Returns True if connection is successful, False otherwise.
    """
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            console.print(f"✅ Connected! Found {len(models)} models", style="green")
            return True
        else:
            console.print(f"❌ Connection failed: {response.status_code}", style="red")
            return False
    except Exception as e:
        console.print(f"❌ Connection error: {e}", style="red")
        return False

# Enhanced main function integrating both strategies
async def main():
    """Enhanced main function with intelligent state management and adaptive timeouts."""
    console.print(Panel(
        "🎯 Week 1: Enhanced LLM API Benchmark\n"
        "Intelligent State Management + Adaptive Timeout Optimization",
        title="Agentic AI Development",
        border_style="bold magenta"
    ))
    
    # 1. Test connection (unchanged)
    if not test_connection():
        return
    
    # 2. STRATEGY 1: Intelligent Model State Management
    state_manager = ModelStateManager()
    model_state = state_manager.check_model_state()
    
    # 3. STRATEGY 2: Initialize Adaptive Timeout Management
    timeout_manager = AdaptiveTimeoutManager()
    
    # 4. Handle cold start scenario
    if model_state == "cold":
        should_warmup = state_manager.offer_warmup_choice()
        if should_warmup:
            if state_manager.warmup_model():
                model_state = "warm"
    
    console.print(f"\n🚀 Starting benchmark with {model_state} model state...\n")
    
    results = []
    
    # 5. Enhanced Synchronous requests with adaptive timeouts
    console.print("🐌 Running synchronous requests (adaptive timeouts)...", style="yellow")
    sync_start = time.perf_counter()
    for i, prompt in enumerate(TEST_PROMPTS):
        is_first = (i == 0)
        timeout = timeout_manager.get_timeout(is_first, model_state)
        
        result = enhanced_sync_request(prompt, timeout, timeout_manager)
        results.append(result)
        
        status = "✅" if result["success"] else "❌"
        if result["success"]:
            timing = f"{result['latency_ms']:.1f}ms"
        else:
            timing = f"FAILED ({result.get('error_type', 'unknown')})"
        
        console.print(f"  {status} {timing}: {prompt}")
    sync_total = time.perf_counter() - sync_start
    
    # 6. Enhanced Asynchronous requests
    console.print("\n⚡ Running async requests...", style="blue")
    async_start = time.perf_counter()
    for prompt in TEST_PROMPTS:
        timeout = timeout_manager.get_timeout(False, "warm")  # Should be warm by now
        result = await enhanced_async_request(prompt, timeout)
        results.append(result)
        
        status = "✅" if result["success"] else "❌"
        timing = f"{result['latency_ms']:.1f}ms" if result["success"] else f"FAILED ({result.get('error_type', 'unknown')})"
        console.print(f"  {status} {timing}: {prompt}")
    async_total = time.perf_counter() - async_start

    # 7. Concurrent requests
    console.print("\n🚀 Running concurrent requests...", style="green")
    concurrent_start = time.perf_counter()
    warm_timeout = timeout_manager.get_timeout(False, "warm")
    tasks = [enhanced_async_request(prompt, warm_timeout) for prompt in TEST_PROMPTS]
    concurrent_results = await asyncio.gather(*tasks, return_exceptions=True)
    concurrent_total = time.perf_counter() - concurrent_start
    
    for result in concurrent_results:
        if isinstance(result, dict):
            results.append({**result, "method": "concurrent"})
            status = "✅" if result["success"] else "❌"
            timing = f"{result['latency_ms']:.1f}ms" if result["success"] else f"FAILED ({result.get('error_type', 'unknown')})"
            console.print(f"  {status} {timing}: {result['prompt']}")
    
    # 8. Enhanced Performance Analysis
    analyze_enhanced_results(results, model_state, state_manager, timeout_manager)

def analyze_enhanced_results(results, model_state, state_manager, timeout_manager):
    """Enhanced analysis with state management insights."""
    console.print("\n📊 Enhanced Performance Analysis", style="bold cyan")
    
    # Success rates and performance
    table = Table()
    table.add_column("Method", style="cyan")
    table.add_column("Success Rate", style="green")
    table.add_column("Avg Latency", style="yellow")
    table.add_column("Optimization", style="magenta")
    
    methods = ["sync", "async", "concurrent"]
    for method in methods:
        method_results = [r for r in results if r["method"] == method]
        successful = [r for r in method_results if r["success"]]
        
        if method_results:
            success_rate = len(successful) / len(method_results) * 100
            avg_latency = sum(r["latency_ms"] for r in successful) / len(successful) if successful else 0
            
            # Optimization insight
            if method == "sync" and success_rate == 100:
                optimization = "✅ State mgmt working"
            elif method == "async" and avg_latency < 5000:
                optimization = "✅ Timeouts optimized"
            elif method == "concurrent" and success_rate > 80:
                optimization = "✅ Parallel efficiency"
            else:
                optimization = "⚠️  Needs tuning"
            
            table.add_row(
                method.title(),
                f"{success_rate:.1f}%",
                f"{avg_latency:.1f}ms" if avg_latency > 0 else "N/A",
                optimization
            )
    
    console.print(table)
    
    # Strategy effectiveness summary
    console.print("\n💡 Strategy Effectiveness:", style="bold yellow")
    console.print(f"  🧠 Model State: Started {model_state}, ended warm")
    if state_manager.warmup_time:
        console.print(f"  🔥 Warmup Time: {state_manager.warmup_time:.1f}s")
    if timeout_manager.performance_history:
        avg_perf = sum(timeout_manager.performance_history) / len(timeout_manager.performance_history)
        console.print(f"  ⏱️  Adaptive Learning: {len(timeout_manager.performance_history)} samples, {avg_perf:.1f}s avg")
    
    console.print(f"\n🎉 Week 1 Enhanced Complete! 🚀", style="bold green")

if __name__ == "__main__":
    asyncio.run(main())