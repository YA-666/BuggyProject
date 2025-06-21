
from langgraph.graph import StateGraph
from .agents.user_agent import user_agent
from .agents.meta_agent import meta_agent
from .agents.safety_agent import safety_agent
from .magic_rect import magic_rect  # ensure imported so singleton exists

def build_app():
    graph=StateGraph()
    graph.add_node("User",user_agent)
    graph.add_node("Meta",meta_agent)
    graph.add_node("Safety",safety_agent)
    graph.set_entry("User")
    graph.add_edge("User","Meta")
    graph.add_edge("Meta","Safety")
    return graph.compile()

app=build_app()
