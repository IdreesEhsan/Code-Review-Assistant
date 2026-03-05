from langgraph.graph import StateGraph, START, END
from graph.state import CodeReviewState
from agents import (
    router_node, style_node, bug_node, 
    security_node, fix_node, reporter_node,
)

def build_review_graph():
    graph = StateGraph(CodeReviewState)
    
    # Register nodes
    graph.add_node('router', router_node)
    graph.add_node('style', style_node)
    graph.add_node('bug', bug_node)
    graph.add_node('security', security_node)
    graph.add_node('fix', fix_node)
    graph.add_node('reporter', reporter_node)
    
    # Entry
    graph.add_edge(START, 'router')
    graph.add_edge('router', 'style')
    graph.add_edge('router', 'bug')
    graph.add_edge('router', 'security')
    
    # Fan-in -> fix
    graph.add_edge('style', 'fix')
    graph.add_edge('bug', 'fix')
    graph.add_edge('security', 'fix')
    
    # Fix -> reporter -> END
    graph.add_edge('fix', 'reporter')
    graph.add_edge('reporter', END)
    
    return graph.compile()

review_graph = build_review_graph()