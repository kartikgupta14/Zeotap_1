from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from rule_engine import RuleEngine, Node, Operator
import json

app = FastAPI()
rule_engine = RuleEngine()

class RuleRequest(BaseModel):
    rule: str

class RulesRequest(BaseModel):
    rules: List[str]
    combine_operator: str = "AND"

class EvaluationRequest(BaseModel):
    rule_ast: Dict[str, Any]
    data: Dict[str, Any]

def node_to_dict(node: Node) -> Dict[str, Any]:
    """Convert Node object to dictionary for JSON serialization"""
    result = {
        "type": node.type.value,
    }
    
    if node.operator:
        result["operator"] = node.operator.value
    if node.value is not None:
        result["value"] = node.value
    if node.field:
        result["field"] = node.field
    if node.left:
        result["left"] = node_to_dict(node.left)
    if node.right:
        result["right"] = node_to_dict(node.right)
    
    return result

def dict_to_node(data: Dict[str, Any]) -> Node:
    """Convert dictionary back to Node object"""
    node = Node(type=NodeType(data["type"]))
    
    if "operator" in data:
        node.operator = Operator(data["operator"])
    if "value" in data:
        node.value = data["value"]
    if "field" in data:
        node.field = data["field"]
    if "left" in data:
        node.left = dict_to_node(data["left"])
    if "right" in data:
        node.right = dict_to_node(data["right"])
    
    return node

@app.post("/rules/create")
async def create_rule(request: RuleRequest):
    try:
        ast = rule_engine.create_rule(request.rule)
        return node_to_dict(ast)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rules/combine")
async def combine_rules(request: RulesRequest):
    try:
        combined_ast = rule_engine.combine_rules(
            request.rules,
            Operator(request.combine_operator)
        )
        return node_to_dict(combined_ast)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rules/evaluate")
async def evaluate_rule(request: EvaluationRequest):
    try:
        ast = dict_to_node(request.rule_ast)
        result = rule_engine.evaluate_rule(ast, request.data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
