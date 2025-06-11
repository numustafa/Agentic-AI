"""
Week 1 Extension: Cold vs Warm Start Analysis
Explicitly tests both cold and warm performance scenarios.
"""

import requests
import time
from rich.console import Console

# Import the correct functions from enhanced hello_llm.py
try:
    from hello_llm import sync_request_basic, MODEL, OLLAMA_BASE_URL, console
except ImportError:
    # Fallback if old version
    console = Console()
    OLLAMA_BASE_URL = "http://host.docker.internal:11434"
    MODEL = "qwen3:latest"
    
    def sync_request_basic(prompt: str) -> dict:
        """Basic sync request fallback."""
        start_time = time.perf_counter()
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": 10, "temperature": 0.1}
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
                "method": "basic"
            }
        except Exception as e:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "prompt": prompt,
                "response": f"Error: {str(e)}",
                "latency_ms": elapsed,
                "success": False,
                "method": "basic"
            }

def test_cold_vs_warm():
    """Compare cold start vs warm performance explicitly."""
    console.print("🎯 Cold vs Warm Start Comparison", style="bold magenta")
    
    # Test 1: Current state
    console.print("\n📊 Test 1: Current State Performance")
    current_result = sync_request_basic("Hello")
    console.print(f"Current request: {current_result['latency_ms']:.1f}ms")
    
    # Test 2: Ensure warm state
    console.print("\n📊 Test 2: Warm State Performance (3 requests)")
    warm_times = []
    for i in range(3):
        result = sync_request_basic(f"Test {i+1}")
        warm_times.append(result['latency_ms'])
        console.print(f"Warm request {i+1}: {result['latency_ms']:.1f}ms")
    
    avg_warm = sum(warm_times) / len(warm_times)
    console.print(f"Average warm performance: {avg_warm:.1f}ms")
    
    # Analysis
    console.print("\n📈 Analysis:", style="bold cyan")
    if current_result['latency_ms'] > avg_warm * 2:
        cold_overhead = current_result['latency_ms'] - avg_warm
        console.print(f"🐌 Cold start detected! Overhead: {cold_overhead:.1f}ms", style="red")
    else:
        console.print("⚡ Model was already warm", style="green")

if __name__ == "__main__":
    test_cold_vs_warm()