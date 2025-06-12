import asyncio
from fastmcp import FastMCP
from language_tool_python import LanguageTool

# Create FastMCP server instance
mcp_server = FastMCP(
    name="LanguageTool MCP Server",
    instructions=(
        "Use LanguageTool to check grammar and spelling. "
        "The tool 'check_text' returns suggestions for the provided text."
    ),
)

# Initialize LanguageTool once
_tool = LanguageTool('en-US')

@mcp_server.tool(name="check_text", description="Check text using LanguageTool")
async def check_text(text: str) -> str:
    loop = asyncio.get_event_loop()
    matches = await loop.run_in_executor(None, _tool.check, text)
    if not matches:
        return "No issues found."
    suggestions = []
    for m in matches:
        suggestions.append(f"{m.ruleId}: {m.message} at {m.offset}-{m.errorLength}")
    return "\n".join(suggestions)

if __name__ == "__main__":
    asyncio.run(mcp_server.run_sse_async(host="0.0.0.0", port=8080))
