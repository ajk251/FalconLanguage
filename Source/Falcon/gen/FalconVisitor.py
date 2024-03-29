# Generated from /media/aaron/Shared2/School/BGSU-thesis/Source/Falcon/lang/Falcon.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FalconParser import FalconParser
else:
    from FalconParser import FalconParser

# This class defines a complete generic visitor for a parse tree produced by FalconParser.

class FalconVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FalconParser#block.
    def visitBlock(self, ctx:FalconParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#ns.
    def visitNs(self, ctx:FalconParser.NsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stmt.
    def visitStmt(self, ctx:FalconParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#assert_test.
    def visitAssert_test(self, ctx:FalconParser.Assert_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#test_basic.
    def visitTest_basic(self, ctx:FalconParser.Test_basicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#macro_basic.
    def visitMacro_basic(self, ctx:FalconParser.Macro_basicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#get_domain_name.
    def visitGet_domain_name(self, ctx:FalconParser.Get_domain_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#get_domain_names.
    def visitGet_domain_names(self, ctx:FalconParser.Get_domain_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_codeline.
    def visitStub_codeline(self, ctx:FalconParser.Stub_codelineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_p.
    def visitStub_p(self, ctx:FalconParser.Stub_pContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_pv.
    def visitStub_pv(self, ctx:FalconParser.Stub_pvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_many_pv.
    def visitStub_many_pv(self, ctx:FalconParser.Stub_many_pvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_assert.
    def visitStub_assert(self, ctx:FalconParser.Stub_assertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_assert_p.
    def visitStub_assert_p(self, ctx:FalconParser.Stub_assert_pContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_assert_logical.
    def visitStub_assert_logical(self, ctx:FalconParser.Stub_assert_logicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_assert_error.
    def visitStub_assert_error(self, ctx:FalconParser.Stub_assert_errorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_directives.
    def visitStub_directives(self, ctx:FalconParser.Stub_directivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_logical.
    def visitStub_logical(self, ctx:FalconParser.Stub_logicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_code.
    def visitStub_code(self, ctx:FalconParser.Stub_codeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_side_effect_many.
    def visitStub_side_effect_many(self, ctx:FalconParser.Stub_side_effect_manyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_side_effect.
    def visitStub_side_effect(self, ctx:FalconParser.Stub_side_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_fail_side_effect.
    def visitStub_fail_side_effect(self, ctx:FalconParser.Stub_fail_side_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_fail_side_effect_many.
    def visitStub_fail_side_effect_many(self, ctx:FalconParser.Stub_fail_side_effect_manyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_partition.
    def visitStub_partition(self, ctx:FalconParser.Stub_partitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_logic.
    def visitStub_logic(self, ctx:FalconParser.Stub_logicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_paren.
    def visitStub_paren(self, ctx:FalconParser.Stub_parenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#stub_logic_multi.
    def visitStub_logic_multi(self, ctx:FalconParser.Stub_logic_multiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#test_winnow.
    def visitTest_winnow(self, ctx:FalconParser.Test_winnowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#test_groupby.
    def visitTest_groupby(self, ctx:FalconParser.Test_groupbyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#test_satisfy.
    def visitTest_satisfy(self, ctx:FalconParser.Test_satisfyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#groupby_stub.
    def visitGroupby_stub(self, ctx:FalconParser.Groupby_stubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#groupby_stub_many.
    def visitGroupby_stub_many(self, ctx:FalconParser.Groupby_stub_manyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#groupby_stub_many_many.
    def visitGroupby_stub_many_many(self, ctx:FalconParser.Groupby_stub_many_manyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#groupby_code.
    def visitGroupby_code(self, ctx:FalconParser.Groupby_codeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#groupby_directives.
    def visitGroupby_directives(self, ctx:FalconParser.Groupby_directivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#winnow_stub_many_many.
    def visitWinnow_stub_many_many(self, ctx:FalconParser.Winnow_stub_many_manyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#winnow_stub_directives.
    def visitWinnow_stub_directives(self, ctx:FalconParser.Winnow_stub_directivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_domain.
    def visitMake_domain(self, ctx:FalconParser.Make_domainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_domain_args.
    def visitMake_domain_args(self, ctx:FalconParser.Make_domain_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#set_directive.
    def visitSet_directive(self, ctx:FalconParser.Set_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#set_single_directive.
    def visitSet_single_directive(self, ctx:FalconParser.Set_single_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_fn_directive.
    def visitMake_fn_directive(self, ctx:FalconParser.Make_fn_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_fn_flag_directive.
    def visitMake_fn_flag_directive(self, ctx:FalconParser.Make_fn_flag_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_codestmt.
    def visitMake_codestmt(self, ctx:FalconParser.Make_codestmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_codeblock.
    def visitMake_codeblock(self, ctx:FalconParser.Make_codeblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#assign_value.
    def visitAssign_value(self, ctx:FalconParser.Assign_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#assign_type_value.
    def visitAssign_type_value(self, ctx:FalconParser.Assign_type_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#args.
    def visitArgs(self, ctx:FalconParser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_list_c.
    def visitMake_list_c(self, ctx:FalconParser.Make_list_cContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_list.
    def visitMake_list(self, ctx:FalconParser.Make_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#name.
    def visitName(self, ctx:FalconParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#predicate.
    def visitPredicate(self, ctx:FalconParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#value.
    def visitValue(self, ctx:FalconParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_value.
    def visitMake_value(self, ctx:FalconParser.Make_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_name_value.
    def visitMake_name_value(self, ctx:FalconParser.Make_name_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_value_type.
    def visitMake_value_type(self, ctx:FalconParser.Make_value_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#make_name_type_value.
    def visitMake_name_type_value(self, ctx:FalconParser.Make_name_type_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FalconParser#dictate.
    def visitDictate(self, ctx:FalconParser.DictateContext):
        return self.visitChildren(ctx)



del FalconParser