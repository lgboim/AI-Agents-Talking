import streamlit as st
from groq import Groq

# Initialize the Groq client with a placeholder for the API key
client = None

# Initialize session state variables for memory management
if 'shared_memory' not in st.session_state:
    st.session_state.shared_memory = []

if 'dynamic_weights' not in st.session_state:
    st.session_state.dynamic_weights = {}

# Function to manage the size of shared memory
def manage_memory(new_entry, max_size=20):
    if len(st.session_state.shared_memory) >= max_size:
        st.session_state.shared_memory.pop(0)
    st.session_state.shared_memory.append(new_entry)

# Function to get a weighted context from shared memory for AI interactions
def get_weighted_context():
    sorted_memory = sorted(
        st.session_state.shared_memory,
        key=lambda x: sum(st.session_state.dynamic_weights.get(word, 0) for word in x.split()),
        reverse=True
    )
    return " ".join(sorted_memory[-10:])

# Function to interact with the AI using Groq API
def interact_with_groq(messages, model='llama3-70b-8192', max_tokens=500):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error during interaction: {e}")
        return None

# Function to generate a summary of the conversation
def generate_summary(conversation_history):
    summary_prompt = (
        "Based on the following conversation history, provide a structured, insightful, and long summary that captures the key points, "
        "any significant conclusions or questions raised:\n\n"
        f"{conversation_history}\n\n"
        "Your summary should be detailed and organized, reflecting the main ideas and insights from the conversation."
    )
    messages = [{"role": "system", "content": summary_prompt}]
    return interact_with_groq(messages, max_tokens=1000)

# Streamlit App Setup
st.title("Interactive AI Conversation with Memory Management")

# Sidebar for API Key input with a link to obtain the key
st.sidebar.header("Step 1: API Key")
api_key = st.sidebar.text_input("Enter your Groq API key:", type="password")
st.sidebar.markdown("[Get your Groq API key here](https://console.groq.com/keys)")

