import json
import difflib
import os

# Files to save learned responses and memory
RESPONSES_FILE = "chatbot_responses.json"
MEMORY_FILE = "chatbot_memory.json"

# Load responses
if os.path.exists(RESPONSES_FILE):
    with open(RESPONSES_FILE, "r") as f:
        responses = json.load(f)
else:
    responses = {
        "hello": "Hi there! How can I help?",
        "how are you": "I'm just code, but I'm doing great!",
        "bye": "Goodbye!"
    }

# Load memory (facts bot remembers)
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def save_data():
    with open(RESPONSES_FILE, "w") as f:
        json.dump(responses, f)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # 🔹 Show all memory
    if user_input == "show memory":
        if memory:
            facts = "\n".join([f"- Your {k} is {v}" for k, v in memory.items()])
            return "Here’s what I remember:\n" + facts
        else:
            return "I don’t remember anything yet."

    # 🔹 Forget all memory
    if user_input == "forget memory":
        memory.clear()
        save_data()
        return "Okay, I’ve forgotten everything you told me."

    # 🔹 Store facts (patterns: "my ___ is ___")
    if user_input.startswith("my "):
        try:
            parts = user_input.split(" is ")
            if len(parts) == 2:
                key = parts[0].replace("my ", "").strip()
                value = parts[1].strip()
                memory[key] = value
                save_data()
                return f"Okay, I'll remember your {key} is {value}."
        except:
            pass

    # 🔹 Recall facts (patterns: "what is my ___")
    if user_input.startswith("what is my "):
        key = user_input.replace("what is my ", "").strip()
        if key in memory:
            return f"Your {key} is {memory[key]}."
        else:
            return f"I don’t know your {key} yet. You can tell me by saying 'my {key} is ...'."

    # 🔹 Check for best matching known response
    best_match = difflib.get_close_matches(user_input, responses.keys(), n=1, cutoff=0.6)
    if best_match:
        return responses[best_match[0]]

    # 🔹 Learn new response if not understood
    print("I don’t understand that. How should I reply?")
    new_response = input("You: ")
    responses[user_input] = new_response
    save_data()
    return "Got it! I'll remember that for next time."

# 🔹 Main chat loop
print("ChatBot with Memory: (type 'quit' to exit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Bot: Goodbye!")
        break
    print("Bot:", chatbot_response(user_input))
