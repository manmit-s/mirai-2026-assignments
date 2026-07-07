import streamlit as st

#Task-1
st.title("Echo Chamber 9000")
st.write("Welcome agent. Enter your credentials and message to transmit into the void.")

#Task-2
user_name = st.text_input("Enter your Name: ")
user_message = st.text_input("Enter your Message: ")

#Task-3
if st.button("Transmit"):
    #Task-4: conditional routing
    if not user_name:
        st.error("Name is required!")
    elif not user_message:
        st.warning("Please provide a message to transmit.")
    else:
        #Task-5
        st.success(f"Transmission successful! Greetings, {user_name}. We received your message : {user_message}")

        #Token calculator
        tokens_count = len(user_message)/4 # as 1 token equivalent to 4 characters
        st.info(f"System check: Your message will consume: {tokens_count} tokens approximately from the context window.")