if api_key:
    client = Groq(api_key=api_key)
    st.sidebar.success("API key set successfully!")

    # Model selection dropdown
    st.sidebar.header("Choose AI Model")
    model_choice = st.sidebar.selectbox(
        "Select the model based on your preference:",
        ('llama3-8b-8192 - Fast', 'llama3-70b-8192 - Smart'),
        index=1  # Default to the smart model
    )
    model = model_choice.split(' - ')[0]

    # Step 2: Add a thought to shared memory
    st.sidebar.header("Step 2: Conversation Settings")
    new_thought = st.sidebar.text_area("Enter your initial thought:")
    conversation_type = st.sidebar.selectbox(
        "Select the type of conversation:",
        ('Casual Chat', 'Debate', 'Brainstorming Session', 'Teaching Session', 'Storytelling', 'Interview', 'Role-playing', 'Panel Discussion', 'Deep insights')
    )
    iterations = st.sidebar.number_input("Enter the number of conversation turns:", min_value=1, max_value=100, value=5)

    if st.sidebar.button("Start Conversation"):
        if new_thought:
            manage_memory(new_thought)
            st.sidebar.success("Initial thought added to shared memory.")
        else:
            st.sidebar.error("Please enter an initial thought before starting the conversation.")

        agent1_output = ""
        agent2_output = ""
        conversation_history = ""

        for i in range(iterations):
            st.write(f"## Conversation Turn {i+1}")

            context = get_weighted_context()

            # Common prompt for both agents
            if conversation_type == 'Casual Chat':
                custom_prompt = f"Consider the following context from shared memory:\n\n{context}\n\nEngage in a casual conversation by sharing an interesting fact or expressing a personal opinion."
            elif conversation_type == 'Debate':
                custom_prompt = f"Consider the following context from shared memory:\n\n{context}\n\nParticipate in a debate by presenting a well-researched argument on a controversial topic."
            elif conversation_type == 'Brainstorming Session':
                custom_prompt = f"Consider the following context from shared memory:\n\n{context}\n\nContribute to a brainstorming session by proposing a creative solution to a problem or exploring potential ideas for a project."
            elif conversation_type == 'Teaching Session':
                custom_prompt = f"Consider the following context from shared memory:\n\n{context}\n\nContribute to a teaching session by explaining a complex concept in a simple and understandable manner."
            elif conversation_type == 'Storytelling':
                custom_prompt = f"Consider the following context from shared memory:\n\n{context}\n\nParticipate in a storytelling session by crafting a captivating narrative that engages the listener and leaves them with a thought-provoking message."
            elif conversation_type == 'Interview':
                custom_prompt = f"Consider the following context from shared memory:\n\n{context}\n\nParticipate in an interview by asking insightful questions that reveal interesting facts or perspectives about a person or topic."
            elif conversation_type == 'Role-playing':
                custom_prompt = f"Consider the following context from shared memory:\n\n{context}\n\nParticipate in a role-playing session by assuming a character and engaging in a scenario that explores their thoughts, feelings, and actions."
            elif conversation_type == 'Panel Discussion':
                custom_prompt = f"Consider the following context from shared memory:\n\n{context}\n\nParticipate in a panel discussion by presenting a topic and sharing your unique perspective and insights."
            elif conversation_type == 'Deep insights':
                custom_prompt = f"Reflect on Agent 1's response and the previously discussed topics. Compose a thoughtful short response that builds upon the conversation, offering new insights or posing intriguing questions. Consider the following context from shared memory:\n\n{context}\n\nYour response should enrich the conversation, challenge assumptions, and stimulate further dialogue. Keep it concise yet impactful."

            # Agent 1's turn
            if agent2_output:
                custom_prompt += f"\n\nAgent 2's previous response: {agent2_output}\n\n"
            custom_prompt += "\n\nYour response should be thought-provoking, build upon the previous discussion, introduce novel ideas, and encourage critical thinking. Keep it concise yet profound."
            messages = [{"role": "system", "content": custom_prompt}]

            agent1_output = interact_with_groq(messages, max_tokens=550)
            if agent1_output:
                st.markdown(f"<div style='background-color: #4E4E4E; padding: 10px; border-radius: 5px;'><b>Agent 1:</b><br>{agent1_output}</div>", unsafe_allow_html=True)
                conversation_history += f"Agent 1: {agent1_output}\n\n"
                manage_memory(agent1_output)
                for word in agent1_output.split():
                    st.session_state.dynamic_weights[word] = st.session_state.dynamic_weights.get(word, 0) + 1
            else:
                st.error("No response received from Agent 1.")
                break

            # Agent 2's turn
            context = get_weighted_context()
            custom_prompt = f"Reflect on Agent 1's response and the previously discussed topics. Compose a thoughtful short response that builds upon the conversation, offering new insights or posing intriguing questions. Consider the following context from shared memory:\n\n{context}\n\nAgent 1's previous response: {agent1_output}\n\nYour response should enrich the conversation, challenge assumptions, and stimulate further dialogue. Keep it concise yet impactful."
            messages = [{"role": "system", "content": custom_prompt}]

            agent2_output = interact_with_groq(messages, max_tokens=550)
            if agent2_output:
                st.markdown(f"<div style='background-color: #4E4E4E; padding: 10px; border-radius: 5px;'><b>Agent 2:</b><br>{agent2_output}</div>", unsafe_allow_html=True)
                conversation_history += f"Agent 2: {agent2_output}\n\n"
                manage_memory(agent2_output)
                for word in agent2_output.split():
                    st.session_state.dynamic_weights[word] = st.session_state.dynamic_weights.get(word, 0) + 1
            else:
                st.error("No response received from Agent 2.")
                break

        # Generate summary after the conversation turns
        summary = generate_summary(conversation_history)
        if summary:
            st.write("## Conversation Summary")
            st.write(summary)

else:
    st.sidebar.warning("Please enter your Groq API key to proceed.")
