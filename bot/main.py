from fastmcp import FastMCP
from javascript import require, On
from bot.tools.attack import attackEntity
from bot.tools.destroy import destroy
from dotenv import load_dotenv
import os
import anthropic 

#Client Things
load_dotenv()
client = anthropic.Anthropic(api_key = os.getenv("API_KEY"))


#Bot Setup
BOT_USERNAME = 'Jerry'
mineflayer = require('mineflayer')
bot = mineflayer.createBot({
    'host': '127.0.0.1',
    'port': 25565,
    'username': BOT_USERNAME
    })

#MCP Stuff
mcp = FastMCP("Server")

#MCP Tools
@mcp.tool()
def attack_tool():
    attackEntity(bot)
@mcp.tool()
def destroy_tool():
    #Find the block that was suggest/found similarity word in dict
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
        "name": "destroy",
        "description": "Destroy the nearest block",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

#Functions
#Login thing
@On(bot, "login")
def login(*args):
    bot.chat("Hi everyone!")

#Deciding what to do
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
            if block.type == "tool_use" and block.name == "attack":
                attack_tool()
            elif block.type == "tool_use" and block.name == "chat":
                bot.chat(message)
            elif block.type == "tool_use" and block.name == "destroy":
                destroy_tool()

if __name__ == "__main__":
    mcp.run()