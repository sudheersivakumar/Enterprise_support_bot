from crewai import Agent
from langchain_groq import ChatGroq  # <-- Use Groq
from retriever import create_knowledge_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model="groq/llama3-70b-8192",  # or "mixtral-8x7b-32768", "gemma-7b-it"
    temperature=0.4,
    max_tokens=8192,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Create retriever
retriever = create_knowledge_base()
# agents.py
researcher = Agent(
    role="Senior Support Researcher",
    goal=(
        "Search the knowledge base and return ONLY the relevant facts. "
        "Do NOT draft replies, greetings, or placeholders. "
        "Return concise, bullet-point style facts that the Resolver can use."
    ),
    backstory=(
        "You are an expert at searching internal documentation. "
        "You return only factual summaries — no opinions, no greetings, no filler. "
        "If the answer is in the knowledge base, extract it verbatim or summarize it precisely. "
        "If the information is not found, say 'No relevant information found in knowledge base.'"
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# agents.py
resolver = Agent(
    role="Support Resolver",
    goal="Draft a clear, helpful, and customer-friendly response using ONLY the research findings.",
    backstory="""You are a customer support specialist who writes empathetic and accurate replies.
    You use ONLY the facts from the Researcher Agent.
    You NEVER say 'I now can give a great answer'.
    You NEVER use placeholders or templates.
    You return a complete, ready-to-send email.
    """,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

reviewer = Agent(
    role="Support Reviewer",
    goal="Review the draft from the Support Resolver and return ONLY the final polished response. NEVER generate a new placeholder.",
    backstory="""You are a senior support lead. Your job is to:
    - Review the draft response for accuracy, tone, and clarity.
    - Ensure it is professional and customer-friendly.
    - Return the Resolver's polished response as the final output.
    - NEVER say 'I now can give a great answer' — return the actual customer reply.
    """,
    allow_delegation=False,
    verbose=True,
    llm=llm
)
