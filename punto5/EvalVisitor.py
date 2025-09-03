from ComplejoParser import ComplejoParser
from ComplejoVisitor import ComplejoVisitor

class EvalVisitor(ComplejoVisitor):

    def visitSuma(self, ctx: ComplejoParser.SumaContext):
        return self.visit(ctx.expr()) + self.visit(ctx.term())

    def visitResta(self, ctx: ComplejoParser.RestaContext):
        return self.visit(ctx.expr()) - self.visit(ctx.term())

    def visitMultiplicacion(self, ctx: ComplejoParser.MultiplicacionContext):
        return self.visit(ctx.term()) * self.visit(ctx.factor())

    def visitDivision(self, ctx: ComplejoParser.DivisionContext):
        return self.visit(ctx.term()) / self.visit(ctx.factor())

    def visitFactor(self, ctx: ComplejoParser.FactorContext):
        return self.visitChildren(ctx)

    def visitComplejo(self, ctx: ComplejoParser.ComplejoContext):
        texto = ctx.getText()
        texto = texto.replace("i", "j")  # Python usa j en lugar de i
        return complex(texto)

    def visitParentesis(self, ctx: ComplejoParser.ParentesisContext):
        return self.visit(ctx.expr())
