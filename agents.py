from crewai import Agent
from langchain_groq import ChatGroq  # <-- Use Groq
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

researcher = Agent(
    role="Senior Support Researcher",
    goal=(
        "Conduct a comprehensive and deep search across all knowledge base files to find "
        "the most accurate, relevant, and up-to-date information to answer the customer query. "
        "Do not stop at the first result — analyze all documents thoroughly. "
        "Return only clean, well-structured facts without assumptions or placeholder text."
    ),
    backstory=(
        "You are a meticulous Senior Support Researcher with expertise in information retrieval and data synthesis. "
        "You are responsible for scanning multiple internal documents — including policies, technical guides, "
        "and case studies — to extract precise answers. You cross-reference information, prioritize accuracy, "
        "and ensure no detail is missed. Your summaries are always clear, concise, and directly address the user's question."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# agents.py
resolver = Agent(
    role="Support Resolver",
    goal="Draft a clear, helpful, and customer-friendly response based SOLELY on the research findings. NEVER make up information.",
    backstory="""You are a customer support specialist who writes empathetic and accurate replies.
    You MUST use only the facts provided by the Support Researcher.
    You MUST NOT say 'I now can give a great answer'.
    You MUST NOT generate generic templates.
    You MUST return a complete, ready-to-send email.
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