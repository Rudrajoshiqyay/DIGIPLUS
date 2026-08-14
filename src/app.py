import streamlit as st
import pandas as pd
import os
import sys

# Ensure src modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.llm_agent import generate_playbook
from src.storage import save_new_incident, save_resolution
from src.rule_engine import apply_rules
from src.triage_agent import chat_with_triage_agent

st.set_page_config(page_title="Digiplus AI Copilot", page_icon="🤖", layout="wide")

st.title("🤖 Digiplus IT Support AI Copilot")
st.markdown("This end-to-end demo shows the lifecycle of an IT ticket from submission to AI resolution.")

# Load mock tickets for the dropdown
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "tickets.csv")
    try:
        df = pd.read_csv(csv_path)
        return df.head(10) # Load 10 for the demo
    except FileNotFoundError:
        return pd.DataFrame(columns=["ticket_id", "summary", "description"])

df = load_data()

# Initialize session state for our custom ticket
if 'custom_ticket' not in st.session_state:
    st.session_state.custom_ticket = None

# Create the Three Tabs
tab1, tab2, tab3 = st.tabs(["🧑‍💼 Employee Portal", "👨‍💻 Engineer Dashboard", "📊 Analytics"])

with tab1:
    st.header("Employee Portal (Triage Agent)")
    st.markdown("Chat with our AI Assistant to try and resolve your issue immediately!")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I am the Digiplus IT Triage Bot. What issue are you facing today?"}]

    # Display chat messages from history on app rerun
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # React to user input
    if prompt := st.chat_input("Describe your issue..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Agent is typing..."):
                response = chat_with_triage_agent(st.session_state.messages)
            
            if "[ESCALATE]" in response:
                st.markdown("I couldn't solve this for you, but I have drafted a formal ticket and escalated it to our Human Support Engineers!")
                
                # Parse summary and description
                lines = response.split('\n')
                summary = "Escalated Ticket"
                desc = "See chat history."
                for line in lines:
                    if line.startswith("Summary:"): summary = line.replace("Summary:", "").strip()
                    if line.startswith("Description:"): desc = line.replace("Description:", "").strip()
                
                # Save to disk
                save_new_incident(summary, desc)
                st.session_state.custom_ticket = {"summary": summary, "description": desc}
                st.success("Ticket Submitted Successfully! Switch to the 'Engineer Dashboard' tab.")
                
            else:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.header("Incoming Tickets")
    
    # Let the user choose between the custom ticket or the pre-loaded CSV tickets
    data_source = st.radio("Select Data Source:", ["Live Submitted Ticket", "Historical Tickets (CSV Database)"])
    
    if data_source == "Live Submitted Ticket":
        if st.session_state.custom_ticket:
            st.info("🚨 New Ticket Received from Employee Portal!")
            selected_summary = st.session_state.custom_ticket["summary"]
            selected_description = st.session_state.custom_ticket["description"]
            
            st.subheader(f"Summary: {selected_summary}")
            st.write(f"**Description:** {selected_description}")
            
        else:
            st.warning("No live tickets submitted yet. Go to the 'Employee Portal' tab to submit one!")
            selected_summary = None
            
    else:
        if df.empty:
            st.error("Data not found. Please ensure data_loader.py has been run.")
            selected_summary = None
        else:
            ticket_options = df.apply(lambda row: f"Ticket #{row['ticket_id']}: {row['summary']}", axis=1).tolist()
            selected_option = st.selectbox("Select a historical ticket:", ticket_options)
            
            if selected_option:
                ticket_id = int(selected_option.split(":")[0].replace("Ticket #", ""))
                ticket_row = df[df['ticket_id'] == ticket_id].iloc[0]
                
                selected_summary = ticket_row['summary']
                selected_description = ticket_row['description']
                
                st.subheader(f"Summary: {selected_summary}")
                st.write(f"**Description:** {selected_description}")
            else:
                selected_summary = None

    # The AI Copilot Action block
    if selected_summary:
        if 'current_playbook' not in st.session_state:
            st.session_state.current_playbook = None
        if 'current_ticket_summary' not in st.session_state or st.session_state.current_ticket_summary != selected_summary:
            st.session_state.current_playbook = None
            st.session_state.current_ticket_summary = selected_summary

        if st.button("Generate Investigation Playbook", type="primary"):
            with st.spinner("Analyzing rules, searching vector store, and prompting Llama..."):
                try:
                    playbook = generate_playbook(selected_summary, selected_description)
                    st.session_state.current_playbook = playbook
                except Exception as e:
                    st.error(f"An error occurred: {e}. Please check your Groq API key.")

        if st.session_state.current_playbook:
            st.success("Playbook Generated Successfully!")
            st.markdown(st.session_state.current_playbook)
            
            # --- FEATURE: Download Button ---
            st.download_button(
                label="💾 Download Playbook (.md)",
                data=st.session_state.current_playbook,
                file_name=f"playbook_{selected_summary.replace(' ', '_').lower()}.md",
                mime="text/markdown"
            )
            
            # --- FEATURE: AI Reasoning Trace ---
            with st.expander("🔍 View AI Reasoning & Logs"):
                st.write("**Rule Engine Processing:**")
                tags = apply_rules(f"{selected_summary} {selected_description}")
                if tags:
                    for tag in tags:
                        st.write(f"- Matched Tag: `{tag}`")
                else:
                    st.write("- No specific rules matched. Falling back to semantic search.")
                
                st.write("**Vector Store:**")
                st.write("- Query sent to ChromaDB to retrieve Similar Past Incidents.")
                
                st.write("**LLM Generation:**")
                st.write("- Prompt injected with Knowledge Base policies and Similar Incidents.")
                st.write("- Llama 3 generation complete.")
            
            st.divider()
            st.markdown("### Action")
            if st.button("Mark as Resolved & Save to Learning History"):
                # Persist the resolution to disk
                save_resolution(selected_summary, selected_description, st.session_state.current_playbook)
                
                # Clear state
                if data_source == "Live Submitted Ticket":
                    st.session_state.custom_ticket = None
                st.session_state.current_playbook = None
                
                st.balloons()
                st.toast("Resolution saved permanently to the Learning History database!", icon="✅")
                st.rerun()

