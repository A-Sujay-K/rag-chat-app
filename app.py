import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Loading...").send()


@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content=f"Echo: {message.content}").send()
