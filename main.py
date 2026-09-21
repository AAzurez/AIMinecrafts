from fastmcp import FastMCP
from javascript import require, On
from tools.chat import chat
from tools.attack import attackEntity
from tools.destroy import destroy
from dotenv import load_dotenv
import os

load_dotenv()

mineflayer = require('mineflayer')

import anthropic 

client = anthropic.Anthropic(api_key = os.getenv("API_KEY"))

mcp = FastMCP("Server")

BOT_USERNAME = 'Jerry'

bot = mineflayer.createBot({
    'host': '127.0.0.1',
    'port': 25565,
    'username': BOT_USERNAME
    })

@mcp.tool()
def attack_tool():
    attackEntity(bot)

@mcp.tool()
def chat_tool(sender, message):
    print(chat(bot, sender, message))

@mcp.tool()
def destroy_tool():
    #Find the block that was suggest/found
    print(destroy(bot, 'oak_leaves'))

tools = [
    {
        "name": "attack",
        "description": "Attack the nearest entity",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "chat",
        "description": "Send a message in the chat",
        "input_schema": {
            "type": "object",
            "properties": {
                "sender": {"type": "string"},
                "message": {"type": "string"}
            },
            "required" : ["message"]
        }
    },
    {
        "name": "destroy",
        "description": "Destroy the nearest block",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

@On(bot, "login")
def login(*args):
    bot.chat("Hi everyone!")

@On(bot, 'chat')
def handleMsg(sender, message, *args):
    if sender != BOT_USERNAME:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            messages=[
                {"role": "user", 
                 
                "content": f"Based on the {message}, decide which tool to use and use it. USE A SHORT RESPONSE"

                },
            ],
            max_tokens=200,
            tools = tools,
        )

        for block in response.content:
            print(block)
            if block.type == "tool_use" and block.name == "attack":
                attack_tool()
            elif block.type == "tool_use" and block.name == "chat":
                chat_tool(sender, block.input.get("message", "..."))
            elif block.type == "tool_use" and block.name == "destroy":
                destroy_tool()

if __name__ == "__main__":
    mcp.run()