with tab3:
    st.header("📊 IT Support Analytics")
    st.markdown("Live analytics of our ticket resolution and Learning History.")
    
    # --- FEATURE: KPI Metrics Dashboard ---
    col1, col2, col3 = st.columns(3)
    
    resolved_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "resolved_tickets.csv")
    submitted_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "submitted_tickets.csv")
    
    total_submitted = 0
    if os.path.exists(submitted_path):
        total_submitted = len(pd.read_csv(submitted_path))
        
    total_resolved = 0
    duplicate_count = 0
    cache_savings = 0
    
    if os.path.exists(resolved_path):
        resolved_df = pd.read_csv(resolved_path)
        total_resolved = len(resolved_df)
        
        # Calculate cache hits based on exact duplicate summaries in the resolution history
        duplicate_count = resolved_df.duplicated(subset=['summary']).sum()
        cache_savings = duplicate_count * 1500 # Assume ~1500 tokens saved per cached playbook
    
    col1.metric("Live Tickets Submitted", total_submitted)
    col2.metric("Total AI Resolutions", total_resolved)
    col3.metric("Tokens Saved via Cache", cache_savings, f"{duplicate_count} Cache Hits")
    
    st.divider()
    
    if total_resolved > 0:
        st.markdown("### Recent Resolutions")
        st.dataframe(resolved_df[['timestamp', 'summary', 'status']])
    else:
        st.info("No tickets have been resolved yet. Use the Engineer Dashboard to resolve tickets and build the Learning History!")
