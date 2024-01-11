from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from Gen20.Java20Lexer import Java20Lexer
from Gen20.Java20Parser import Java20Parser

def build_tree(path):
    # Reading the Java source code
    input_stream = FileStream(path)

    # Creating a lexer object
    lexer = Java20Lexer(input_stream)

    # Creating a token stream
    stream = CommonTokenStream(lexer)

    # Creating a parser object
    parser = Java20Parser(stream)

    # Creating a parse tree
    tree = parser.compilationUnit()

    return tree


def scan_tree(tree, listener):
    # Walking the parse tree
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Finalize database (Convert scope name to scope id)
    # If you want to scope names instead of scope id, comment this line
    # listener.finalize_est()

    return listener.get_est()
