import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.rule_engine import RuleEngine, Node, NodeType, Operator

client = TestClient(app)

def test_create_rule():
    response = client.post(
        "/rules/create",
        json={"rule": "age > 30 AND department = 'Sales'"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "operator"
    assert data["operator"] == "AND"

def test_evaluate_rule():
    # First create a rule
    rule_response = client.post(
        "/rules/create",
        json={"rule": "age > 30 AND department = 'Sales'"}
    )
    rule_ast = rule_response.json()
    
    # Test evaluation with matching data
    eval_response = client.post(
        "/rules/evaluate",
        json={
            "rule_ast": rule_ast,
            "data": {"age": 35, "department": "Sales"}
        }
    )
    assert eval_response.status_code == 200
    assert eval_response.json()["result"] == True
    
    # Test evaluation with non-matching data
    eval_response = client.post(
        "/rules/evaluate",
        json={
            "rule_ast": rule_ast,
            "data": {"age": 25, "department": "Sales"}
        }
    )
    assert eval_response.status_code == 200
    assert eval_response.json()["result"] == False

def test_combine_rules():
    rules = [
        "age > 30 AND department = 'Sales'",
        "salary > 50000 OR experience > 5"
    ]
    
    response = client.post(
        "/rules/combine",
        json={"rules": rules, "combine_operator": "AND"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "operator"
    assert data["operator"] == "AND"

def test_invalid_rule():
    response = client.post(
        "/rules/create",
        json={"rule": "invalid rule syntax"}
    )
    assert response.status_code == 400

def test_rule_engine():
    engine = RuleEngine()
    
    # Test rule creation
    rule = "age > 30 AND department = 'Sales'"
    ast = engine.create_rule(rule)
    assert isinstance(ast, Node)
    assert ast.type == NodeType.OPERATOR
    assert ast.operator == Operator.AND
    
    # Test rule evaluation
    data = {"age": 35, "department": "Sales"}
    result = engine.evaluate_rule(ast, data)
    assert result == True
    
    data = {"age": 25, "department": "Sales"}
    result = engine.evaluate_rule(ast, data)
    assert result == False
