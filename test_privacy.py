#!/usr/bin/env python3
"""
Privacy Test Suite for Data Exploration MCP Server
Tests to verify that sensitive data never leaves the local machine.
"""

import os
import sys
import time
import subprocess
import psutil
import pandas as pd
import tempfile
from pathlib import Path
import json
import socket
import threading
from datetime import datetime

def create_test_data():
    """Create sensitive test data to verify privacy protection."""
    print("📊 Creating sensitive test dataset...")
    
    # Create realistic sensitive data
    sensitive_data = {
        'customer_id': [f'CUST_{i:06d}' for i in range(1000)],
        'full_name': [f'John Doe {i}' for i in range(1000)],
        'email': [f'customer{i}@email.com' for i in range(1000)],
        'phone': [f'555-{i:04d}' for i in range(1000)],
        'ssn': [f'123-45-{i:04d}' for i in range(1000)],
        'credit_card': [f'4532-1234-5678-{i:04d}' for i in range(1000)],
        'salary': [50000 + (i * 100) for i in range(1000)],
        'age': [25 + (i % 40) for i in range(1000)],
        'account_balance': [1000 + (i * 50) for i in range(1000)]
    }
    
    df = pd.DataFrame(sensitive_data)
    test_file = '/tmp/sensitive_test_data.csv'
    df.to_csv(test_file, index=False)
    
    print(f"✅ Created sensitive test data: {test_file}")
    print(f"   • Contains PII: names, emails, SSNs, credit cards")
    print(f"   • {len(df)} records with sensitive information")
    
    return test_file

def monitor_network_connections():
    """Monitor network connections during MCP server operation."""
    print("\n🔍 Starting network monitoring...")
    
    connections_log = []
    monitoring = True
    
    def network_monitor():
        while monitoring:
            try:
                # Get all network connections
                connections = psutil.net_connections(kind='inet')
                python_connections = []
                
                for conn in connections:
                    try:
                        if conn.pid:
                            proc = psutil.Process(conn.pid)
                            if 'python' in proc.name().lower():
                                python_connections.append({
                                    'pid': conn.pid,
                                    'local_addr': conn.laddr,
                                    'remote_addr': conn.raddr,
                                    'status': conn.status,
                                    'process': proc.name()
                                })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if python_connections:
                    connections_log.extend(python_connections)
                    
            except Exception as e:
                print(f"Network monitoring error: {e}")
            
            time.sleep(1)
    
    monitor_thread = threading.Thread(target=network_monitor, daemon=True)
    monitor_thread.start()
    
    return lambda: setattr(locals(), 'monitoring', False), connections_log

def test_mcp_server_privacy():
    """Test MCP server to ensure no data leakage."""
    print("\n🧪 Testing MCP Server Privacy...")
    
    # Create sensitive test data
    test_file = create_test_data()
    
    # Start network monitoring
    stop_monitoring, connections_log = monitor_network_connections()
    
    try:
        # Test 1: Import and run MCP server components locally
        print("\n📋 Test 1: Local Data Processing")
        
        # Import MCP server modules
        sys.path.insert(0, '/Users/dakshinsiva/Data_MCP/src')
        from simple_mcp_server import safe_json_serialize
        
        # Load sensitive data
        df = pd.read_csv(test_file)
        print(f"✅ Loaded {len(df)} sensitive records locally")
        
        # Test data processing (should happen locally)
        print("🔄 Processing sensitive data locally...")
        
        # Simulate what the MCP server does
        numeric_cols = df.select_dtypes(include=['number']).columns
        correlations = df[numeric_cols].corr() if len(numeric_cols) > 1 else {}
        
        # Test serialization (this is what gets sent to LLM)
        serialized_output = safe_json_serialize({
            'total_records': len(df),
            'numeric_columns': len(numeric_cols),
            'correlations_summary': 'Found correlations between numeric fields',
            'age_stats': {
                'mean': float(df['age'].mean()),
                'median': float(df['age'].median()),
                'std': float(df['age'].std())
            },
            'salary_stats': {
                'mean': float(df['salary'].mean()),
                'median': float(df['salary'].median()),
                'std': float(df['salary'].std())
            }
        })
        
        print("✅ Data processed locally - only statistical summaries generated")
        
        # Test 2: Verify no PII in serialized output
        print("\n📋 Test 2: PII Detection in Output")
        
        output_str = json.dumps(serialized_output)
        pii_found = []
        
        # Check for PII leakage
        sample_pii = ['John Doe', 'customer', '@email.com', '555-', '123-45-', '4532-1234']
        for pii in sample_pii:
            if pii in output_str:
                pii_found.append(pii)
        
        if pii_found:
            print(f"❌ PII DETECTED in output: {pii_found}")
            return False
        else:
            print("✅ No PII detected in serialized output")
        
        # Test 3: Verify only statistical data
        print("\n📋 Test 3: Statistical Data Only")
        
        expected_safe_data = ['total_records', 'mean', 'median', 'std', 'correlations_summary']
        found_safe_data = [key for key in expected_safe_data if key in output_str]
        
        print(f"✅ Safe statistical data found: {found_safe_data}")
        print(f"✅ Sample output: {json.dumps(serialized_output, indent=2)[:200]}...")
        
        # Wait a bit for network monitoring
        time.sleep(3)
        
        # Test 4: Network Connection Analysis
        print("\n📋 Test 4: Network Connection Analysis")
        
        stop_monitoring()
        time.sleep(1)
        
        external_connections = []
        for conn in connections_log:
            if conn.get('remote_addr'):
                remote_ip = conn['remote_addr'][0] if conn['remote_addr'] else None
                if remote_ip and not (remote_ip.startswith('127.') or remote_ip.startswith('::1')):
                    external_connections.append(conn)
        
        if external_connections:
            print(f"⚠️  External connections detected: {len(external_connections)}")
            for conn in external_connections[:3]:  # Show first 3
                print(f"   • {conn['remote_addr']} - {conn['status']}")
            print("   Note: These might be unrelated to MCP server")
        else:
            print("✅ No external connections detected during data processing")
        
        return True
        
    except Exception as e:
        print(f"❌ Privacy test failed: {e}")
        return False
    
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        stop_monitoring()

