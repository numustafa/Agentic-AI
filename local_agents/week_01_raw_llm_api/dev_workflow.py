"""
STRATEGY 3: Development Workflow Orchestration
Manages and coordinates all your Week 1 tools for efficient development
"""

import subprocess
import time
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def main_menu():
    """Main development workflow menu."""
    console.print(Panel(
        "🛠️  Week 1 LLM Development Workflow\n"
        "Orchestrates your benchmark tools for efficient development",
        title="Strategy 3: Workflow Orchestration",
        border_style="bold blue"
    ))
    
    while True:
        console.print("\n📋 Available Tools:", style="bold cyan")
        console.print("  1. quick-test     - Fast connection check (30s)")
        console.print("  2. basic-bench    - Original hello_llm.py")  
        console.print("  3. enhanced-bench - Enhanced with strategies 1&2")
        console.print("  4. explained      - Deep dive learning module")
        console.print("  5. cold-warm      - Explicit cold vs warm comparison")
        console.print("  6. compare-all    - Run multiple benchmarks and compare")
        console.print("  7. system-status  - Check Ollama and model status")
        console.print("  q. quit")
        
        choice = input("\nChoose tool: ").strip().lower()
        
        if choice == "q" or choice == "quit":
            console.print("👋 Happy coding!", style="green")
            break
        elif choice == "1":
            quick_test()
        elif choice == "2":
            run_basic_benchmark()
        elif choice == "3":
            run_enhanced_benchmark()
        elif choice == "4":
            run_explained_module()
        elif choice == "5":
            run_cold_warm_analysis()
        elif choice == "6":
            compare_all_approaches()
        elif choice == "7":
            check_system_status()
        else:
            console.print("❌ Invalid choice. Try again.", style="red")

def quick_test():
    """Quick 30-second connectivity and performance test."""
    console.print("🧪 Quick Test - 30 Second Check", style="yellow")
    
    start_time = time.time()
    try:
        result = subprocess.run([
            "python", "-c", 
            """
import requests, time
start = time.perf_counter()
resp = requests.post(
    'http://host.docker.internal:11434/api/generate',
    json={'model': 'qwen3:latest', 'prompt': 'Hi', 'stream': False, 'options': {'num_predict': 3}},
    timeout=25
)
elapsed = time.perf_counter() - start
if resp.status_code == 200:
    print(f'✅ Model responding in {elapsed:.1f}s')
else:
    print(f'❌ Failed: {resp.status_code}')
            """
        ], capture_output=True, text=True, timeout=30)
        
        elapsed = time.time() - start_time
        console.print(result.stdout.strip())
        console.print(f"Total test time: {elapsed:.1f}s", style="dim")
        
    except subprocess.TimeoutExpired:
        console.print("❌ Quick test timed out - model may be cold", style="red")
    except Exception as e:
        console.print(f"❌ Test failed: {e}", style="red")

def run_basic_benchmark():
    """Run original hello_llm.py."""
    console.print("🎯 Running Basic Benchmark (Original)", style="blue")
    try:
        subprocess.run(["python", "hello_llm.py"], check=True)
    except subprocess.CalledProcessError:
        console.print("❌ Basic benchmark failed", style="red")
    except FileNotFoundError:
        console.print("❌ hello_llm.py not found", style="red")

def run_enhanced_benchmark():
    """Run enhanced version with strategies 1&2."""
    console.print("🚀 Running Enhanced Benchmark (Strategies 1&2)", style="green")
    try:
        # This would run your enhanced hello_llm.py from Step 1
        subprocess.run(["python", "hello_llm.py"], check=True)
    except subprocess.CalledProcessError:
        console.print("❌ Enhanced benchmark failed", style="red")

def run_explained_module():
    """Run the learning/explanation module."""
    console.print("🎓 Running Deep Learning Module", style="magenta")
    try:
        subprocess.run(["python", "hello_llm_explained.py"], check=True)
    except subprocess.CalledProcessError:
        console.print("❌ Explained module failed", style="red")

def run_cold_warm_analysis():
    """Run explicit cold vs warm analysis."""
    console.print("❄️🔥 Running Cold vs Warm Analysis", style="cyan")
    try:
        subprocess.run(["python", "cold_warm_benchmark.py"], check=True)
    except subprocess.CalledProcessError:
        console.print("❌ Cold/warm analysis failed", style="red")

def compare_all_approaches():
    """Run multiple benchmarks and compare results."""
    console.print("📊 Comprehensive Comparison", style="bold cyan")
    console.print("Running multiple tools to compare approaches...\n")
    
    # This would orchestrate running multiple tools and collecting results
    tools = [
        ("Quick Test", quick_test),
        ("Basic Benchmark", run_basic_benchmark), 
        ("Cold/Warm Analysis", run_cold_warm_analysis)
    ]
    
    for tool_name, tool_func in tools:
        console.print(f"🔄 Running {tool_name}...", style="yellow")
        try:
            tool_func()
            console.print(f"✅ {tool_name} completed\n", style="green")
        except Exception as e:
            console.print(f"❌ {tool_name} failed: {e}\n", style="red")

def check_system_status():
    """Check Ollama and model status."""
    console.print("🔍 System Status Check", style="bold cyan")
    
    try:
        # Check Ollama connection
        result = subprocess.run([
            "curl", "-s", "http://host.docker.internal:11434/api/tags"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            console.print("✅ Ollama service reachable", style="green")
            
            # Check loaded models
            ps_result = subprocess.run([
                "curl", "-s", "http://host.docker.internal:11434/api/ps"
            ], capture_output=True, text=True, timeout=5)
            
            if "qwen3:latest" in ps_result.stdout:
                console.print("🟢 qwen3:latest is loaded (warm)", style="green")
            else:
                console.print("🔴 qwen3:latest not loaded (cold)", style="red")
                
        else:
            console.print("❌ Ollama service not reachable", style="red")
            
    except Exception as e:
        console.print(f"❌ Status check failed: {e}", style="red")

if __name__ == "__main__":
    main_menu()