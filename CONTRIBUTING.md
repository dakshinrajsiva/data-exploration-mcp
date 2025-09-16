# Contributing to Data Exploration MCP

Thank you for your interest in contributing to Data Exploration MCP! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Basic understanding of MCP (Model Context Protocol)
- Familiarity with data analysis and pandas

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/dakshinsiva/data-exploration-mcp.git
   cd data-exploration-mcp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Test the installation**
   ```bash
   python test_mcp_connection.py
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Keep functions focused and concise

### Testing
- Write tests for new features
- Ensure all existing tests pass before submitting PR
- Test with different dataset formats (CSV, Excel, JSON, Parquet)

### Documentation
- Update README.md for significant changes
- Add docstrings for new functions
- Update tool documentation if adding new MCP tools

## 🎯 How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Sample dataset (if applicable)

### Suggesting Features
1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Proposed implementation approach

### Submitting Code Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, tested code
   - Follow existing code patterns
   - Add/update documentation

4. **Test your changes**
   ```bash
   python test_mcp_connection.py
   python -m src.main analyze test_dataset.csv
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description of changes
   - Reference related issues
   - Include screenshots for UI changes

## 🏗️ Architecture Overview

### Core Components
- **`src/simple_mcp_server.py`** - Main MCP server with 13 analysis tools
- **`src/main.py`** - CLI interface and entry point
- **Memory Optimization** - Production-grade dtype optimization
- **Analysis Workflow** - 5-phase systematic exploration

### Adding New MCP Tools

1. **Define the tool in `simple_mcp_server.py`**
   ```python
   Tool(
       name="your_tool_name",
       description="Clear description of what the tool does",
       inputSchema={
           "type": "object",
           "properties": {
               "parameter_name": {
                   "type": "string",
                   "description": "Parameter description"
               }
           },
           "required": ["parameter_name"]
       }
   )
   ```

2. **Create the handler function**
   ```python
   async def handle_your_tool_name(arguments: dict) -> list[TextContent]:
       """Handle your new tool functionality."""
       # Implementation here
       return [TextContent(type="text", text="Result")]
   ```

3. **Register the handler**
   ```python
   @server.call_tool()
   async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
       if name == "your_tool_name":
           return await handle_your_tool_name(arguments)
   ```

## 🎯 Priority Areas for Contribution

### High Priority
- **New Data Formats** - Support for more file formats (HDF5, Feather, etc.)
- **Advanced Visualizations** - Interactive plots, statistical charts
- **Performance Optimizations** - Memory usage, processing speed
- **Statistical Tests** - More hypothesis testing capabilities

### Medium Priority
- **Export Capabilities** - Save analysis results in various formats
- **Configuration Options** - User-customizable analysis parameters
- **Error Handling** - Better error messages and recovery
- **Documentation** - More examples and tutorials

### Low Priority
- **UI Improvements** - Better CLI interface
- **Logging Enhancements** - More detailed logging options
- **Code Refactoring** - Improve code organization

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes
- [ ] No breaking changes (or clearly documented)

## 🤝 Community Guidelines

### Be Respectful
- Use inclusive language
- Be constructive in feedback
- Help newcomers get started
- Respect different perspectives and experience levels

### Be Collaborative
- Share knowledge and resources
- Provide helpful code reviews
- Suggest improvements constructively
- Celebrate others' contributions

## 📞 Getting Help

- **Issues**: Create a GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
- **Documentation**: Check the README and guides first

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks for major features or fixes

## 📄 License

By contributing to Data Exploration MCP, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Data Exploration MCP! Your contributions help make data analysis more accessible and efficient for everyone. 🚀
