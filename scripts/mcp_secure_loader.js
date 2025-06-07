#!/usr/bin/env node
/**
 * MIRRALISM Secure MCP Configuration Loader
 * 
 * Purpose: Load MCP configuration with secure environment variable handling
 * Security: Prevents API key exposure in configuration files
 * 
 * Created: 2025-06-07
 * Version: 1.0.0
 */

const fs = require('fs');
const path = require('path');
const { config } = require('dotenv');

// Load environment variables from .env.local
const envPath = path.join(__dirname, '..', '.env.local');
if (fs.existsSync(envPath)) {
    config({ path: envPath });
    console.log('✅ Environment variables loaded securely');
} else {
    console.error('🚨 .env.local not found! API keys not loaded.');
    process.exit(1);
}

// Secure MCP configuration with environment variables
const mcpConfig = {
    mcpServers: {
        "task-master-ai": {
            command: "node",
            args: [
                process.env.MCP_TASK_MASTER_PATH || "/usr/local/lib/node_modules/task-master-ai/mcp-server/server.js"
            ],
            env: {
                ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
                PERPLEXITY_API_KEY: process.env.PERPLEXITY_API_KEY || "",
                OPENAI_API_KEY: process.env.OPENAI_API_KEY || "",
                GOOGLE_API_KEY: process.env.GOOGLE_API_KEY || "",
                XAI_API_KEY: process.env.XAI_API_KEY || "",
                OPENROUTER_API_KEY: process.env.OPENROUTER_API_KEY || "",
                MISTRAL_API_KEY: process.env.MISTRAL_API_KEY || "",
                AZURE_OPENAI_API_KEY: process.env.AZURE_OPENAI_API_KEY || "",
                OLLAMA_API_KEY: process.env.OLLAMA_API_KEY || ""
            }
        },
        
        "filesystem": {
            command: "npx",
            args: [
                "@modelcontextprotocol/server-filesystem",
                ...process.env.MCP_FILESYSTEM_PATHS.split(',')
            ]
        },
        
        "notion": {
            command: "npx",
            args: ["@notionhq/notion-mcp-server"],
            env: {
                NOTION_API_KEY: process.env.NOTION_API_KEY || ""
            }
        }
    }
};

// Write secure configuration
const outputPath = path.join(__dirname, '..', '.cursor', 'mcp.json');
fs.writeFileSync(outputPath, JSON.stringify(mcpConfig, null, 4));

console.log('✅ Secure MCP configuration generated');
console.log('📁 Output:', outputPath);
console.log('🔒 API keys loaded from environment variables');
console.log('');
console.log('🚨 Security Notice:');
console.log('   - Never commit mcp.json with API keys');
console.log('   - Always use this loader for MCP configuration');
console.log('   - Keep .env.local secure and out of version control');