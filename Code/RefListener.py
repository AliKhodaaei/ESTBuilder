from Code.Database import *
from Gen20.Java20Parser import Java20Parser
from Gen20.Java20ParserListener import Java20ParserListener


class RefListener(Java20ParserListener):
    def __init__(self, est):
        self.entity_est = est
        self.est = []

    def print_entities(self):
        for entity in self.entity_est:
            print(entity)

    def finalize_est(self):
        pass

    def exitClassExtends(self, ctx: Java20Parser.ClassExtendsContext):
        try:
            reference = Reference()
            reference.kind = 'inheritance'

            referrer_name = ctx.parentCtx.typeIdentifier().getChild(0).getText()
            referred_name = ctx.getChild(1).getText()
            for e in self.entity_est:
                if type(e) is Entity:
                    if e.name == referrer_name:
                        reference.referrerId = e.uid
                    elif e.name == referred_name:
                        reference.referredId = e.uid

            # if entities not exists in symbol table, just save entity name instead of uid
            if not reference.referrerId:
                reference.referrerId = referrer_name
            if not reference.referredId:
                reference.referredId = referred_name

            self.est.append(reference)
        except Exception as e:
            print('Error in exitClassExtends:', e)

    def exitClassImplements(self, ctx: Java20Parser.ClassImplementsContext):
        try:
            reference = Reference()
            reference.kind = 'inheritance'

            referrer_name = ctx.parentCtx.typeIdentifier().getChild(0).getText()
            referred_name = ctx.getChild(1).getText()
            for e in self.entity_est:
                if type(e) is Entity:
                    if e.name == referrer_name:
                        reference.referrerId = e.uid
                    elif e.name == referred_name:
                        reference.referredId = e.uid

            # if entities not exists in symbol table, just save entity name instead of uid
            if not reference.referrerId:
                reference.referrerId = referrer_name
            if not reference.referredId:
                reference.referredId = referred_name

            self.est.append(reference)
        except Exception as e:
            print('Error in exitClassExtends:', e)
