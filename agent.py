import os
from langgraph.graph import StateGraph
from agents.agent_base import State, Assistant, get_runnable
from models.model import ToAppointmentBookingAssistant, ToGetInfo, ToPrimaryBookingAssistant
from langgraph.graph import START, END
from dotenv import load_dotenv
from models.model import CompleteOrEscalate
from prompts.prompt import info_agent_prompt,booking_agent_prompt,primary_agent_prompt
from toolkit.tools import (set_appointment,
                         reschedule_appointment,
                         cancel_appointment,
                         check_availability_by_specialization,
                         check_availability_by_doctor
                         )
from utils.helper import (
                        create_entry_node,
                        create_tool_node_with_fallback,
                        pop_dialog_state,
                        RouteUpdater,
                        route_to_workflow,
                        route_primary_assistant
                        
)
from utils.llm_manager import LLMModel
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

memory = InMemorySaver()

llm = LLMModel().get_model()


info_tools = [check_availability_by_specialization,check_availability_by_doctor]
info_runnable = get_runnable(
                llm=llm,
                tools= info_tools + [CompleteOrEscalate],
                agent_prompt=info_agent_prompt
)

booking_tools = [set_appointment,reschedule_appointment,cancel_appointment]
booking_runnable = get_runnable(
                llm=llm,
                tools= booking_tools + [CompleteOrEscalate],
                agent_prompt=booking_agent_prompt
)

primary_tools = [ToAppointmentBookingAssistant,ToGetInfo,ToPrimaryBookingAssistant,CompleteOrEscalate]
primary_runnable = get_runnable(
                                llm=llm,
                                tools= primary_tools,
                                agent_prompt=primary_agent_prompt
)


def build_graph():
    builder = StateGraph(State)

    builder.add_node("primary_assistant", Assistant(primary_runnable))

    builder.add_node(
        "enter_get_info",
        create_entry_node("Get Information Assistant", "get_info"),
    )
    builder.add_node(
        "enter_appointment_info",
        create_entry_node("Appointment Assistant", "appointment_info"),
    )
    
    builder.add_node("get_info", Assistant(info_runnable))
    builder.add_node("appointment_info", Assistant(booking_runnable))

    builder.add_node(
        "update_info_tools",
        create_tool_node_with_fallback(info_tools),
    )

    builder.add_node(
        "update_appointment_tools",
        create_tool_node_with_fallback(booking_tools),
    )
    
    builder.add_node("leave_skill", pop_dialog_state)
    
    builder.add_conditional_edges(START,route_to_workflow)

    builder.add_conditional_edges(
        "primary_assistant",
        route_primary_assistant,
        [
            "enter_appointment_info",
            "enter_get_info",
            END,
        ],
    )

    builder.add_edge("enter_get_info","get_info")
    
    builder.add_edge("update_info_tools", "get_info")
    builder.add_conditional_edges(
        "get_info",
        RouteUpdater(info_tools,"update_info_tools").route_update_info,
        ["update_info_tools", "leave_skill", END],
    )

    
    builder.add_edge("leave_skill", "primary_assistant")

    builder.add_edge("enter_appointment_info", "appointment_info")


    builder.add_edge("update_appointment_tools", "appointment_info")
    builder.add_conditional_edges(
        "appointment_info",
        RouteUpdater(booking_tools,"update_appointment_tools").route_update_info,
        ["update_appointment_tools", "leave_skill", END],
    )


    graph = builder.compile(
        checkpointer=memory,
        # # Let the user approve or deny the use of sensitive tools
        # interrupt_before=[
        #     "update_appointment_tools"
        # ]
    )

    return graph