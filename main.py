import streamlit as st
from groq import Groq

# Initialize the Groq client with a placeholder for the API key
client = None

# Initialize session state variables for shared memory and dynamic weights
if 'shared_memory' not in st.session_state:
    st.session_state.shared_memory = []

if 'dynamic_weights' not in st.session_state:
    st.session_state.dynamic_weights = {}

# Function to manage shared memory size
def manage_memory(new_entry, max_size=20):
    if len(st.session_state.shared_memory) >= max_size:
        st.session_state.shared_memory.pop(0)
    st.session_state.shared_memory.append(new_entry)

# Function to get a weighted context from shared memory
def get_weighted_context():
    sorted_memory = sorted(st.session_state.shared_memory, key=lambda x: sum(st.session_state.dynamic_weights.get(word, 0) for word in x.split()), reverse=True)
    return " ".join(sorted_memory[-10:])

# Function to interact with the AI using Groq API
def interact_with_groq(messages, max_tokens=500):
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
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

# Streamlit App
st.title("Interactive AI Conversation with Memory Management")

st.sidebar.header("Step 1: API Key")
api_key = st.sidebar.text_input("Enter your Groq API key:", type="password")

if api_key:
    client = Groq(api_key=api_key)
    st.sidebar.success("API key set successfully!")

    # Step 2: Add a thought to shared memory
    st.sidebar.header("Step 2: Add Thought to Shared Memory")
    new_thought = st.sidebar.text_area("Enter your thought:")

    if st.sidebar.button("Add Thought"):
        if new_thought:
            manage_memory(new_thought)
            st.sidebar.success("Thought added to shared memory.")
        else:
            st.sidebar.error("Please enter a thought before adding.")

    if st.session_state.shared_memory:
        st.write("### Shared Memory:")
        st.write(st.session_state.shared_memory)

        # Step 3: Start a conversation between AI agents
        st.sidebar.header("Step 3: Conversation Settings")
        iterations = st.sidebar.number_input("Enter the number of conversation turns:", min_value=1, max_value=100, value=5)

        if st.sidebar.button("Start Conversation"):
            agent1_output = ""
            agent2_output = ""
            conversation_history = ""

            for i in range(iterations):
                st.write(f"## Conversation Turn {i+1}")

                context = get_weighted_context()

                # Agent 1's turn
                if agent2_output:
                    custom_prompt = (
                        f"Reflect on the previously discussed topics and Agent 2's response. "
                        f"Compose an insightful short response that delves deeper into the subject matter, offering new perspectives or questions for further investigation. "
                        f"Consider the following context from shared memory:\n\n{context}\n\n"
                        f"Agent 2's previous response: {agent2_output}\n\n"
                        f"Your response should be thought-provoking, build upon the previous discussion, introduce novel ideas, and encourage critical thinking. "
                        f"Keep it concise yet profound."
                    )
                    messages = [{"role": "system", "content": custom_prompt}]
                else:
                    messages = [{"role": "system", "content": f"Consider the following context from shared memory:\n\n{context}\n\nStart a conversation by introducing a thought-provoking topic or question."}]

                agent1_output = interact_with_groq(messages, max_tokens=550)
                if agent1_output:
                    st.write("### Agent 1:")
                    st.write(agent1_output)
                    conversation_history += f"Agent 1: {agent1_output}\n\n"
                    manage_memory(agent1_output)
                    for word in agent1_output.split():
                        st.session_state.dynamic_weights[word] = st.session_state.dynamic_weights.get(word, 0) + 1
                else:
                    st.error("No response received from Agent 1.")
                    break

                # Agent 2's turn
                context = get_weighted_context()
                custom_prompt = (
                    f"Reflect on Agent 1's response and the previously discussed topics. "
                    f"Compose a thoughtful short response that builds upon the conversation, offering new insights or posing intriguing questions. "
                    f"Consider the following context from shared memory:\n\n{context}\n\n"
                    f"Agent 1's previous response: {agent1_output}\n\n"
                    f"Your response should enrich the conversation, challenge assumptions, and stimulate further dialogue. "
                    f"Keep it concise yet impactful."
                )
                messages = [{"role": "system", "content": custom_prompt}]

                agent2_output = interact_with_groq(messages, max_tokens=550)
                if agent2_output:
                    st.write("### Agent 2:")
                    st.write(agent2_output)
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
