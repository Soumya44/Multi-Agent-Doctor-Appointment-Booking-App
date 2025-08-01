import streamlit as st
import requests
import uuid
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Hospital Appointment Booking",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Hospital Appointment Booking Chat")

# Agent dictionary for dialog state mapping
agent_dict = {
    'get_info': 'information_agent',
    'appointment_info': 'appointment_agent',
    'primary_assistant': 'supervisor_agent'
}

def generate_uuid() -> str:
    """Generate a unique UUID for session management"""
    return str(uuid.uuid4())

def make_api_call(prompt: str) -> dict:
    """Calls the API and returns the response as a dictionary."""
    # Get backend URL from environment variable, fallback to localhost for development
    BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')
    API_URL = f"{BACKEND_URL}/generate-stream"
    thread_id = st.session_state.thread_id

    try:
        response = requests.post(
            API_URL, 
            json={"query": prompt}, 
            headers={"X-THREAD-ID": thread_id}, 
            timeout=60.0
        )
        response.raise_for_status()  # Raise an error for HTTP errors
        return response.json()  # Parse response JSON
    except requests.exceptions.HTTPError as e:
        st.error(f"API returned an error: {e.response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to the server at {BACKEND_URL}. Please make sure the FastAPI server is running.")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
    return {"answer": "Error retrieving response"}  # Fallback response

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_uuid()

if "has_interacted" not in st.session_state:
    st.session_state.has_interacted = False

# Sidebar for session management
with st.sidebar:
    st.header("Session Information")
    
    if st.session_state.thread_id:
        st.info(f"Session ID: {st.session_state.thread_id[:8]}...")
    
    if st.button("🔄 Start New Session"):
        st.session_state.thread_id = generate_uuid()
        st.session_state.messages = []
        st.session_state.has_interacted = False
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about appointments, check availability, or book/cancel appointments..."):
    # Display user input
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call API and display response
    with st.chat_message("assistant"):
        response_data = make_api_call(prompt)  # Get API response
        dialog_state = response_data.get('dialog_state')
        if not dialog_state:
            dialog_state = 'primary_assistant'
        answer = response_data.get("answer", "No response from API")
        
        # Display agent type
        agent_name = agent_dict.get(dialog_state, 'supervisor_agent')
        st.markdown(f'**:red[{agent_name}]**')
        
        # Display answer
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        # Mark as interacted after first response
        st.session_state.has_interacted = True

# Show footer only if there hasn't been any interaction yet
if not st.session_state.has_interacted:
    st.markdown("---")
    st.markdown("""
### How to use:
1. **Ask questions** directly in the chat, such as:
   - "Check availability for Dr. John Doe on 01-08-2025"
   - "Book an appointment with a general dentist"
   - "What slots are available for orthodontist on 05-08-2025?"
2. **Follow the prompts** to provide any missing information like patient ID when booking

### Available Services:
- 🔍 Check doctor availability
- 📅 Book appointments  
- ❌ Cancel appointments
- 🔄 Reschedule appointments
- **Fetch appointments details (Not implemented yet)** ❌
""")