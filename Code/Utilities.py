from Gen20.Java20Parser import Java20Parser


def findParentClassOrInterface(ctx, entity):
    while type(ctx) is not Java20Parser.NormalClassDeclarationContext and type(ctx) is not Java20Parser.NormalInterfaceDeclarationContext:
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
