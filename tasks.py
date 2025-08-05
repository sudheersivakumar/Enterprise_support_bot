# tasks.py
from crewai import Task

# tasks.py
def research_task(customer_query):
    return Task(
        description=f"Search the knowledge base to find relevant information for the customer query: {customer_query}",
        expected_output="A summary of relevant facts from the knowledge base.",
        agent=None,
        output_file="research_output.txt"
    )

# tasks.py
def resolve_task():
    return Task(
        description="""
        Draft a customer-friendly response using the research findings.
        The response must include:
        - A greeting
        - Step-by-step instructions for resetting a password
        - Password requirements
        - Troubleshooting tips
        - A professional closing
        Do NOT write a generic template.
        Do NOT say 'I now can give a great answer'.
        Return only the final email.
        """,
        expected_output="A well-written, concise reply to the customer.",
        agent=None,
        output_file="resolution_output.txt"
    )

def review_task():
    return Task(
        description="Review the draft response for accuracy, tone, and clarity. Finalize it.",
        expected_output="The final approved response ready to send to the customer.",
        agent=None,
        output_file="final_response.txt"
    )