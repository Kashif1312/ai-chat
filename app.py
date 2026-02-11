import gradio as gr
from groq import Groq
import asyncio
import edge_tts
import nest_asyncio

nest_asyncio.apply()

# 🔑 PUT YOUR GROQ KEY
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# 🔥 SYSTEM PROMPTS PER MODE
MODE_PROMPTS = {
    "Chat": "You are a helpful AI assistant. Give clear and intelligent answers.",
    "Image": "Return ONLY a detailed AI image generation prompt with scene, lighting, style, camera angle.",
    "Voice": "Convert text into natural speech-ready narration."
}

# 🤖 GROQ RESPONSE
def ai_response(user_text, mode):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":MODE_PROMPTS[mode]},
            {"role":"user","content":user_text}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# 🔊 TEXT TO SPEECH
async def generate_voice(text):
    file="voice.mp3"
    communicate=edge_tts.Communicate(text,"en-US-AriaNeural")
    await communicate.save(file)
    return file

# 🚀 MAIN CHAT FUNCTION
def chatbot(user_message, history, mode):

    ai_text = ai_response(user_message, mode)

    audio=None

    if mode=="Voice":
        audio=asyncio.run(generate_voice(ai_text))

    history.append((user_message, ai_text))

    return history, "", audio

# 🎨 CHATBOT UI
with gr.Blocks(title="🔥 SUPER AI CHATBOT") as demo:

    gr.Markdown("# 🔥 SUPER AI MULTI MODE CHATBOT")

    # 🔝 Mode Buttons
    mode = gr.Radio(
        ["Chat","Image","Voice"],
        value="Chat",
        label="Select Mode"
    )

    chatbot_ui = gr.Chatbot(height=400)

    msg = gr.Textbox(placeholder="Type your message...")

    audio_output = gr.Audio(label="Voice Output")

    send = gr.Button("🚀 Send")

    send.click(
        chatbot,
        inputs=[msg, chatbot_ui, mode],
        outputs=[chatbot_ui, msg, audio_output]
    )

demo.launch(share=True)
