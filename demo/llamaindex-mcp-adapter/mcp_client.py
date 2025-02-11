from contextlib import asynccontextmanager
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import StdioServerParameters, stdio_client
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self, command_or_url: str, args: list[str] = [], env: dict[str, str] = {}):
        self.command_or_url = command_or_url
        self.args = args
        self.env = env

    async def _receive_loop(self, session: ClientSession):
        logger.info("Starting receive loop")
        async for message in session.incoming_messages:
            if isinstance(message, Exception):
                logger.error("Error: %s", message)
                continue
            logger.info("Received message from server: %s", message)

    @asynccontextmanager
    async def _run_session(self):
        if urlparse(self.command_or_url).scheme in ("http", "https"):
            async with sse_client(self.command_or_url) as streams:
                async with ClientSession(*streams) as session:
                    logger.info("Initializing session")
                    await session.initialize()
                    yield session
        else:
            server_parameters = StdioServerParameters(
                command=self.command_or_url, args=self.args, env=self.env
            )
            async with stdio_client(server_parameters) as streams:
                async with ClientSession(*streams) as session:
                    logger.info("Initializing session")
                    await session.initialize()
                    yield session

    async def call_tool(self, tool_name: str, arguments: dict):
        async with self._run_session() as session:
            return await session.call_tool(tool_name, arguments)

    async def list_tools(self):
        async with self._run_session() as session:
            return await session.list_tools()
