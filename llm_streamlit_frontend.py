import streamlit as st

from openai import OpenAI

client = OpenAI(
    api_key=OPENAI_KEY)


def sidebar_config():
    st.sidebar.title("Configuration")

    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
    top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9)
    #top_k = st.sidebar.slider("Top K", 0, 100, 50)

    return temperature, top_p


def main():
    st.title("OpenAI Chat and Instruct Modes")

    # Select mode
    mode = st.selectbox("Choose Mode", ["Chat", "Instruct"])

    # Get configuration values
    temperature, top_p = sidebar_config()

    # Define input fields
    if mode == "Chat":
        user_input = st.text_input("You: ", "")
        chat_history = st.empty()
    else:
        instructions = st.text_area("Instructions: ", "")
        documents = st.text_area("Documents: ", "")

    # Process user input
    if st.button("Submit"):
        if mode == "Chat":
            chat_response = get_chat_response(user_input, temperature, top_p)
            chat_history.markdown(f"**You:** {user_input}\n\n**Assistant:** {chat_response}")
        else:
            instruct_response = get_instruct_response(instructions, documents, temperature, top_p)
            st.markdown(instruct_response)


def get_chat_response(user_input, temperature, top_p):

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are helpful assistant"},
            {"role": "user", "content": user_input}
        ],
        temperature=temperature,
        top_p=top_p
        #stream=True
    )

    # result = ""
    # for message in completion:
    #     result += message.choices[0].message.content
    # return result

    result = completion.choices[0].message.content

    return result


def get_instruct_response(instructions, documents, temperature, top_p):
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": documents}
        ],
        temperature=temperature,
        top_p=top_p
        #stream=True  # Streaming output
    )

    result = completion.choices[0].message.content

    return result


if __name__ == "__main__":
    main()
