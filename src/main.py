#!/usr/bin/env python3
"""
Main entry point for Data Exploration MCP Server

This module provides the MCP server interface for dynamic data analysis
during technical interviews. Designed to handle unknown datasets with
professional-grade analysis and real-time collaboration.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession
from mcp.types import Resource, Tool
import typer

# Add project root to path for imports
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# Simplified imports for streamlined system
# Core functionality is now in simple_mcp_server.py

# Configure logging for professional debugging
# For MCP mode, only use console logging to avoid file system issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# CLI application for direct usage
app = typer.Typer(
    name="data-exploration-mcp",
    help="Dynamic data analysis MCP server for technical interviews",
    add_completion=False
)

# Global configuration from environment
INTERVIEW_CONFIG = {
    "INTERVIEW_MODE": os.getenv("INTERVIEW_MODE", "true").lower() == "true",
    "TIME_LIMIT_MINUTES": int(os.getenv("TIME_LIMIT_MINUTES", "60")),
    "AUTO_INSIGHTS": os.getenv("AUTO_INSIGHTS", "true").lower() == "true",
    "VERBOSE_EXPLANATIONS": os.getenv("VERBOSE_EXPLANATIONS", "true").lower() == "true",
    "PROFESSIONAL_OUTPUT": os.getenv("PROFESSIONAL_OUTPUT", "true").lower() == "true",
    "COLLABORATION_ENABLED": os.getenv("COLLABORATION_ENABLED", "true").lower() == "true",
    "MEMORY_OPTIMIZATION": os.getenv("MEMORY_OPTIMIZATION", "true").lower() == "true",
}

# MCP server initialization is handled in simple_mcp_server.py

@app.command()
def serve(
    host: str = typer.Option("localhost", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
    interview_mode: bool = typer.Option(True, help="Enable interview optimization mode"),
    time_limit: int = typer.Option(60, help="Interview time limit in minutes"),
    verbose: bool = typer.Option(False, help="Enable verbose logging"),
) -> None:
    """
    Start the Data Exploration MCP server for live analysis.
    
    This command starts the server in interview mode, optimized for
    60-minute technical interviews with unknown datasets.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        
    logger.info(f"🚀 Starting Data Exploration MCP Server")
    logger.info(f"📊 Interview Mode: {interview_mode}")
    logger.info(f"⏱️ Time Limit: {time_limit} minutes")
    logger.info(f"🔗 Server URL: http://{host}:{port}")
    
    # Update configuration
    INTERVIEW_CONFIG.update({
        "INTERVIEW_MODE": interview_mode,
        "TIME_LIMIT_MINUTES": time_limit,
    })
    
    # Start the simple MCP server
    try:
        from src.simple_mcp_server import main as mcp_main
        asyncio.run(mcp_main())
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        raise typer.Exit(1)

@app.command()
def analyze(
    file_path: str = typer.Argument(..., help="Path to dataset file"),
) -> None:
    """
    Perform quick analysis of a dataset (non-MCP mode).
    """
    if not Path(file_path).exists():
        typer.echo(f"❌ File not found: {file_path}")
        raise typer.Exit(1)
        
    logger.info(f"🔍 Quick analysis of: {file_path}")
    
    try:
        import pandas as pd
        data = pd.read_csv(file_path)
        
        typer.echo(f"📊 Dataset: {len(data):,} rows × {len(data.columns)} columns")
        typer.echo(f"💾 Memory usage: {data.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        typer.echo(f"📈 Data types: {data.dtypes.value_counts().to_dict()}")
        typer.echo("✅ Use MCP server for full optimized analysis")
        
    except Exception as e:
        typer.echo(f"❌ Analysis failed: {e}")
        raise typer.Exit(1)

@app.command()
def test_optimization(
    file_path: str = typer.Argument(..., help="Path to dataset file"),
) -> None:
    """
    Test memory optimization on a dataset.
    """
    if not Path(file_path).exists():
        typer.echo(f"❌ File not found: {file_path}")
        raise typer.Exit(1)
        
    try:
        import pandas as pd
        data = pd.read_csv(file_path)
        original_memory = data.memory_usage(deep=True).sum() / (1024*1024)
        
        # Simple optimization
        optimized_data = data.copy()
        for col in optimized_data.columns:
            if optimized_data[col].dtype == 'object':
                unique_ratio = optimized_data[col].nunique() / len(optimized_data)
                if unique_ratio < 0.5:
                    optimized_data[col] = optimized_data[col].astype('category')
        
        optimized_memory = optimized_data.memory_usage(deep=True).sum() / (1024*1024)
        reduction = ((original_memory - optimized_memory) / original_memory) * 100
        
        typer.echo(f"🧠 Memory Optimization Results:")
        typer.echo(f"   • Original: {original_memory:.1f} MB")
        typer.echo(f"   • Optimized: {optimized_memory:.1f} MB") 
        typer.echo(f"   • Reduction: {reduction:.1f}%")
        typer.echo("✅ Use MCP server for full production workflow")
        
    except Exception as e:
        typer.echo(f"❌ Optimization failed: {e}")
        raise typer.Exit(1)

@app.command()
def version() -> None:
    """Show version information."""
    from src import __version__, __author__, __description__
    
    typer.echo(f"Veeam Interview Analyzer v{__version__}")
    typer.echo(f"Author: {__author__}")
    typer.echo(f"Description: {__description__}")

def main() -> None:
    """Main entry point for the application."""
    # Handle MCP server mode (default when called as module)
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ["-m", "--mcp"]):
        logger.info("🚀 Starting in MCP server mode")
        # Use the simple MCP server
        from src.simple_mcp_server import main as mcp_main
        asyncio.run(mcp_main())
    else:
        # Handle CLI commands
        app()

if __name__ == "__main__":
    main()
