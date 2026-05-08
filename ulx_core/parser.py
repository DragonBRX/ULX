#!/usr/bin/env python3
"""
ULX Parser - Analisador sintático completo com AST
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from .tokens import Token, TokenType
from .errors import (ULXSyntaxError, ULXError, ErrorContext, 
                     ErrorSeverity, ErrorCategory, ErrorHandler)


# ============ AST Nodes ============

@dataclass
class ASTNode:
    """Nó base da AST"""
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        visitor_method = getattr(visitor, method_name, self._default_visit)
        return visitor_method(self)
    
    def _default_visit(self, visitor):
        raise NotImplementedError(f"Visitador não implementado para {self.__class__.__name__}")


@dataclass 
class Program(ASTNode):
    """Nó raiz do programa"""
    statements: List[ASTNode] = field(default_factory=list)


@dataclass
class NumberLiteral(ASTNode):
    """Literal numérico"""
    value: Union[int, float] = 0


@dataclass
class StringLiteral(ASTNode):
    """Literal de string"""
    value: str = ""


@dataclass
class BooleanLiteral(ASTNode):
    """Literal booleano"""
    value: bool = False


@dataclass
class NullLiteral(ASTNode):
    """Literal nulo"""
    pass


@dataclass
class Identifier(ASTNode):
    """Identificador"""
    name: str = ""


@dataclass
class BinaryOp(ASTNode):
    """Operação binária"""
    left: ASTNode = None
    operator: str = ""
    right: ASTNode = None


@dataclass
class UnaryOp(ASTNode):
    """Operação unária"""
    operator: str = ""
    operand: ASTNode = None


@dataclass
class Assignment(ASTNode):
    """Atribuição"""
    name: str = ""
    value: ASTNode = None
    operator: str = "="  # =, +=, -=, *=, /=


@dataclass
class VariableDecl(ASTNode):
    """Declaração de variável com tipo opcional"""
    name: str = ""
    var_type: Optional[str] = None
    value: Optional[ASTNode] = None


@dataclass
class FunctionDef(ASTNode):
    """Definição de função"""
    name: str = ""
    params: List[Dict[str, Any]] = field(default_factory=list)  # {name, type, default}
    body: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None


@dataclass
class FunctionCall(ASTNode):
    """Chamada de função"""
    name: str = ""
    args: List[ASTNode] = field(default_factory=list)
    is_builtin: bool = False


@dataclass
class ReturnStmt(ASTNode):
    """Instrução de retorno"""
    value: Optional[ASTNode] = None


@dataclass
class IfStmt(ASTNode):
    """Instrução condicional"""
    condition: ASTNode = None
    then_body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileStmt(ASTNode):
    """Loop while"""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ForStmt(ASTNode):
    """Loop for"""
    init: Optional[ASTNode] = None
    condition: Optional[ASTNode] = None
    increment: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)
    is_foreach: bool = False
    iterator: Optional[str] = None
    iterable: Optional[ASTNode] = None


@dataclass
class BreakStmt(ASTNode):
    """Break"""
    pass


@dataclass
class ContinueStmt(ASTNode):
    """Continue"""
    pass


@dataclass
class PrintStmt(ASTNode):
    """Print (escreva)"""
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class InputStmt(ASTNode):
    """Input (leia)"""
    prompt: Optional[str] = None


@dataclass
class ArrayLiteral(ASTNode):
    """Literal de array"""
    elements: List[ASTNode] = field(default_factory=list)


@dataclass
class DictLiteral(ASTNode):
    """Literal de dicionário"""
    pairs: List[tuple] = field(default_factory=list)  # [(key, value)]


@dataclass
class IndexAccess(ASTNode):
    """Acesso por índice: arr[i]"""
    obj: ASTNode = None
    index: ASTNode = None


@dataclass
class MemberAccess(ASTNode):
    """Acesso a membro: obj.prop"""
    obj: ASTNode = None
    member: str = ""


@dataclass
class TryExcept(ASTNode):
    """Try/Except/Finally"""
    try_body: List[ASTNode] = field(default_factory=list)
    except_var: Optional[str] = None
    except_body: List[ASTNode] = field(default_factory=list)
    finally_body: List[ASTNode] = field(default_factory=list)


@dataclass
class ThrowStmt(ASTNode):
    """Lança exceção"""
    value: ASTNode = None


@dataclass
class ImportStmt(ASTNode):
    """Importação de módulo"""
    module: str = ""
    alias: Optional[str] = None
    names: List[str] = field(default_factory=list)


@dataclass
class ClassDef(ASTNode):
    """Definição de classe"""
    name: str = ""
    parent: Optional[str] = None
    methods: List[ASTNode] = field(default_factory=list)
    fields: List[ASTNode] = field(default_factory=list)


@dataclass
class Block(ASTNode):
    """Bloco de código"""
    statements: List[ASTNode] = field(default_factory=list)


# ============ Parser ============

class Parser:
    """Analisador sintático ULX"""
    
    def __init__(self, tokens: List[Token], source: str = "", filename: Optional[str] = None):
        self.tokens = tokens
        self.source = source
        self.filename = filename
        self.current = 0
        self.errors = ErrorHandler()
        
        # Estatísticas
        self.statement_count = 0
        self.function_count = 0
        self.class_count = 0
    
    def _make_context(self, token: Optional[Token] = None) -> ErrorContext:
        """Cria contexto de erro"""
        tok = token or self.current_token()
        return ErrorContext(
            line=tok.line,
            column=tok.column,
            filename=self.filename,
            code_snippet=self._get_line(tok.line)
        )
    
    def _get_line(self, line_num: int) -> str:
        """Obtém linha do código fonte"""
        lines = self.source.split('\n')
        if 0 < line_num <= len(lines):
            return lines[line_num - 1].strip()
        return ""
    
    def current_token(self) -> Token:
        """Retorna token atual"""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return self.tokens[-1] if self.tokens else Token(TokenType.EOF, '', 0, 0)
    
    def peek(self, offset: int = 0) -> Token:
        """Olha token à frente"""
        pos = self.current + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def is_at_end(self) -> bool:
        """Verifica se chegou ao fim"""
        return self.current_token().type == TokenType.EOF
    
    def advance(self) -> Token:
        """Avança para próximo token"""
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]
    
    def check(self, token_type: TokenType) -> bool:
        """Verifica se token atual é do tipo esperado"""
        if self.is_at_end():
            return False
        return self.current_token().type == token_type
    
    def match(self, *types: TokenType) -> bool:
        """Tenta casar tipos de token"""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def expect(self, token_type: TokenType, message: str = None) -> Token:
        """Espera um tipo específico de token"""
        if self.check(token_type):
            return self.advance()
        
        token = self.current_token()
        msg = message or f"Esperado '{token_type.name}', encontrado '{token.value}'"
        
        err = ULXSyntaxError(
            message=msg,
            context=self._make_context(token),
            expected=token_type.name,
            found=str(token.value)
        )
        self.errors.add_error(err)
        return token
    
    def synchronize(self):
        """Sincroniza após erro para continuar parsing"""
        self.advance()
        
        while not self.is_at_end():
            if self.peek(-1).type == TokenType.SEMICOLON:
                return
            
            if self.current_token().type in (
                TokenType.FUNCAO, TokenType.CLASSE, TokenType.SE,
                TokenType.ENQUANTO, TokenType.PARA, TokenType.RETORNA,
                TokenType.ESCREVA, TokenType.IMPORTE
            ):
                return
            
            self.advance()
    
    def parse(self) -> Program:
        """Parse completo do programa"""
        program = Program()
        
        while not self.is_at_end():
            try:
                stmt = self.parse_statement()
                if stmt:
                    program.statements.append(stmt)
                    self.statement_count += 1
            except ULXError as e:
                self.errors.add_error(e)
                self.synchronize()
        
        return program
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse de uma instrução"""
        # Pula newlines
        while self.match(TokenType.NEWLINE):
            pass
        
        if self.is_at_end():
            return None
        
        token = self.current_token()
        
        # Declarações
        if self.match(TokenType.ESCREVA):
            return self.parse_print()
        elif self.match(TokenType.LEIA):
            return self.parse_input()
        elif self.check(TokenType.FUNCAO):
            return self.parse_function_def()
        elif self.check(TokenType.CLASSE):
            return self.parse_class_def()
        elif self.match(TokenType.SE):
            return self.parse_if()
        elif self.match(TokenType.ENQUANTO):
            return self.parse_while()
        elif self.match(TokenType.PARA):
            return self.parse_for()
        elif self.match(TokenType.RETORNA):
            return self.parse_return()
        elif self.match(TokenType.PARE):
            return self.parse_break()
        elif self.match(TokenType.CONTINUA):
            return self.parse_continue()
        elif self.match(TokenType.TENTE):
            return self.parse_try_except()
        elif self.match(TokenType.LANCA):
            return self.parse_throw()
        elif self.match(TokenType.IMPORTE):
            return self.parse_import()
        
        # Bloco
        if self.match(TokenType.LBRACE):
            return self.parse_block()
        
        # Expressão ou atribuição
        return self.parse_expression_or_assignment()
    
    def parse_block(self) -> Block:
        """Parse de bloco { ... }"""
        block = Block(line=self.current_token().line, column=self.current_token().column)
        
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                block.statements.append(stmt)
        
        self.expect(TokenType.RBRACE, "Esperado '}' para fechar bloco")
        return block
    
    def parse_print(self) -> PrintStmt:
        """Parse de escreva(...)"""
        line = self.peek(-1).line
        self.expect(TokenType.LPAREN, "Esperado '(' após 'escreva'")
        
        args = []
        if not self.check(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                args.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN, "Esperado ')' após argumentos de escreva")
        return PrintStmt(args=args, line=line)
    
    def parse_input(self) -> InputStmt:
        """Parse de leia(...)"""
        line = self.peek(-1).line
        prompt = None
        
        if self.match(TokenType.LPAREN):
            if not self.check(TokenType.RPAREN):
                expr = self.parse_expression()
                if isinstance(expr, StringLiteral):
                    prompt = expr.value
            self.expect(TokenType.RPAREN, "Esperado ')' após 'leia'")
        
        return InputStmt(prompt=prompt, line=line)
    
    def parse_function_def(self) -> FunctionDef:
        """Parse de definição de função"""
        token = self.advance()  # consome 'funcao'
        line = token.line
        
        name_token = self.expect(TokenType.IDENTIFIER, 
                                  "Esperado nome da função após 'funcao'")
        name = name_token.value
        self.function_count += 1
        
        # Parâmetros
        self.expect(TokenType.LPAREN, "Esperado '(' após nome da função")
        params = []
        
        while not self.check(TokenType.RPAREN) and not self.is_at_end():
            param_token = self.expect(TokenType.IDENTIFIER, 
                                       "Esperado nome do parâmetro")
            param_name = param_token.value
            param_type = None
            param_default = None
            
            # Tipo opcional
            if self.match(TokenType.COLON):
                type_token = self.expect(TokenType.IDENTIFIER,
                                          "Esperado tipo após ':'")
                param_type = type_token.value
            
            # Valor padrão opcional
            if self.match(TokenType.ASSIGN):
                param_default = self.parse_expression()
            
            params.append({
                'name': param_name,
                'type': param_type,
                'default': param_default
            })
            
            if not self.match(TokenType.COMMA):
                break
        
        self.expect(TokenType.RPAREN, "Esperado ')' após parâmetros")
        
        # Tipo de retorno opcional
        return_type = None
        if self.match(TokenType.ARROW):
            type_token = self.expect(TokenType.IDENTIFIER,
                                      "Esperado tipo de retorno após '->'")
            return_type = type_token.value
        
        # Corpo
        self.expect(TokenType.LBRACE, "Esperado '{' para iniciar corpo da função")
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE, "Esperado '}' para fechar função")
        
        return FunctionDef(name=name, params=params, body=body,
                          return_type=return_type, line=line)
    
    def parse_if(self) -> IfStmt:
        """Parse de if/else"""
        line = self.peek(-1).line
        self.expect(TokenType.LPAREN, "Esperado '(' após 'se'")
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN, "Esperado ')' após condição")
        
        # Corpo do if
        then_body = []
        if self.match(TokenType.LBRACE):
            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    then_body.append(stmt)
            self.expect(TokenType.RBRACE, "Esperado '}' após 'se'")
        else:
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
        
        # Corpo do else
        else_body = []
        if self.match(TokenType.SENAO):
            if self.check(TokenType.SE):
                # else if
                self.advance()  # consome 'se'
                else_if = self.parse_if()
                else_body.append(else_if)
            elif self.match(TokenType.LBRACE):
                while not self.check(TokenType.RBRACE) and not self.is_at_end():
                    stmt = self.parse_statement()
                    if stmt:
                        else_body.append(stmt)
                self.expect(TokenType.RBRACE, "Esperado '}' após 'senao'")
            else:
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
        
        return IfStmt(condition=condition, then_body=then_body,
                     else_body=else_body, line=line)
    
    def parse_while(self) -> WhileStmt:
        """Parse de while"""
        line = self.peek(-1).line
        self.expect(TokenType.LPAREN, "Esperado '(' após 'enquanto'")
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN, "Esperado ')' após condição")
        
        body = []
        if self.match(TokenType.LBRACE):
            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.expect(TokenType.RBRACE, "Esperado '}' após 'enquanto'")
        else:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        return WhileStmt(condition=condition, body=body, line=line)
    
    def parse_for(self) -> ForStmt:
        """Parse de for"""
        line = self.peek(-1).line
        self.expect(TokenType.LPAREN, "Esperado '(' após 'para'")
        
        init = None
        condition = None
        increment = None
        
        # Inicialização
        if not self.check(TokenType.SEMICOLON):
            init = self.parse_expression_or_assignment()
        self.expect(TokenType.SEMICOLON, "Esperado ';' após inicialização")
        
        # Condição
        if not self.check(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON, "Esperado ';' após condição")
        
        # Incremento
        if not self.check(TokenType.RPAREN):
            increment = self.parse_expression_or_assignment()
        self.expect(TokenType.RPAREN, "Esperado ')' após incremento")
        
        # Corpo
        body = []
        if self.match(TokenType.LBRACE):
            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.expect(TokenType.RBRACE, "Esperado '}' após 'para'")
        else:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        return ForStmt(init=init, condition=condition, increment=increment,
                      body=body, line=line)
    
    def parse_return(self) -> ReturnStmt:
        """Parse de retorna"""
        line = self.peek(-1).line
        value = None
        
        # Verifica se há valor de retorno
        if not self.check(TokenType.NEWLINE) and not self.check(TokenType.RBRACE) and not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()
        
        return ReturnStmt(value=value, line=line)
    
    def parse_break(self) -> BreakStmt:
        """Parse de pare"""
        return BreakStmt(line=self.peek(-1).line)
    
    def parse_continue(self) -> ContinueStmt:
        """Parse de continua"""
        return ContinueStmt(line=self.peek(-1).line)
    
    def parse_try_except(self) -> TryExcept:
        """Parse de tente/pegue/finalmente"""
        line = self.peek(-1).line
        
        self.expect(TokenType.LBRACE, "Esperado '{' após 'tente'")
        try_body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                try_body.append(stmt)
        self.expect(TokenType.RBRACE, "Esperado '}' após bloco 'tente'")
        
        except_var = None
        except_body = []
        
        if self.match(TokenType.PEGUE):
            if self.match(TokenType.LPAREN):
                var_token = self.expect(TokenType.IDENTIFIER,
                                         "Esperado nome da variável em 'pegue'")
                except_var = var_token.value
                self.expect(TokenType.RPAREN, "Esperado ')'")
            
            self.expect(TokenType.LBRACE, "Esperado '{' após 'pegue'")
            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    except_body.append(stmt)
            self.expect(TokenType.RBRACE, "Esperado '}' após bloco 'pegue'")
        
        finally_body = []
        if self.match(TokenType.FINALMENTE):
            self.expect(TokenType.LBRACE, "Esperado '{' após 'finalmente'")
            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    finally_body.append(stmt)
            self.expect(TokenType.RBRACE, "Esperado '}' após bloco 'finalmente'")
        
        return TryExcept(try_body=try_body, except_var=except_var,
                        except_body=except_body, finally_body=finally_body,
                        line=line)
    
    def parse_throw(self) -> ThrowStmt:
        """Parse de lança"""
        line = self.peek(-1).line
        value = self.parse_expression()
        return ThrowStmt(value=value, line=line)
    
    def parse_import(self) -> ImportStmt:
        """Parse de importe"""
        line = self.peek(-1).line
        
        module_token = self.expect(TokenType.IDENTIFIER,
                                    "Esperado nome do módulo após 'importe'")
        module = module_token.value
        alias = None
        names = []
        
        if self.match(TokenType.COMO):
            alias_token = self.expect(TokenType.IDENTIFIER,
                                       "Esperado alias após 'como'")
            alias = alias_token.value
        
        return ImportStmt(module=module, alias=alias, names=names, line=line)
    
    def parse_class_def(self) -> ClassDef:
        """Parse de classe"""
        token = self.advance()  # consome 'classe'
        line = token.line
        
        name_token = self.expect(TokenType.IDENTIFIER,
                                  "Esperado nome da classe após 'classe'")
        name = name_token.value
        self.class_count += 1
        
        parent = None
        if self.match(TokenType.COLON):
            parent_token = self.expect(TokenType.IDENTIFIER,
                                        "Esperado nome da classe pai")
            parent = parent_token.value
        
        self.expect(TokenType.LBRACE, "Esperado '{' para iniciar classe")
        
        methods = []
        fields = []
        
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            # Modificadores de acesso
            is_private = self.match(TokenType.PRIVADO)
            is_public = self.match(TokenType.PUBLICO)
            is_static = self.match(TokenType.ESTATICO)
            
            if self.check(TokenType.FUNCAO):
                func = self.parse_function_def()
                methods.append(func)
            elif self.check(TokenType.IDENTIFIER):
                # Campo
                field = self.parse_expression_or_assignment()
                if field:
                    fields.append(field)
            else:
                stmt = self.parse_statement()
                if stmt:
                    fields.append(stmt)
        
        self.expect(TokenType.RBRACE, "Esperado '}' para fechar classe")
        
        return ClassDef(name=name, parent=parent, methods=methods,
                       fields=fields, line=line)
    
    def parse_expression_or_assignment(self) -> Optional[ASTNode]:
        """Parse de expressão ou atribuição"""
        expr = self.parse_expression()
        if expr is None:
            return None
        
        # Atribuição composta
        compound_ops = {
            TokenType.PLUS_ASSIGN: '+=',
            TokenType.MINUS_ASSIGN: '-=',
            TokenType.MULT_ASSIGN: '*=',
            TokenType.DIV_ASSIGN: '/=',
            TokenType.MOD_ASSIGN: '%=',
        }
        
        for token_type, op in compound_ops.items():
            if self.match(token_type):
                value = self.parse_expression()
                if isinstance(expr, Identifier):
                    return Assignment(name=expr.name, value=value, operator=op,
                                     line=expr.line, column=expr.column)
                else:
                    self.errors.add_error(ULXSyntaxError(
                        message="Lado esquerdo da atribuição deve ser um identificador",
                        context=self._make_context()
                    ))
                    return expr
        
        # Atribuição simples
        if self.match(TokenType.ASSIGN):
            value = self.parse_expression()
            if isinstance(expr, Identifier):
                return Assignment(name=expr.name, value=value, operator='=',
                                line=expr.line, column=expr.column)
            elif isinstance(expr, IndexAccess):
                # Atribuição a índice
                return Assignment(name=f"{expr.obj}_{expr.index}", 
                                value=value, operator='=',
                                line=expr.line, column=expr.column)
            else:
                self.errors.add_error(ULXSyntaxError(
                    message="Lado esquerdo da atribuição deve ser um identificador",
                    context=self._make_context()
                ))
                return expr
        
        return expr
    
    def parse_expression(self) -> Optional[ASTNode]:
        """Parse de expressão (nível mais baixo)"""
        return self.parse_or()
    
    def parse_or(self) -> Optional[ASTNode]:
        """Parse de OR lógico"""
        left = self.parse_and()
        if left is None:
            return None
        
        while self.match(TokenType.OR):
            right = self.parse_and()
            left = BinaryOp(left=left, operator='||', right=right,
                          line=left.line, column=left.column)
        
        return left
    
    def parse_and(self) -> Optional[ASTNode]:
        """Parse de AND lógico"""
        left = self.parse_equality()
        if left is None:
            return None
        
        while self.match(TokenType.AND):
            right = self.parse_equality()
            left = BinaryOp(left=left, operator='&&', right=right,
                          line=left.line, column=left.column)
        
        return left
    
    def parse_equality(self) -> Optional[ASTNode]:
        """Parse de igualdade"""
        left = self.parse_comparison()
        if left is None:
            return None
        
        while self.match(TokenType.EQ, TokenType.NE):
            op = '==' if self.peek(-1).type == TokenType.EQ else '!='
            right = self.parse_comparison()
            left = BinaryOp(left=left, operator=op, right=right,
                          line=left.line, column=left.column)
        
        return left
    
    def parse_comparison(self) -> Optional[ASTNode]:
        """Parse de comparação"""
        left = self.parse_term()
        if left is None:
            return None
        
        while self.match(TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE):
            op_map = {TokenType.GT: '>', TokenType.LT: '<',
                     TokenType.GTE: '>=', TokenType.LTE: '<='}
            op = op_map.get(self.peek(-1).type, '>')
            right = self.parse_term()
            left = BinaryOp(left=left, operator=op, right=right,
                          line=left.line, column=left.column)
        
        return left
    
    def parse_term(self) -> Optional[ASTNode]:
        """Parse de termos (+, -)"""
        left = self.parse_factor()
        if left is None:
            return None
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = '+' if self.peek(-1).type == TokenType.PLUS else '-'
            right = self.parse_factor()
            left = BinaryOp(left=left, operator=op, right=right,
                          line=left.line, column=left.column)
        
        return left
    
    def parse_factor(self) -> Optional[ASTNode]:
        """Parse de fatores (*, /, %)"""
        left = self.parse_power()
        if left is None:
            return None
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op_map = {TokenType.MULTIPLY: '*', TokenType.DIVIDE: '/',
                     TokenType.MODULO: '%'}
            op = op_map.get(self.peek(-1).type, '*')
            right = self.parse_power()
            left = BinaryOp(left=left, operator=op, right=right,
                          line=left.line, column=left.column)
        
        return left
    
    def parse_power(self) -> Optional[ASTNode]:
        """Parse de potência (^)"""
        left = self.parse_unary()
        if left is None:
            return None
        
        if self.match(TokenType.POWER):
            right = self.parse_power()  # right-associative
            left = BinaryOp(left=left, operator='^', right=right,
                          line=left.line, column=left.column)
        
        return left
    
    def parse_unary(self) -> Optional[ASTNode]:
        """Parse de operadores unários"""
        if self.match(TokenType.MINUS, TokenType.NOT, TokenType.BIT_NOT):
            op_map = {TokenType.MINUS: '-', TokenType.NOT: '!',
                     TokenType.BIT_NOT: '~'}
            op = op_map.get(self.peek(-1).type, '-')
            operand = self.parse_unary()
            return UnaryOp(operator=op, operand=operand,
                          line=self.peek(-1).line, column=self.peek(-1).column)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> Optional[ASTNode]:
        """Parse de operadores pós-fixos (chamada, índice, membro)"""
        left = self.parse_primary()
        if left is None:
            return None
        
        while True:
            # Chamada de função
            if self.match(TokenType.LPAREN):
                if isinstance(left, Identifier):
                    args = []
                    while not self.check(TokenType.RPAREN) and not self.is_at_end():
                        args.append(self.parse_expression())
                        if not self.match(TokenType.COMMA):
                            break
                    self.expect(TokenType.RPAREN, "Esperado ')' após argumentos")
                    left = FunctionCall(name=left.name, args=args,
                                       line=left.line, column=left.column)
                else:
                    self.errors.add_error(ULXSyntaxError(
                        message="Só identificadores podem ser chamados como funções",
                        context=self._make_context()
                    ))
                    # Consome argumentos para recuperar
                    while not self.check(TokenType.RPAREN) and not self.is_at_end():
                        self.advance()
                    self.match(TokenType.RPAREN)
            
            # Acesso por índice
            elif self.match(TokenType.LBRACKET):
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET, "Esperado ']' após índice")
                left = IndexAccess(obj=left, index=index,
                                  line=left.line, column=left.column)
            
            # Acesso a membro
            elif self.match(TokenType.DOT):
                member_token = self.expect(TokenType.IDENTIFIER,
                                            "Esperado nome do membro após '.'")
                left = MemberAccess(obj=left, member=member_token.value,
                                   line=left.line, column=left.column)
            
            else:
                break
        
        return left
    
    def parse_primary(self) -> Optional[ASTNode]:
        """Parse de valores primários"""
        # Números
        if self.match(TokenType.NUMBER):
            token = self.peek(-1)
            return NumberLiteral(value=token.value, line=token.line, 
                               column=token.column)
        
        # Strings
        if self.match(TokenType.STRING):
            token = self.peek(-1)
            return StringLiteral(value=token.value, line=token.line,
                               column=token.column)
        
        # Booleanos
        if self.match(TokenType.BOOLEAN):
            token = self.peek(-1)
            return BooleanLiteral(value=token.value, line=token.line,
                                column=token.column)
        
        # Nulo
        if self.match(TokenType.NULL):
            token = self.peek(-1)
            return NullLiteral(line=token.line, column=token.column)
        
        # Arrays
        if self.match(TokenType.LBRACKET):
            return self.parse_array()
        
        # Identificadores
        if self.match(TokenType.IDENTIFIER):
            token = self.peek(-1)
            return Identifier(name=token.value, line=token.line,
                            column=token.column)
        
        # Expressão entre parênteses
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Esperado ')' após expressão")
            return expr
        
        # Incremento/decremento
        if self.match(TokenType.INCREMENT, TokenType.DECREMENT):
            op = '++' if self.peek(-1).type == TokenType.INCREMENT else '--'
            operand = self.parse_unary()
            return UnaryOp(operator=op, operand=operand,
                          line=self.peek(-1).line, column=self.peek(-1).column)
        
        return None
    
    def parse_array(self) -> ArrayLiteral:
        """Parse de literal de array"""
        line = self.peek(-1).line
        elements = []
        
        while not self.check(TokenType.RBRACKET) and not self.is_at_end():
            elements.append(self.parse_expression())
            if not self.match(TokenType.COMMA):
                break
        
        self.expect(TokenType.RBRACKET, "Esperado ']' para fechar array")
        return ArrayLiteral(elements=elements, line=line)
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas do parsing"""
        return {
            'statements': self.statement_count,
            'functions': self.function_count,
            'classes': self.class_count,
            'errors': self.errors.error_count,
            'warnings': self.errors.warning_count,
        }
    
    def has_errors(self) -> bool:
        return self.errors.has_errors()
