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


def findParentScope(ctx, entity):
    while ctx.parentCtx is not None:
        ctx = ctx.parentCtx
        if type(ctx) is Java20Parser.BlockContext:
            entity.scope = ctx.scope_id
            break
        if type(ctx) is Java20Parser.NormalClassDeclarationContext or type(
            ctx) is Java20Parser.NormalInterfaceDeclarationContext:
            parent_class_name = ctx.typeIdentifier().getChild(0).getText()
            if parent_class_name:
                entity.scope = parent_class_name
            break
        if type(ctx) is Java20Parser.MethodDeclarationContext:
            parent_class_name = ctx.methodHeader().getChild(1).Identifier().getText()
            if parent_class_name:
                entity.scope = parent_class_name
            break


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