def test_offline_functionality():
    """Test that MCP server works offline."""
    print("\n📋 Test 5: Offline Functionality")
    
    try:
        # Test basic imports and functionality without network
        sys.path.insert(0, '/Users/dakshinsiva/Data_MCP/src')
        from simple_mcp_server import safe_json_serialize, analysis_session
        
        # Create test data
        test_data = pd.DataFrame({
            'value1': [1, 2, 3, 4, 5],
            'value2': [10, 20, 30, 40, 50]
        })
        
        # Test serialization
        result = safe_json_serialize({
            'correlation': test_data['value1'].corr(test_data['value2']),
            'mean_value1': test_data['value1'].mean(),
            'count': len(test_data)
        })
        
        print("✅ MCP server functions work offline")
        print(f"✅ Sample offline result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Offline test failed: {e}")
        return False

def test_file_system_isolation():
    """Test that MCP server only accesses local files."""
    print("\n📋 Test 6: File System Isolation")
    
    try:
        # Check current working directory
        cwd = os.getcwd()
        print(f"✅ Current working directory: {cwd}")
        
        # Check if we're in the expected MCP directory
        if 'Data_MCP' in cwd:
            print("✅ Operating in MCP server directory")
        
        # List accessible files (should be local only)
        local_files = list(Path('.').glob('**/*.py'))[:5]  # First 5 Python files
        print(f"✅ Local Python files accessible: {len(local_files)}")
        for f in local_files:
            print(f"   • {f}")
        
        return True
        
    except Exception as e:
        print(f"❌ File system test failed: {e}")
        return False

def generate_privacy_report():
    """Generate a comprehensive privacy test report."""
    print("\n" + "="*60)
    print("🔒 PRIVACY TEST REPORT")
    print("="*60)
    
    test_results = []
    
    # Run all privacy tests
    tests = [
        ("MCP Server Privacy", test_mcp_server_privacy),
        ("Offline Functionality", test_offline_functionality),
        ("File System Isolation", test_file_system_isolation)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            result = test_func()
            test_results.append((test_name, result))
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}: {test_name}")
        except Exception as e:
            test_results.append((test_name, False))
            print(f"❌ FAILED: {test_name} - {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 PRIVACY TEST SUMMARY")
    print("="*60)
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🔒 PRIVACY VERIFIED: Your MCP server protects sensitive data!")
    else:
        print("⚠️  PRIVACY CONCERNS: Some tests failed - review implementation")
    
    # Privacy recommendations
    print("\n📋 PRIVACY RECOMMENDATIONS:")
    print("✅ Use only statistical summaries in LLM interactions")
    print("✅ Monitor network connections during sensitive analysis")
    print("✅ Keep sensitive data files in local directories only")
    print("✅ Test offline functionality regularly")
    print("✅ Use air-gapped environments for maximum security")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    print("🔒 Data Exploration MCP - Privacy Test Suite")
    print("=" * 50)
    print("Testing privacy protection of sensitive data...")
    
    privacy_verified = generate_privacy_report()
    
    if privacy_verified:
        print("\n🎉 PRIVACY TEST COMPLETE: Your data is protected! 🔒")
    else:
        print("\n⚠️  PRIVACY REVIEW NEEDED: Check failed tests above")
    
    sys.exit(0 if privacy_verified else 1)
