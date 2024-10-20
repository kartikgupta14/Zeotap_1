from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import operator
from abc import ABC, abstractmethod

class NodeType(Enum):
    OPERATOR = "operator"
    OPERAND = "operand"
    COMPARISON = "comparison"

class Operator(Enum):
    AND = "AND"
    OR = "OR"
    GT = ">"
    LT = "<"
    EQ = "="
    GTE = ">="
    LTE = "<="

@dataclass
class Node:
    type: NodeType
    value: Optional[Union[str, int, float]] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    operator: Optional[Operator] = None
    field: Optional[str] = None

class RuleParser:
    def __init__(self):
        self.pos = 0
        self.tokens = []
    
    def tokenize(self, rule_string: str) -> List[str]:
        """Convert rule string into tokens"""
        rule_string = rule_string.replace('(', ' ( ').replace(')', ' ) ')
        return [token for token in rule_string.split() if token.strip()]
    
    def parse_comparison(self, tokens: List[str]) -> Node:
        field = tokens[0]
        op = tokens[1]
        value = tokens[2]
        
        # Convert value to appropriate type
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                value = value.strip("'\"")
        
        return Node(
            type=NodeType.COMPARISON,
            field=field,
            operator=Operator(op),
            value=value
        )
    
    def parse_expression(self, tokens: List[str]) -> Node:
        if tokens[0] == '(':
            # Find matching closing parenthesis
            count = 1
            i = 1
            while count > 0:
                if tokens[i] == '(':
                    count += 1
                elif tokens[i] == ')':
                    count -= 1
                i += 1
            
            left_expr = self.parse(tokens[1:i-1])
            
            if i >= len(tokens):
                return left_expr
            
            operator_token = tokens[i]
            right_expr = self.parse(tokens[i+1:])
            
            return Node(
                type=NodeType.OPERATOR,
                operator=Operator(operator_token),
                left=left_expr,
                right=right_expr
            )
        else:
            # Simple comparison
            return self.parse_comparison(tokens)
    
    def parse(self, tokens: List[str]) -> Node:
        if not tokens:
            raise ValueError("Empty rule")
        return self.parse_expression(tokens)

class RuleEngine:
    def __init__(self):
        self.parser = RuleParser()
    
    def create_rule(self, rule_string: str) -> Node:
        """Create AST from rule string"""
        tokens = self.parser.tokenize(rule_string)
        return self.parser.parse(tokens)
    
    def combine_rules(self, rules: List[str], combine_operator: Operator = Operator.AND) -> Node:
        """Combine multiple rules into a single AST"""
        if not rules:
            raise ValueError("No rules provided")
        
        if len(rules) == 1:
            return self.create_rule(rules[0])
        
        ast_nodes = [self.create_rule(rule) for rule in rules]
        combined = ast_nodes[0]
        
        for node in ast_nodes[1:]:
            combined = Node(
                type=NodeType.OPERATOR,
                operator=combine_operator,
                left=combined,
                right=node
            )
        
        return combined
    
    def evaluate_comparison(self, node: Node, data: Dict[str, Any]) -> bool:
        """Evaluate a comparison node"""
        if node.field not in data:
            raise ValueError(f"Field {node.field} not found in data")
        
        actual_value = data[node.field]
        expected_value = node.value
        
        if node.operator == Operator.GT:
            return actual_value > expected_value
        elif node.operator == Operator.LT:
            return actual_value < expected_value
        elif node.operator == Operator.EQ:
            return actual_value == expected_value
        elif node.operator == Operator.GTE:
            return actual_value >= expected_value
        elif node.operator == Operator.LTE:
            return actual_value <= expected_value
        else:
            raise ValueError(f"Unsupported operator: {node.operator}")
    
    def evaluate_node(self, node: Node, data: Dict[str, Any]) -> bool:
        """Evaluate a node in the AST"""
        if node.type == NodeType.COMPARISON:
            return self.evaluate_comparison(node, data)
        
        if node.operator == Operator.AND:
            return self.evaluate_node(node.left, data) and self.evaluate_node(node.right, data)
        elif node.operator == Operator.OR:
            return self.evaluate_node(node.left, data) or self.evaluate_node(node.right, data)
        
        raise ValueError(f"Invalid node type: {node.type}")
    
    def evaluate_rule(self, rule_ast: Node, data: Dict[str, Any]) -> bool:
        """Evaluate a rule against provided data"""
        try:
            return self.evaluate_node(rule_ast, data)
        except Exception as e:
            raise ValueError(f"Error evaluating rule: {str(e)}")
