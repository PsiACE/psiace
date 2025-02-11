# Integrate MCP tools into LlamaIndex

This repo is a demo of integrating MCP (ModelContextProtocol, https://modelcontextprotocol.io) tools into LlamaIndex (https://github.com/run-llama/llama_index).

## How to Use

1. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Edit the environment variables in `.env`

```bash
cp .env.example .env
```

> Note: To run the demo, you need to set the `IPINFO_API_TOKEN` in the `.env` file. You can get the token from [IPInfo](https://ipinfo.io/). And you need Azure OpenAI account to run the demo, or you can modify the `llamaindex_mcp_example.py` to use other LLM providers.

4. Run the demo with following command

**SSE Mode**

```bash
python mcp_server.py --server_type sse
python llamaindex_mcp_example.py --client_type sse
```

**StdIO Mode**

```bash
python llamaindex_mcp_example.py --client_type stdio
```

## Learn More

- [Integrate MCP tools into LlamaIndex](https://psiace.me/posts/integrate-mcp-tools-into-llamaindex/)
