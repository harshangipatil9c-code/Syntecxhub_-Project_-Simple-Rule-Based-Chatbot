import re
import random
import json
from datetime import datetime
from pathlib import Path


class RuleBasedChatbot:
    def __init__(self, name="PyBot"):
        self.name = name
        self.history = []
        self.log_file = "conversation_log.json"
        
        # Define intents with patterns and responses
        self.intents = {
            "greeting": {
                "patterns": [
                    r"\b(hi|hello|hey|greetings|howdy|hola)\b",
                    r"good (morning|afternoon|evening)"
                ],
                "responses": [
                    "Hello! How can I help you today?",
                    "Hi there! What can I do for you?",
                    "Hey! Nice to meet you.",
                    "Greetings! How may I assist you?"
                ]
            },
            "farewell": {
                "patterns": [
                    r"\b(bye|goodbye|see you|see ya|farewell|quit|exit)\b",
                    r"good night"
                ],
                "responses": [
                    "Goodbye! Have a great day!",
                    "See you later!",
                    "Bye! Take care.",
                    "Farewell! Come back soon."
                ]
            },
            "thanks": {
                "patterns": [
                    r"\b(thank you|thanks|thx|appreciate)\b"
                ],
                "responses": [
                    "You're welcome!",
                    "Happy to help!",
                    "My pleasure!",
                    "Anytime!"
                ]
            },
            "help": {
                "patterns": [
                    r"\b(help|assist|support|what can you do)\b",
                    r"how (do|does) (this|you) work"
                ],
                "responses": [
                    "I can help with greetings, small talk, and answer questions about Python, AI, and programming. Try asking me something!",
                    "Ask me anything! I know a bit about Python, machine learning, and general programming concepts.",
                    "I'm here to chat and answer questions. Type 'topics' to see what I know about."
                ]
            },
            "small_talk_how_are_you": {
                "patterns": [
                    r"how are you",
                    r"how (is it |you )going",
                    r"what's up"
                ],
                "responses": [
                    "I'm just a bot, but I'm functioning well! How about you?",
                    "Doing great, thanks for asking! What's on your mind?",
                    "All systems running smoothly! How are you?"
                ]
            },
            "small_talk_name": {
                "patterns": [
                    r"what('s| is) your name",
                    r"who are you"
                ],
                "responses": [
                    f"I'm {self.name}, a simple rule-based chatbot!",
                    f"My name is {self.name}. Nice to meet you!",
                    f"Call me {self.name}."
                ]
            },
            "joke": {
                "patterns": [
                    r"tell me a joke",
                    r"(say |tell |make )(something )?funny"
                ],
                "responses": [
                    "Why do programmers prefer dark mode? Because light attracts bugs!",
                    "Why did the developer go broke? Because he used up all his cache.",
                    "There are 10 types of people: those who understand binary and those who don't."
                ]
            },
            "topics": {
                "patterns": [
                    r"\b(topics|knowledge|subjects)\b",
                    r"what do you know"
                ],
                "responses": [
                    "I know about: Python, AI, machine learning, chatbots, variables, functions, and programming languages. Ask away!"
                ]
            }
        }
        
        # Knowledge base (domain Q&A)
        self.knowledge_base = {
            "python": "Python is a high-level, interpreted programming language known for its readability and versatility. Created by Guido van Rossum in 1991.",
            "ai": "Artificial Intelligence (AI) is the simulation of human intelligence by machines, especially computer systems.",
            "artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence by machines, especially computer systems.",
            "machine learning": "Machine learning is a subset of AI that enables systems to learn from data and improve without explicit programming.",
            "chatbot": "A chatbot is a software application that conducts conversations with users via text or voice, using rules or AI.",
            "variable": "A variable is a named storage location in memory that holds a value which can change during program execution.",
            "function": "A function is a reusable block of code that performs a specific task, optionally taking inputs and returning outputs.",
            "deep learning": "Deep learning is a subset of machine learning using neural networks with multiple layers to model complex patterns.",
            "neural network": "A neural network is a computational model inspired by the human brain, consisting of interconnected nodes (neurons).",
            "programming language": "A programming language is a formal language used to write instructions that a computer can execute."
        }
        
        self.default_responses = [
            "I'm not sure I understand. Could you rephrase?",
            "Hmm, I don't know about that. Try asking something else!",
            "That's outside my knowledge. Type 'help' to see what I can do.",
            "I didn't catch that. Can you try again?"
        ]
    
    def match_intent(self, user_input):
        """Match user input to an intent using regex patterns."""
        text = user_input.lower()
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data["patterns"]:
                if re.search(pattern, text):
                    return intent_name
        return None
    
    def search_knowledge_base(self, user_input):
        """Search knowledge base for matching keywords."""
        text = user_input.lower()
        # Sort keys by length (longer first) for better matching
        for key in sorted(self.knowledge_base.keys(), key=len, reverse=True):
            if key in text:
                return self.knowledge_base[key]
        return None
    
    def generate_response(self, user_input):
        """Generate a response based on intent or knowledge base."""
        if not user_input.strip():
            return "Please say something!"
        
        # Try matching intent first
        intent = self.match_intent(user_input)
        if intent:
            return random.choice(self.intents[intent]["responses"])
        
        # Try knowledge base
        kb_answer = self.search_knowledge_base(user_input)
        if kb_answer:
            return kb_answer
        
        # Default fallback
        return random.choice(self.default_responses)
    
    def log_conversation(self, user_input, bot_response):
        """Log conversation to history and file."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "bot": bot_response
        }
        self.history.append(entry)
    
    def save_log(self):
        """Save conversation history to a JSON file."""
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)
        print(f"[Conversation log saved to {self.log_file}]")
    
    def chat(self):
        """Start interactive chat session."""
        print("=" * 50)
        print(f"  {self.name} - Simple Rule-Based Chatbot")
        print("  Type 'quit', 'exit', or 'bye' to end.")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("You: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break
            
            if not user_input:
                continue
            
            response = self.generate_response(user_input)
            print(f"{self.name}: {response}")
            self.log_conversation(user_input, response)
            
            # End session on farewell intent
            if self.match_intent(user_input) == "farewell":
                break
        
        self.save_log()
        print(f"Total messages exchanged: {len(self.history)}")


if __name__ == "__main__":
    bot = RuleBasedChatbot(name="PyBot")
    bot.chat()
