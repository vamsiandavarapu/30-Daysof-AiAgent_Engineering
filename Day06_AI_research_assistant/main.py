import json

from langchain_core.messages import HumanMessage, ToolMessage
from config import llm
from tools import google_search
from schemas import ResearchReport
from memory import ConversationMemory
from prompts import tool_selection_prompt, research_prompt
from email_service import send_report_email

# Initialize conversation memory
memory = ConversationMemory()

# Bind Google Search tool to the LLM
tool_llm = llm.bind_tools([google_search])

# Create structured-output model
structured_llm = llm.with_structured_output(
    ResearchReport, method="json_schema", strict=True
)
# Map tool names to their Python tool objects
tool_map = {"google_search": google_search}


def format_history(messages):
    """Convert conversation messages into readable text."""

    history_text = []

    for message in messages:
        if isinstance(message, HumanMessage):
            role = "User"
        else:
            role = "Assistant"

        history_text.append(f"{role}: {message.content}")

    return "\n".join(history_text)


def run_assistant(question):
    """Process a user question and generate an answer."""

    # 1. Prepare conversation messages
    messages = memory.get_history().copy()

    messages.append(HumanMessage(content=question))

    search_results = []

    # 2. Ask the LLM whether a tool is needed
    prompt_value = tool_selection_prompt.invoke({"messages": messages})

    response = tool_llm.invoke(prompt_value)

    # 3. Execute requested tools
    max_tool_rounds = 3
    round_count = 0

    while response.tool_calls and round_count < max_tool_rounds:

        messages.append(response)

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            if tool_name not in tool_map:
                raise ValueError(f"Unknown tool requested: {tool_name}")

            # Execute the Python tool
            result = tool_map[tool_name].invoke(tool_args)

            search_results.append(result)

            # Return the result to the LLM
            messages.append(
                ToolMessage(content=json.dumps(result), tool_call_id=tool_id)
            )

        round_count += 1

        # Ask the LLM what to do next
        response = tool_llm.invoke(messages)

    # 4. Generate the final response
    if search_results:

        history_text = format_history(memory.get_history())

        synthesis_input = research_prompt.invoke(
            {
                "question": question,
                "history": history_text,
                "search_results": json.dumps(search_results, indent=2),
            }
        )

        report = structured_llm.invoke(synthesis_input)

        answer = report.model_dump_json(indent=2)

        print("\n========== RESEARCH REPORT ==========")
        print(f"\nQuestion: {report.research_question}")
        print(f"\nSummary:\n{report.summary}")

        print("\nKey Findings:")

        for finding in report.key_findings:
            print(f"- {finding}")

        print("\nSources:")

        for source in report.sources:
            print(f"- {source.title}")
            print(f"  URL: {source.url}")
        # Ask for permission before sending the report

        send_email = (
            input("\nWould you like to email this research report? (yes/no): ")
            .strip()
            .lower()
        )

        if send_email in ["yes", "y"]:

            recipient = input("Enter recipient email address: ").strip()

            if not recipient:
                print("Recipient email address cannot be empty.")

            else:
                try:
                    send_report_email(report, recipient=recipient)

                    print(f"\nResearch report sent successfully to {recipient}!")

                except Exception as error:
                    print(f"\nEmail delivery failed: {error}")

        else:
            print("\nEmail delivery skipped.")

    else:

        # No search was needed; use the direct LLM response
        answer = response.content

        print("\n========== ASSISTANT ==========")
        print(answer)

    # 5. Update conversation memory
    memory.add_user_message(question)
    memory.add_ai_message(answer)


def main():

    print("=" * 45)
    print("       AI RESEARCH ASSISTANT")
    print("=" * 45)

    print("\nAsk a research question.")
    print("Type 'exit' to quit.")
    print("Type 'clear' to reset conversation memory.")

    while True:

        question = input("\nYou: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if question.lower() == "clear":
            memory.clear()
            print("Conversation memory cleared.")
            continue

        try:
            run_assistant(question)

        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
