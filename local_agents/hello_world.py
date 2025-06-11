# This is a simple Python script to test the Dev Container setup.
print("🎉 Dev Container is working!")
print("Python version:", __import__('sys').version)

# Test async (for Week 1)
import asyncio
async def test_async():
    return "✅ Asyncio ready for Week 1!"

print(asyncio.run(test_async()))