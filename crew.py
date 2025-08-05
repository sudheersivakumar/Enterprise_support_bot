# crew.py
from crewai import Crew
from tasks import research_task, resolve_task, review_task
from agents import researcher, resolver, reviewer
import os
import time

# crew.py
def run_support_crew(customer_query):
    # Create tasks
    tasks = [
        research_task(customer_query),  # ✅ Pass the query here
        resolve_task(),
        review_task()
    ]

    # Assign agents
    tasks[0].agent = researcher
    tasks[1].agent = resolver
    tasks[2].agent = reviewer

    # Create crew
    crew = Crew(
        agents=[researcher, resolver, reviewer],
        tasks=tasks,
        verbose=True,
        process='sequential',
        full_output=True,
        share_crew=False,
        manager_llm=researcher.llm
    )

    
    # Run the crew
    result = crew.kickoff()

    try:
        if hasattr(result, 'final_output') and result.final_output:
            if "great answer" not in result.final_output and len(result.final_output) > 100:
                return result.final_output.strip()
    except:
        pass

    # ✅ 2. Fallback: Read Resolver's output from file
    try:
        time.sleep(1)
        if os.path.exists("resolution_output.txt"):
            with open("resolution_output.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content and "great answer" not in content and "template" not in content:
                    return content
    except Exception as e:
        print("File read error:", str(e))

    # ✅ 3. Ultimate fallback
    return "We are currently processing your request. Please try again later."