#!/usr/bin/env python3
"""
Test script to verify MCP server connection and functionality.
Run this to diagnose any connection issues.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

async def test_mcp_server():
    """Test MCP server functionality."""
    print("🔧 Testing MCP Server Components...")
    print("=" * 50)
    
    success_count = 0
    total_tests = 5
    
    # Test 1: Import server
    try:
        from src.simple_mcp_server import server, ANALYSIS_STEPS, analysis_session
        print("✅ Test 1/5: MCP server imports successful")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 1/5: MCP server import failed: {e}")
    
    # Test 2: Server initialization
    try:
        print(f"✅ Test 2/5: Server initialized with {len(ANALYSIS_STEPS)} analysis steps")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 2/5: Server initialization failed: {e}")
    
    # Test 3: Tool handlers
    try:
        from src.simple_mcp_server import handle_dataset_overview, handle_optimize_memory
        print("✅ Test 3/5: Tool handlers available")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 3/5: Tool handlers failed: {e}")
    
    # Test 4: Test dataset exists
    test_file = project_root / "test_dataset.csv"
    if test_file.exists():
        print("✅ Test 4/5: Test dataset available")
        success_count += 1
    else:
        print("❌ Test 4/5: Test dataset missing")
    
    # Test 5: Basic analysis test
    try:
        if test_file.exists():
            result = await handle_dataset_overview({"file_path": str(test_file)})
            if result.get("status") == "success":
                print("✅ Test 5/5: Basic analysis works")
                success_count += 1
            else:
                print(f"❌ Test 5/5: Analysis failed: {result.get('error', 'Unknown error')}")
        else:
            print("⚠️  Test 5/5: Skipped - no test dataset")
            success_count += 1
    except Exception as e:
        print(f"❌ Test 5/5: Analysis test failed: {e}")
    
    print("=" * 50)
    print(f"📊 Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 MCP SERVER READY!")
        print("\n🚀 Connection troubleshooting:")
        print("1. The server components are working correctly")
        print("2. If you still get 'upstream connect error':")
        print("   - Restart Claude Desktop completely (Cmd+Q)")
        print("   - Wait 15-20 seconds for full initialization")
        print("   - Check that no other Python processes are running")
        print("   - Try the simple test: 'Get dataset overview of test_dataset.csv'")
        
        print("\n🛠️ Available tools:")
        tools = [
            "dataset_overview", "numeric_exploration", "distribution_checks",
            "correlation_analysis", "scatter_plots", "temporal_analysis", 
            "full_exploration_report", "optimize_memory", "discover_data",
            "explain_methodology", "start_guided_analysis", "continue_analysis"
        ]
        for i, tool in enumerate(tools, 1):
            print(f"   {i:2d}. {tool}")
        
        return 0
    else:
        print("⚠️  Some components have issues. Check the errors above.")
        return 1

def main():
    """Run the test."""
    return asyncio.run(test_mcp_server())

if __name__ == "__main__":
    sys.exit(main())
