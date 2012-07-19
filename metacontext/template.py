import ast

from metacontext import Keyword

class QuoteKeyword(Keyword):

    def translate(self, translator, body, args, var):
        ast_sym = translator.gensym()
        Keyword.templates[ast_sym] = body
        mm = ast.Assign([var], ast.parse('Keyword.templates["%s"]' % ast_sym, mode='eval').body)
    
        locals_call = ast.copy_location(ast.Call(ast.Name('locals', ast.Load()), [], [], None, None), body[-1])

        expand = ast.copy_location(ast.Call(ast.Attribute(ast.Name('self', ast.Load()), 'expand', ast.Load()),
                          [ast.Name(var.id, ast.Load()), locals_call], [],  None, None), body[-1])

        ast.fix_missing_locations(expand)
        ast.fix_missing_locations(locals_call)

        return [mm, ast.Expr(expand)]


quote = QuoteKeyword()
unquote = object()
unquote_stmts = object()
