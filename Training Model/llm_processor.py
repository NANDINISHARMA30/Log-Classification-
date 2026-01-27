import os
import re
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Safety check
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is not set")

# Initialize Groq client
client = Groq()

def classify_with_llm(log_msg: str) -> str:
    """
    Classifies a log message into:
    - Workflow Error
    - Deprecation Warning
    - Unclassified
    """

    prompt = f"""
You are a log classification system.

Classify the log message into ONE of the following categories ONLY:
- Workflow Error
- Deprecation Warning
- Unclassified

Return the answer strictly inside XML tags like:
<category>Workflow Error</category>

Log message:
{log_msg}
""".strip()

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # faster + stable
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            timeout=15
        )

        content = response.choices[0].message.content

        match = re.search(r"<category>\s*(.*?)\s*</category>", content, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return "Unclassified"

    except Exception as e:
        print("LLM classification failed:", str(e))
        return "Unclassified"


if __name__ == "__main__":
    test_logs = [
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active.",
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025",
        "System reboot initiated by user 12345."
    ]

    for log in test_logs:
        print(f"\nLog: {log}")
        print("Category:", classify_with_llm(log))



# import os
# from dotenv import load_dotenv

# load_dotenv()

# print("GROQ_API_KEY loaded:", os.getenv("GROQ_API_KEY") is not None)
