import os
import ast
from typing import List, Dict, Any

CUSTOM_ATTRIBUTE_CLASSES = {
    "AttributeValidationError",
    "BooleanAttribute",
    "DatetimeAttribute",
    "EmailAttribute",
    "EnumAttribute",
    "FloatAttribute",
    "IntegerAttribute",
    "IPAddressAttribute",
    "RelationshipAttribute",
    "StringAttribute",
}

class CodebaseScanner:
    def __init__(self):
        pass

    def scan_codebase(self, root_dir: str = '.') -> List[Dict]:
        annotated_classes = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    annotated_classes.extend(self.scan_file(file_path))
        return annotated_classes

    def scan_file(self, file_path: str) -> List[Dict]:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                tree = ast.parse(file.read(), filename=file_path)
            except SyntaxError as e:
                print(f"SyntaxError in file {file_path}: {e}")
                return []

        annotated_classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Skip scanning custom attribute classes themselves
                if node.name in CUSTOM_ATTRIBUTE_CLASSES:
                    continue

                attributes = self.extract_attributes(node)
                if attributes:
                    annotated_classes.append({
                        'name': self.to_camel_case(node.name),
                        'attributes': attributes
                    })
        return annotated_classes

    def extract_attributes(self, class_node: ast.ClassDef) -> List[Dict]:
        attributes = []
        for node in class_node.body:
            if isinstance(node, ast.AnnAssign):
                if not node.target or not node.value:
                    continue

                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    custom_attr_type = node.value.func.id
                    if custom_attr_type in CUSTOM_ATTRIBUTE_CLASSES:
                        attr_args = {kw.arg: self.parse_arg_value(kw.value) for kw in node.value.keywords}
                        attr_key = attr_args.get('attribute_key', self.to_camel_case(node.target.id))
                        
                        is_optional = self.check_optional(node.annotation)

                        attributes.append({
                            'key': attr_key,
                            'type': custom_attr_type,
                            'required': attr_args.get('required', False),
                            'optional': is_optional,
                            **attr_args
                        })

        return attributes

    def check_optional(self, annotation):
        if isinstance(annotation, ast.Subscript):
            if (isinstance(annotation.value, ast.Name) and annotation.value.id == 'Optional'):
                return True
            elif (isinstance(annotation.value, ast.Name) and annotation.value.id == 'Union'):
                for sub in annotation.slice.elts:
                    if isinstance(sub, ast.NameConstant) and sub.value is None:
                        return True
        return False

    @staticmethod
    def parse_arg_value(node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.NameConstant):
            return node.value
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            if isinstance(node.operand, ast.Num):
                return -node.operand.n
        elif isinstance(node, ast.List):
            return [CodebaseScanner.parse_arg_value(elt) for elt in node.elts]
        return None

    @staticmethod
    def to_camel_case(string: str) -> str:
        words = string.split('_')
        return words[0] + ''.join(word.capitalize() for word in words[1:])

# Example usage
if __name__ == "__main__":
    scanner = CodebaseScanner()
    annotated_classes = scanner.scan_codebase('.')
    for cls in annotated_classes:
        print(f"Class: {cls['name']}")
        for attr in cls['attributes']:
            print(f"  Attribute: {attr['key']}, Type: {attr['type']}, Additional Args: {attr}")