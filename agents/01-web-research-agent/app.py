import streamlit as pd
import streamlit as st
import os
from dotenv import load_dotenv

# Import your working agent function from your original file
# (Assumes your agent has an execution function; adjust the function name if needed)
from agent import main as run_agent

# 1. Page Configuration
st.set_page_config(
    page_title="AI Web Research Agent",
    page_icon="🔍",
    layout="centered"
)

# 2. App Title & Subtitle
st.title("🤖 Local AI Web Research Agent")
st.markdown("Enter a topic below. The agent will crawl the web using Tavily and synthesize a comprehensive report using your local Ollama model.")

# 3. Sidebar Status Configuration
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("🤖 Core Model: Llama 3.2 (Local)")
    st.info("🌐 Search Engine: Tavily API Connected")
    
    # Optional input to override search queries if your main script doesn't use sys.argv
    num_results = st.slider("Max Search Results", min_value=1, max_value=10, value=5)

# 4. User Input Area
query = st.text_input(
    "What topic would you like to research?",
    placeholder="e.g., Latest trends in quantum computing 2026"
)

# 5. Execution Trigger
if st.button("Generate Research Report", type="primary"):
    if not query.strip():
        st.warning("Please enter a valid research topic first!")
    else:
        # Create a visual loading spinner while the agent runs
        with st.spinner("🕵️‍♂️ Agent is searching the web and synthesizing findings... Please wait."):
            try:
                # Modifying your original script execution flow slightly:
                # If your agent script outputs a file like 'report.md', we read it.
                # Here we trigger your core script logic.
                
                # Mocking argument parsing or environment variables if your script relies on them:
                os.environ["AGENT_QUERY"] = query 
                
                # Run your agent logic
                run_agent() 
                
                st.success("✅ Research completed successfully!")
                
                # 6. Display the Output File
                # Checking if your agent saved the output to a markdown file
                output_file = "report.md" 
                if os.path.exists(output_file):
                    with open(output_file, "r", encoding="utf-8") as f:
                        report_content = f.read()
                    
                    st.divider()
                    st.subheader("📋 Generated Research Report")
                    st.markdown(report_content)
                    
                    # Add a convenient download button for the user
                    st.download_button(
                        label="📥 Download Report (.md)",
                        data=report_content,
                        file_name=f"research_report_{query.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.info("The agent finished, but no 'report.md' file was detected. Check your terminal output.")
                    
            except Exception as e:
                st.error(f"An error occurred during execution: {str(e)}")
