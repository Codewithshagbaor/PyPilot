import streamlit as st
import json
from anthropic import Anthropic

# Initialize ClaudeAI class with Anthropic package
class ClaudeAI:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
        self.retry_attempts = 3

    def send_message(self, message, conversation_id=None):
        """Send a message to the Claude API and receive a response."""
        for attempt in range(1, self.retry_attempts + 1):
            try:
                response = self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": message}]
                )
                return {
                    "reply": response.content[0].text,
                    "conversation_id": None
                }
            except Exception as e:
                print(f"Error communicating with Claude API on attempt {attempt}: {e}")
                if attempt == self.retry_attempts:
                    break
        return None

    def manage_context(self, project_name, new_message):
        context = self.load_context(project_name)
        messages = context.get("messages", [])

        if len(messages) > 20:
            messages = messages[-20:]
        # Prepare full conversation history for API call
        conversation_history = [
            {"role": msg["role"], "content": msg["message"]} 
            for msg in messages
        ]
        conversation_history.append({"role": "user", "content": new_message})

        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,  # Increased token limit
            messages=conversation_history
        )
        
        ai_reply = response.content[0].text
        messages.append({"role": "user", "message": new_message})
        messages.append({"role": "assistant", "message": ai_reply})
        
        context.update({"messages": messages})
        self.save_context(project_name, context)

        return ai_reply

    def load_context(self, project_name):
        """Load conversation context from a JSON file."""
        try:
            with open(f"{project_name}.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"messages": []}
        except Exception as e:
            print(f"Error loading context for {project_name}: {e}")
            return {"messages": []}

    def save_context(self, project_name, context):
        """Save conversation context to a JSON file."""
        try:
            with open(f"{project_name}.json", "w") as file:
                json.dump(context, file)
        except Exception as e:
            print(f"Error saving context for {project_name}: {e}")

# Streamlit App Configuration
def main():
    # API Key Configuration
    API_KEY = st.sidebar.text_input("Anthropic API Key", type="password")
    
    if not API_KEY:
        st.warning("Please enter your Anthropic API key.")
        return

    # Initialize ClaudeAI with API key
    claude_ai = ClaudeAI(API_KEY)

    # Session State Initialization
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "is_processing" not in st.session_state:
        st.session_state["is_processing"] = False

    # Sidebar for Project Management
    st.sidebar.title("Project Management")
    project_name = st.sidebar.text_input("Project Name", "default_project")

    # Load Project Button
    if st.sidebar.button("Load Project"):
        context = claude_ai.load_context(project_name)
        st.session_state["messages"] = [
            {"role": msg["role"], "content": msg["message"]} 
            for msg in context.get("messages", [])
        ]

    # Main Chat Interface
    st.title("Personal Coding AI")

    # Display Messages
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input("Your message", disabled=st.session_state["is_processing"]):
        # Add user message to session state
        st.session_state["messages"].append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Processing indicator
        st.session_state["is_processing"] = True
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = claude_ai.manage_context(project_name, prompt)
                st.markdown(response)

        # Add AI response to session state
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.session_state["is_processing"] = False
        st.rerun()  # Updated from st.experimental_rerun()

if __name__ == "__main__":
    main()