from antlr4.tree.Tree import TerminalNodeImpl

from Code import Utilities
from Code.Database import *
from Gen20.Java20Parser import Java20Parser
from Gen20.Java20ParserListener import Java20ParserListener


class RefListener(Java20ParserListener):
    def __init__(self, est):
        self.entity_est = est
        self.reference_est = []

    def get_est(self):
        return self.reference_est

    def print_entities(self):
        for entity in self.reference_est:
            print(entity)

    def finalize_est(self):
        for ref in self.reference_est:
            for e in self.entity_est:
                if e.name == ref.referrerId:
                    ref.referrerId = e.uid
                if e.name == ref.referredId:
                    ref.referredId = e.uid

    def exitClassExtends(self, ctx: Java20Parser.ClassExtendsContext):
        try:
            reference = Reference()
            reference.kind = 'inheritance'

            referrer_name = ctx.parentCtx.typeIdentifier().getChild(0).getText()
            referred_name = ctx.getChild(1).getText()

            reference.referrerId = referrer_name
            reference.referredId = referred_name

            self.reference_est.append(reference)
        except Exception as e:
            print('Error in exitClassExtends:', e)

    def exitClassImplements(self, ctx: Java20Parser.ClassImplementsContext):
        try:
            reference = Reference()
            reference.kind = 'inheritance'

            referrer_name = ctx.parentCtx.typeIdentifier().getChild(0).getText()
            referred_name = ctx.getChild(1).getText()

            reference.referrerId = referrer_name
            reference.referredId = referred_name

            self.reference_est.append(reference)
        except Exception as e:
            print('Error in exitClassImplements:', e)

    def exitAssignment(self, ctx: Java20Parser.AssignmentContext):
        reference = Reference()
        reference.kind = 'def_use'

        # look for scope
        reference.referrerId = Utilities.findParentScope(ctx)

        # We should look for leftHandSide definition
        lhs = ctx.getChild(0)
        while type(lhs) is not TerminalNodeImpl:
            lhs = lhs.getChild(0)
        lookup_symbol = lhs.getText()

        definition_uid = Utilities.getSymbolDefinition(lookup_symbol, lhs, self.entity_est)
        reference.referredId = definition_uid

        self.reference_est.append(reference)

    def exitMethodInvocation(self, ctx: Java20Parser.MethodInvocationContext):
        # search definition based on method name or instance name
        pass
