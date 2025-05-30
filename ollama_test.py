import ollama

def interactive_chat():
    print("Welcome to the interactive chat! Type 'exit' to quit. \n")
    client = ollama.Client()
    messages = [{"role": "system",
                 "content": "You are a helpful assistant. Respond to user queries in a friendly manner."}]
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting chat. Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        stream = client.chat(
            model="mistral:7b-instruct",
            messages=messages,
            stream=True
        )
        print("Bot is typing...")
        bot_response = ""
        for chunk in stream:
            # Debug: stampa la struttura del chunk
          #  print(chunk)

            content = ""
            # Prova tutte le possibilità note
            if isinstance(chunk, dict):
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                elif 'response' in chunk:
                    content = chunk['response']
            elif hasattr(chunk, "message"):
                msg = chunk.message
                if isinstance(msg, dict) and 'content' in msg:
                    content = msg['content']
                elif hasattr(msg, "content"):
                    content = msg.content
            elif hasattr(chunk, "response"):
                content = chunk.response

            bot_response += content
            print(content, end='', flush=True)
        print("\nBot has finished typing.")
        print(f"Bot: {bot_response}")
        messages.append(
            {"role": "assistant", "content": bot_response}
        )

if __name__ == "__main__":
    interactive_chat()

