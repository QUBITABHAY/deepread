import gradio as gr
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8080/api")

def chat_interface(message, history):
    text = message.get("text", "").strip()
    files = message.get("files", [])
    
    upload_status = ""
    
    if files:
        for file_path in files:
            upload_endpoint = f"{API_URL}/upload"
            try:
                fname = os.path.basename(file_path)
                with open(file_path, "rb") as f:
                    req_files = {"file": (fname, f)}
                    resp = requests.post(upload_endpoint, files=req_files)
                    
                if resp.status_code == 200:
                    upload_status += f"**{fname}** successfully processed.\n\n"
                else:
                    return f"Error uploading {fname}: {resp.text}"
            except Exception as e:
                return f"Request failed on upload: {str(e)}"

    if text:
        query_endpoint = f"{API_URL}/query"
        try:
            payload = {"question": text}
            response = requests.post(query_endpoint, json=payload)
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                return upload_status + answer
            else:
                return upload_status + f"Error: {response.text}"
        except Exception as e:
            return upload_status + f"Request failed: {str(e)}"
            
    if upload_status and not text:
        return upload_status + "You can now ask questions about the document(s)."
        
    return "Please ask a question or attach a document."

with gr.Blocks(title="DeepRead AI") as app:
    gr.Markdown("<h1 style='text-align: center; margin-top: 20px;'>📚 DeepRead AI</h1>")
    gr.Markdown("<p style='text-align: center;'>Type a message or attach a PDF to ask questions about it.</p>")
    
    gr.ChatInterface(
        fn=chat_interface,
        multimodal=True,
        chatbot=gr.Chatbot(height=650, show_label=False),
        textbox=gr.MultimodalTextbox(placeholder="Ask a question or attach a PDF...", container=False, scale=7),
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        share=False,
        theme=gr.themes.Soft(primary_hue="blue"),
    )
