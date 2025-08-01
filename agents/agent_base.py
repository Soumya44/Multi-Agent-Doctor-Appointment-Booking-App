from langchain_core.runnables import Runnable, RunnableConfig
from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.prompts.chat import ChatPromptTemplate

def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    dialog_state: Annotated[
        list[
            Literal[
                "assistant",
                "get_info",
                "appointment_info",
            ]
        ],
        update_dialog_stack,
    ]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)

            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}



def get_runnable(llm,tools,agent_prompt):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
            "system",
            agent_prompt
            ),
            ("placeholder", "{messages}"),
        ]
    )

    agent_runnable = prompt_template | llm.bind_tools(tools)
    return agent_runnable


    