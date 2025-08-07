# tasks.py
from crewai import Task


def research_task(customer_query):
    return Task(
        description=f"Use the retriever tool to find relevant information for: {customer_query}",
        expected_output="A summary of relevant facts from the knowledge base.",
        agent=None,
        output_file="research_output.txt"
    )

# tasks.py
def resolve_task():
    return Task(
        description="""
        Draft a response using ONLY the research findings.
        NEVER say 'I now can give a great answer'.
        NEVER use placeholders.
        Return only the final email.
        """,
        expected_output="A well-written reply based on research.",
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
