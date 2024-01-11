import uuid

from Gen20.Java20Parser import Java20Parser


def findParentClassOrInterface(ctx, entity):
    while type(ctx) is not Java20Parser.NormalClassDeclarationContext and type(
            ctx) is not Java20Parser.NormalInterfaceDeclarationContext:
        ctx = ctx.parentCtx

    parent_class_name = ctx.typeIdentifier().getChild(0).getText()
    if parent_class_name:
        entity.scope = parent_class_name


def findParentMethod(ctx, entity):
    while type(ctx) is not Java20Parser.MethodDeclarationContext:
        ctx = ctx.parentCtx

    parent_class_name = ctx.methodHeader().getChild(1).Identifier().getText()
    if parent_class_name:
        entity.scope = parent_class_name


def setParentScope(ctx, entity):
    entity.scope = findParentScope(ctx)


def findParentScope(ctx):
    while ctx.parentCtx is not None:
        ctx = ctx.parentCtx
        if type(ctx) is Java20Parser.BlockContext:
            return ctx.scope_id
        if type(ctx) is Java20Parser.NormalClassDeclarationContext or type(
                ctx) is Java20Parser.NormalInterfaceDeclarationContext:
            parent_class_name = ctx.typeIdentifier().getChild(0).getText()
            if parent_class_name:
                return parent_class_name
        if type(ctx) is Java20Parser.MethodDeclarationContext:
            parent_class_name = ctx.methodHeader().getChild(1).Identifier().getText()
            if parent_class_name:
                return parent_class_name


def getSymbolDefinition(symbol, ctx, entity_est):
    scope = findParentScope(ctx)
    while scope:
        scope_entities = [entity for entity in entity_est if entity.scope == scope]
        for e in scope_entities:
            if e.name == symbol:
                return e.uid

        # update scope
        pe = next(e for e in entity_est if e.uid == scope or e.name == scope)
        scope = pe.scope


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
