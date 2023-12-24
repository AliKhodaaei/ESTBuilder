from antlr4.tree.Tree import TerminalNodeImpl

from Code import Utilities
from Code.Database import *
from Gen20.Java20Parser import Java20Parser
from Gen20.Java20ParserListener import Java20ParserListener


# Defining the listener class
class EstListener(Java20ParserListener):
    def __init__(self, filename, projectname):
        self.est = []
        self.filename = filename
        self.packagename = None
        self.projectname = projectname.split('/')[-1]
        entity = Entity()
        entity.kind = 'file'
        entity.name = filename
        self.est.append(entity)

    # Method for resolve scope names and replace with their uid
    def finalize_est(self):
        for entity in self.est:
            if entity.scope and not Utilities.is_valid_uuid(entity.scope):
                default_entity = Entity()
                default_entity.uid = 0
                parent_entity = next((e for e in self.est if e.kind in ['file', 'class', 'interface', 'method', 'package'] and e.name == entity.scope), default_entity)
                if parent_entity.uid != 0:
                    entity.scope = parent_entity.uid

    def print_entities(self):
        for entity in self.est:
            print(entity)

    def enterBlock(self, ctx: Java20Parser.BlockContext):
        entity = Entity()
        entity.kind = 'block'
        ctx.scope_id = entity.uid
        self.est.append(entity)

    def exitBlock(self, ctx: Java20Parser.BlockContext):
        parent_ctx = ctx.parentCtx
        entity = next((e for e in self.est if e.kind == 'block' and e.uid == ctx.scope_id))
        Utilities.findParentScope(parent_ctx, entity)

    def exitPackageDeclaration(self, ctx: Java20Parser.PackageDeclarationContext):
        try:
            entity = Entity()
            entity.kind = 'package'
            entity.name = ''
            for i in range(1, ctx.getChildCount()):
                if ctx.getChild(i).getText() == ';':
                    break
                entity.name += ctx.getChild(i).getText()

            entity.scope = self.projectname

            self.est.append(entity)
            self.packagename = entity.name
        except Exception as e:
            print('Error in exitPackageDeclaration:', e)

    def exitImportDeclaration(self, ctx: Java20Parser.ImportDeclarationContext):
        try:
            entity = Entity()
            entity.kind = "import"
            ctx = ctx.getChild(0)  # reach singleTypeImportDeclaration
            ctx = ctx.getChild(1)  # reach typeName
            ctx = ctx.getChild(0)  # reach packageName

            entity.name = ''
            while ctx is not None:
                entity.name += ctx.getChild(0).getText() + '.'
                ctx = ctx.getChild(2)  # reach rest of package name if any
            entity.name = entity.name[:-1]

            entity.scope = self.packagename

            self.est.append(entity)
        except Exception as e:
            print('Error in exitImportDeclaration:', e)

    def exitNormalClassDeclaration(self, ctx: Java20Parser.NormalClassDeclarationContext):
        try:
            entity = Entity()
            entity.kind = 'class'
            entity.name = ctx.typeIdentifier().getChild(0).getText()
            entity.type = ctx.typeIdentifier().getChild(0).getText()

            if type(ctx.parentCtx.parentCtx) is Java20Parser.TopLevelClassOrInterfaceDeclarationContext:
                entity.scope = self.packagename if self.packagename else self.filename
            else:
                parent_class_ctx = ctx.parentCtx
                Utilities.findParentScope(parent_class_ctx, entity)

            entity.modifier = ''
            for i in range(ctx.getChildCount()):  # iterate all modifiers if more than one modifier exists
                class_token = ctx.getChild(i).getText()
                if class_token.lower() == 'class':
                    break
                entity.modifier += ctx.getChild(i).getChild(0).getText() + ' '

            entity.modifier = entity.modifier[:-1]
            self.est.append(entity)
        except Exception as e:
            print('Error in exitNormalClassDeclaration:', e)

    def exitNormalInterfaceDeclaration(self, ctx: Java20Parser.NormalInterfaceDeclarationContext):
        try:
            entity = Entity()
            entity.kind = 'interface'
            entity.name = ctx.typeIdentifier().getChild(0).getText()
            entity.type = ctx.typeIdentifier().getChild(0).getText()

            if type(ctx.parentCtx.parentCtx) is Java20Parser.TopLevelClassOrInterfaceDeclarationContext:
                entity.scope = self.filename
            else:
                parent_class_ctx = ctx.parentCtx
                Utilities.findParentScope(parent_class_ctx, entity)

            entity.modifier = ''
            for i in range(ctx.getChildCount()):  # iterate all modifiers if more than one modifier exists
                interface_token = ctx.getChild(i).getText()
                if interface_token.lower() == 'interface':
                    break
                entity.modifier += ctx.getChild(i).getChild(0).getText() + ' '

            entity.modifier = entity.modifier[:-1]
            self.est.append(entity)
        except Exception as e:
            print('Error in exitNormalInterfaceDeclaration:', e)

    def exitEnumDeclaration(self, ctx: Java20Parser.EnumDeclarationContext):
        try:
            entity = Entity()
            entity.kind = 'enum'
            entity.name = ctx.typeIdentifier().getChild(0).getText()
            entity.type = ctx.typeIdentifier().getChild(0).getText()

            if type(ctx.parentCtx.parentCtx) is Java20Parser.TopLevelClassOrInterfaceDeclarationContext:
                entity.scope = self.filename
            else:
                parent_class_ctx = ctx.parentCtx
                Utilities.findParentScope(parent_class_ctx, entity)

            entity.modifier = ''
            for i in range(ctx.getChildCount()):  # iterate all modifiers if more than one modifier exists
                interface_token = ctx.getChild(i).getText()
                if interface_token.lower() == 'enum':
                    break
                entity.modifier += ctx.getChild(i).getChild(0).getText() + ' '

            entity.modifier = entity.modifier[:-1]
            self.est.append(entity)
        except Exception as e:
            print('Error in exitEnumDeclaration:', e)

    def exitRecordDeclaration(self, ctx: Java20Parser.RecordDeclarationContext):
        try:
            entity = Entity()
            entity.kind = 'record'
            entity.name = ctx.typeIdentifier().getChild(0).getText()
            entity.type = ctx.typeIdentifier().getChild(0).getText()

            if type(ctx.parentCtx.parentCtx) is Java20Parser.TopLevelClassOrInterfaceDeclarationContext:
                entity.scope = self.filename
            else:
                parent_class_ctx = ctx.parentCtx
                Utilities.findParentScope(parent_class_ctx, entity)

            entity.modifier = ''
            for i in range(ctx.getChildCount()):  # iterate all modifiers if more than one modifier exists
                interface_token = ctx.getChild(i).getText()
                if interface_token.lower() == 'record':
                    break
                entity.modifier += ctx.getChild(i).getChild(0).getText() + ' '

            entity.modifier = entity.modifier[:-1]
            self.est.append(entity)
        except Exception as e:
            print('Error in exitRecordDeclaration:', e)

    def exitFieldDeclaration(self, ctx: Java20Parser.FieldDeclarationContext):
        try:
            entity = Entity()
            entity.kind = 'field'
            entity.modifier = ''

            for i in range(ctx.getChildCount()):
                if type(ctx.getChild(i)) is Java20Parser.FieldModifierContext:
                    entity.modifier += ctx.getChild(i).getText() + ' '
            entity.modifier = entity.modifier[:-1]

            type_ctx = ctx.unannType()  # reach type of field
            var_ctx = ctx.variableDeclaratorList().getChild(0)  # reach variable info

            while type(type_ctx) is not TerminalNodeImpl:
                type_ctx = type_ctx.getChild(0)
            entity.type = type_ctx.getText()

            entity.name = var_ctx.getChild(0).getText()

            # Check if field has value or not
            if var_ctx.getChildCount() > 1:
                var_ctx = var_ctx.getChild(2)
                while type(var_ctx) is not TerminalNodeImpl:
                    var_ctx = var_ctx.getChild(0)

            entity.value = var_ctx.getText()

            parent_class_ctx = ctx.parentCtx
            Utilities.findParentScope(parent_class_ctx, entity)

            self.est.append(entity)
        except Exception as e:
            print('Error in exitFieldDeclaration:', e)

    def exitMethodDeclaration(self, ctx: Java20Parser.MethodDeclarationContext):
        try:
            entity = Entity()
            entity.kind = 'method'
            entity.modifier = ''

            for i in range(ctx.getChildCount()):
                if type(ctx.getChild(i)) is Java20Parser.MethodModifierContext:
                    entity.modifier += ctx.getChild(i).getText() + ' '

            return_type = ctx.methodHeader().getChild(0)
            declarator = ctx.methodHeader().getChild(1)
            while type(return_type) is not TerminalNodeImpl:
                return_type = return_type.getChild(0)
            entity.return_type = return_type.getText()
            entity.name = declarator.getChild(0).getText()
            parent_class_ctx = ctx.parentCtx
            Utilities.findParentScope(parent_class_ctx, entity)
            self.est.append(entity)
        except Exception as e:
            print('Error in exitMethodDeclaration:', e)

    def exitFormalParameter(self, ctx: Java20Parser.FormalParameterContext):
        try:
            entity = Entity()
            entity.kind = 'parameter'
            parameter_type = ctx.getChild(0)
            parameter_name = ctx.getChild(1)

            while type(parameter_type) is not TerminalNodeImpl:
                parameter_type = parameter_type.getChild(0)
            entity.type = parameter_type.getText()

            while type(parameter_name) is not TerminalNodeImpl:
                parameter_name = parameter_name.getChild(0)
            entity.name = parameter_name.getText()
            parent_method_ctx = ctx.parentCtx
            Utilities.findParentScope(parent_method_ctx, entity)
            self.est.append(entity)
        except Exception as e:
            print('Error in exitFormalParameter:', e)

    def exitLocalVariableDeclaration(self, ctx: Java20Parser.LocalVariableDeclarationContext):
        try:
            entity = Entity()
            entity.kind = 'variable'
            entity.modifier = ''

            for i in range(ctx.getChildCount()):
                if type(ctx.getChild(i)) is Java20Parser.VariableModifierContext:
                    entity.modifier += ctx.getChild(i).getText() + ' '
            entity.modifier = entity.modifier[:-1]

            type_ctx = ctx.localVariableType()  # reach type of field
            var_ctx = ctx.variableDeclaratorList().getChild(0)  # reach variable info

            while type(type_ctx) is not TerminalNodeImpl:
                type_ctx = type_ctx.getChild(0)
            entity.type = type_ctx.getText()

            entity.name = var_ctx.getChild(0).getText()

            var_ctx = var_ctx.getChild(2)
            while type(var_ctx) is not TerminalNodeImpl:
                var_ctx = var_ctx.getChild(0)

            entity.value = var_ctx.getText()

            parent_method_ctx = ctx.parentCtx
            Utilities.findParentScope(parent_method_ctx, entity)

            self.est.append(entity)
        except Exception as e:
            print('Error in exitLocalVariableDeclaration:', e)
