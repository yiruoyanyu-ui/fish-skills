"""Read-only stdio MCP; media execution stays with the Fish Audio MCP server."""
import asyncio
import os

from mcp.server.fastmcp import FastMCP

from .reader import SkillReader
from .storage import configured_store


def main():
    reader = SkillReader(configured_store(), os.getenv("FISH_SKILLS_CHANNEL", "preview"))
    server = FastMCP("Fish Skills", instructions=(
        "Use list_skills to discover media workflows. For a matching task fetch get_skill_instructions, "
        "then fetch required references using get_skill_file with the returned fixed version. "
        "Follow delivery_instructions, including routing other Skills by their ID. "
        "These are read-only documents; generation requires the separately connected Fish Audio MCP. "
        "Experimental means quality has not been independently accepted; dormant means not supported."
    ))

    @server.tool()
    async def list_skills(version: str | None = None) -> dict:
        """List Skill IDs, descriptions, status and fixed content version; no generation."""
        return await asyncio.to_thread(reader.list_skills, version)

    @server.tool()
    async def get_skill_instructions(skill_id: str, version: str | None = None) -> dict:
        """Get Markdown and reference paths; omitted version resolves the configured channel."""
        return await asyncio.to_thread(reader.get_instructions, skill_id, version)

    @server.tool()
    async def get_skill_file(version: str, path: str) -> dict:
        """Get one UTF-8 file by exact manifest package path and pinned content version."""
        return await asyncio.to_thread(reader.get_file, version, path)

    server.run(transport="stdio")


if __name__ == "__main__":
    main()
