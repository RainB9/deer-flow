FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv


# 安装 curl 和 xz-utils（解压 tar.xz 用）
RUN apt-get update && apt-get install -y curl xz-utils

# 安装 Git
RUN apt-get update && apt-get install -y git



# 安装 Node.js v20.x LTS 版本（无需 apt 源）
ENV NODE_VERSION=20.12.2

RUN curl -fsSL https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-arm64.tar.xz -o node.tar.xz && \
    mkdir -p /usr/local/lib/nodejs && \
    tar -xJf node.tar.xz -C /usr/local/lib/nodejs && \
    rm node.tar.xz && \
    ln -sf /usr/local/lib/nodejs/node-v$NODE_VERSION-linux-arm64/bin/node /usr/bin/node && \
    ln -sf /usr/local/lib/nodejs/node-v$NODE_VERSION-linux-arm64/bin/npm /usr/bin/npm && \
    ln -sf /usr/local/lib/nodejs/node-v$NODE_VERSION-linux-arm64/bin/npx /usr/bin/npx && \
    node -v && npm -v


WORKDIR /app

# Install Tavily + LangChain tool support
RUN pip install -U langchain-community tavily-python
#INSTALL PUBMED MCP SERVER

# 安装 PubMed MCP Server 到虚拟环境
RUN pip install mcp-simple-pubmed


COPY . /app

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

EXPOSE 8000

# Run the app
CMD ["uv", "run", "python", "server.py", "--host", "0.0.0.0", "--port", "8000"]
