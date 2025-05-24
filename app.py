import gradio as gr
from chatbot import HiringAssistant

class GradioHiringAssistant:
    def __init__(self):
        self.assistant = HiringAssistant()

    def chat_interface(self, message, history):
        if not history:
            welcome_msg = self.assistant.get_welcome_message()
            history.append([None, welcome_msg])
            return history, ""

        if message:
            response = self.assistant.process_message(message)
            history.append([message, response])
            return history, ""

    def get_candidate_info_display(self):
        if not self.assistant.candidate_info:
            return "No information collected yet..."
        
        info_text = "**Candidate Information:**\n\n"
        for key, value in self.assistant.candidate_info.items():
            if not key.startswith('answer_'):
                display_key = key.replace('_', ' ').title()
                info_text += f"• **{display_key}:** {value}\n"
        return info_text

    def update_progress(self):
        progress = int(self.assistant.get_progress() * 100)
        return f'<div style="width: 100%; background-color: #f0f0f0; border-radius: 10px; margin: 10px 0;"><div style="width: {progress}%; background-color: #4CAF50; height: 20px; border-radius: 10px; text-align: center; line-height: 20px; color: white;">Progress: {progress}%</div></div>'

    def reset_conversation(self):
        self.assistant.reset_conversation()
        return [], "", "Conversation reset."

def create_gradio_interface():
    assistant_app = GradioHiringAssistant()
    
    with gr.Blocks(title="TalentScout AI Hiring Assistant") as demo:
        gr.Markdown("# 🤖 TalentScout AI Hiring Assistant\n### Powered by LLaMA - Technology Position Screening")
        
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="Chat with AI Assistant", height=500)
                
                with gr.Row():
                    msg = gr.Textbox(label="Your Response", placeholder="Type here...", lines=2, scale=4)
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("Clear Chat", variant="secondary")
                    reset_btn = gr.Button("Reset", variant="stop")
            
            with gr.Column(scale=1):
                gr.Markdown("### 📋 Candidate Information")
                candidate_display = gr.Markdown("Information will appear here...")
                progress_bar = gr.HTML(assistant_app.update_progress())
        
        def chat_fn(message, history):
            return assistant_app.chat_interface(message, history)
        
        def update_display():
            return assistant_app.get_candidate_info_display(), assistant_app.update_progress()
        
        submit_btn.click(chat_fn, inputs=[msg, chatbot], outputs=[chatbot, msg]).then(
            update_display, outputs=[candidate_display, progress_bar])
        
        msg.submit(chat_fn, inputs=[msg, chatbot], outputs=[chatbot, msg]).then(
            update_display, outputs=[candidate_display, progress_bar])
        
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg])
        reset_btn.click(assistant_app.reset_conversation, outputs=[chatbot, msg, candidate_display])
    
    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=True, debug=True)
