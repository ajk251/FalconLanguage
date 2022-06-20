
import re
import runpy
import textwrap
import warnings

from collections import defaultdict
from datetime import datetime
from random import choices, randint
from string import ascii_letters, digits

from Falcon.algorithms.algorithms import ALGORITHMS
from Falcon.macros.macros import MACROS
from Falcon.predicates.predicates import PREDICATES
from Falcon.utilities.FalconError import FalconError

from Falcon import domains

from Falcon.writers.tools import *

tabsize: int = 4
TAB: str = ' ' * tabsize
nl: str = '\n'

# ⊻ ⊼ ⊽ ￫ these require special treatment…
booleans = {'∧': 'and', '&&': 'and', 'and': 'and',
            '∨': 'or', '||': 'or', 'or': 'or',
            '!': 'not', '¬': 'not', 'not': 'not'}

# writes the file -----------------------------------------


def write_basic_test(intermediate, source=None, destination=None):

    # intermediate is the tree, source & destination are the names of the i/o

    # indent: int = 0
    # nl = '\n'

    # file = intermediate['global']['directives'].setdefault('file', './test.py')
    # file = 'Tests/tests.py' if 'file' not in intermediate['global']['directives'] else intermediate['global']['directives']['file']

    # the file can be a directive, in the commandline args, or a default
    if 'file' in intermediate['global']['directives']:
        file = intermediate['global']['directives']
    elif 'file' in intermediate['global']['directives']:
        file = intermediate['global']['directives']['file']
    elif destination is not None:
        file = destination
    else:
        file = 'Tests/test_falcon_file.py'

    with open(file, 'w', encoding='utf-8') as falcon:

        # write the boilerplate stuff, that applies globally
        lines = make_initial(intermediate['initial'], source)
        falcon.write(lines)

        lines = make_global(intermediate['global'])
        falcon.write(lines)

        for block in intermediate['ordering']:

            kind, value = block

            if kind == 'code':
                line = code_block(value)
                falcon.write(line)
            elif kind == 'namespace':
                # lines = make_namespace(intermediate[value], value)
                # lines = make_unittest(intermediate[value], 0)
                # falcon.write(lines)
                lines = make_global(intermediate[value])
                falcon.write(lines)
            else:
                lines = make_global(intermediate[value])

            falcon.write(nl)

        # finally!
        falcon.write('')


def make_global(entry) -> str:

    indent: int = 0
    lines = []

    # directives -----
    desc = entry['directives'].get(':desc', None)

    if desc:
        lines.append(indent * TAB + '# ' + desc)

    for block in entry['ordering']:

        kind, value = block if len(block) == 2 else (block[0], block[1:])

        if kind == 'code':
            line = '\n' + code_block(value)
            lines.append(line)
        elif kind == 'assertion':
            line = basic_Assert(entry['tests'][value])
            lines.append(line)
        elif kind == 'domain':
            line = make_domain(value)
            lines.append(line)
        elif kind == 'test':
            if entry['tests'][value]['kind'] == 'test-basic':
                line = basic_Test(entry['tests'][value])
                lines.append(line)
            # elif entry['tests'][value]['kind'] == 'winnow-test':
            elif entry['tests'][value]['kind'] == 'groupby-test':
                # line = basic_Winnow(entry['tests'][value], indent)
                # line = basic_Groupby(entry['tests'][value])
                line = basic_Groupby2(entry['tests'][value])
                lines.append(line)
            elif entry['tests'][value]['kind'] == 'winnow-test':
                line = basic_Winnow2(entry['tests'][value])
                lines.append(line)
            elif entry['tests'][value]['kind'] == 'satisfy-test':
                line = basic_Satisfy2(entry['tests'][value])
                lines.append(line)
            elif entry['tests'][value]['kind'] == 'macro':
                line = basic_macros(entry['tests'][value])
                lines.append(line)

    return '\n'.join(lines)


# testers --------------
def basic_macros(entry) -> str:

    name = entry['name']

    if MACROS.get(name, False):
        lines = MACROS[name][0](entry)
    else:
        raise FalconError(f'{name} is not a Falcon function or macro')

    return '\n'.join(lines)


def basic_Test(entry) -> str:

    # Test - a for-loop over some domain with n predicates

    indent: int = 0

    directives = get_directives(entry)

    message = directives['message']
    pyfunc = directives['pyfunc']
    dvars = entry['domain']                                         # the domain names
    labels = directives['labels']
    algo = directives['algo']
    params = directives['params']
    fn_name = directives['fn_name']
    obj_update = directives['object-update']

    # write tests ------
    lines = ['\n# start test -----------------', pyfunc, '']
    indent += 1

    if message:
        line = indent * TAB + '# ' + message.strip('"') + nl
        lines.append(line)

    # build the for loop, naked/with custom iterator/generic & no parameters
    if len(dvars) == 1:
        # note dvars is the number of domains, labels can be user-defined number to unpack
        template = indent * TAB + "for {} in {}:".format(','.join(labels), dvars[0])
    elif len(params) > 0:
        template = indent * TAB + 'for {} in {}({}, {}):'.format(', '.join(labels), algo, ', '.join(dvars), ', '.join(params))
    else:
        template = indent * TAB + "for {} in {}({}):".format(', '.join(labels), algo, ', '.join(dvars))

    lines.append(template)

    # fn_name = entry['function']
    args = ', '.join(labels)

    indent += 1

    for stub in entry['stubs']:
        stmt = make_assert_stmt(stub, fn_name, args)
        lines.append((indent * TAB) + stmt)

    lines.append('')

    if obj_update:
        # test_case = ', '.join(str(arg) for arg in args)
        for domain in entry['domain']:
            line = indent * TAB + domain + "()"
            lines.append(line)

    # indent -= 1

    return '\n'.join(lines)


def basic_Assert(entry) -> str:

    # n predicates

    # TODO:
    #   add directive for value = … \ assert predicate(value, args)...
    #   handle messages, ie assert …, <message>
    #   extra args!!! raise error!
    #   add explanations

    # directives -------------

    indent: int = 0
    ignore_true = True          # this was an earlier attempt, eg is-int? True, TODO: refactor out

    # because assert is different, it can't use get_directives - it doesn't have the function & domain
    # message, pyfunc,

    # get the message, if any
    if entry['directives'].get(':message', None) is not None:
        message = entry['directives'][':message']['value']
    else:
        message = None

    # get the name of the function, create one, or append one
    # test-name ￫ user name, as-is. :name any name, but decorated

    fn_name = entry['function']

    if entry['directives'].get(':test-name', None):
        # TODO: raise warning if it does not start with test
        t_name = entry['directives'][':test-name']['value']
        pyfunc = f'def {t_name}():'
    elif entry['directives'].get(':name', None):
        t_name = entry['directives'][':name']['value']
        pyfunc = f'def {t_name}():' if t_name.startswith('test') else f'def test_{t_name}():'

    else:
        rand_name = ''.join((choices(ascii_letters+digits, k=randint(2, 5))))
        pyfunc = f'def test_{fn_name}_assertions_{rand_name}():' #.format(fn_name, rand_name)

    indent += 1

    # -----------------------
    a1 = 'assert {} {} {}'              # w/ symbol
    a2 = 'assert {}({}, {})'            # w/ function
    a3 = 'assert {}({})'                # ignoring True

    # -----------------------
    lines = ['', pyfunc + '\n']

    if message:
        lines.append((TAB * indent) + '# ' + message.strip('"'))

    # fn_name = entry['function']

    for stub in entry['stubs']:

        if stub['kind'] == 'code':
            lines.append((TAB * indent) + stub['value'])
            continue

        # print(get_predicate(stub, False))

        # this is kind of a special case/after-thought
        if stub.get('predicate', False) and PREDICATES[stub['predicate']].is_symbolic:
            # these must raise an error, ie catches(fn, args, Exception)
            pd_name = PREDICATES[stub['predicate']].name
            args = make_args(stub['argument'])
            line = f"{indent * TAB}assert {pd_name}({fn_name}, {args}"
            line += f", {', '.join(s for s in stub['value'][1:] if s is not None)})" if len(stub['value']) > 1 else ')'
            lines.append(line)
            continue
        elif stub['kind'] == 'assert-logical':
            # logical conditions
            args = make_args(stub['argument']).strip('(').strip(')')
            line = (indent * TAB) + make_assert_stmt(stub, fn_name, args)
            lines.append(line)
            continue
        elif stub['kind'] == 'assert-error':
            # error stubs
            if len(stub['value']) > 2:
                stub['kind'] = 'assert-error+'
            args = make_args(stub['argument']).strip('(').strip(')')
            line = (indent * TAB) + make_assert_stmt(stub, fn_name, args)
            lines.append(line)
            continue

        args = make_args(stub['argument'])
        fn = fn_name + args
        value = stub['value'][1:]

        # print(get_predicate(stub, False), stub['value'])

        if PREDICATES[stub['predicate']].is_symbolic:
            # the symbolic representation
            pd_name = PREDICATES[stub['predicate']].symbol
            line = a1.format(fn, pd_name, value)
        else:
            # print(get_predicate(stub, False), stub['value'])
            pd_name = PREDICATES[stub['predicate']].name

            if ignore_true and value == 'True':
                line = a3.format(pd_name, fn)
            elif stub['kind'] == 'logical':
                line = make_assert_stmt(stub, fn_name, args, just_result=False)
                # stmt = make_assert_stmt(stub, fn_name, args)
                # print(stmt)
            elif len(value) > 2:
                # more than 1 value in predicate args
                v = ', '.join(v for v in value[1:])
                line = f"assert {pd_name}({fn_name}{args}, {v})"
                # line = a2.format(pd_name, fn_name, ', '.join((v for v in value[1:])))
            else:
                # print(get_predicate(stub, False), stub['value'])
                line = a2.format(pd_name, fn, ', '.join(value))

        if 'error-message' in stub and stub['error-message'] is not None:
            line += f", {stub['error-message']}"

        # line = (TAB * indent) + line
        lines.append((TAB * indent) + line)

    lines.append('')        # add a blank line

    return '\n'.join(lines)


def basic_Groupby2(entry) -> str:

    # groupby - predicates must hold for every group member, n groups, m predicates

    indent: int = 0
    lines = ['']

    directives = get_directives(entry)

    # message = directives['message']
    pyfunc = directives['pyfunc']
    dvars = entry['domain']                                         # the domain names
    labels = directives['labels']
    algo = directives['algo']
    params = directives['params']
    fn_name = directives['fn_name']
    followup = directives['follow-up']

    save_results = True if entry.get(':save-results', False) else False
    save_groups = True if entry.get(':save-cases', False) else False

    args = ', '.join(labels)
    fn_sig = '{}({})'.format(fn_name, args)

    # the def name
    lines.extend((f'{pyfunc}', ''))

#     # w1 has a separate bin function defined
#     w1 = '''
# try:
#     result = {}
# except Exception as e:
#     result = e
#
# try:
#     group = {}(result)
# except Exception as e:
#     raise FalconError('Failed to properly partition the function')
#     '''

    w2 = '''
try:
    result = {}
except Exception as e:
    result = e
'''

    indent += 1

    if save_groups:
        line = (indent * TAB) + 'groups = defaultdict(list)'
        lines.append(line)
    if save_results:
        line = (indent * TAB) + 'results = defaultdict(list)\n'
        lines.append(line)

    # build the for loop, naked/with custom iterator/generic & no parameters
    if len(labels) == 1:
        template = indent * TAB + "for {} in {}:".format(labels[0], dvars[0])
    elif len(params) > 0:
        template = indent * TAB + 'for {} in {}({}, {}):'.format(', '.join(labels), algo, ', '.join(dvars), ', '.join(params))
    else:
        template = indent * TAB + "for {} in {}({}):".format(', '.join(labels), algo, ', '.join(dvars))

    lines.append(template)

    # build the template
    line = textwrap.indent(w2.format(fn_sig, entry['bin'], ', '.join(labels)), TAB * 2)
    lines.append(line)
    using_bin_fn = False

    # =========================================

    # collected all the groups {name: stub...}
    groups = defaultdict(list)

    for stub in entry['stubs']:
        groups[stub['group']].append(stub)

    groups = tuple(groups.items())      # flatten
    agg_groups = []                     # the groups that have aggregated ops on them
    labels = ', '.join(labels)

    cond = 'if'         # rather than have if if, if elif, ...

    indent += 1

    for group, stub in groups:

        # the if statement
        if len(stub) > 1:
            names = []
            for s in stub:
                # just the predicates, no values
                predicate, _ = get_predicate(s, by_group=False)
                text = f"{predicate.name}({labels})"
                names.append(text)
            line = f"{indent * TAB}{cond} {' or '.join(names)}:\n"
        else:
            predicate, values = get_predicate(stub[0], by_group=False)
            line = f"{indent * TAB}{cond} {predicate.name}({labels}):\n"

        cond = 'elif'

        # the sub-parts is there a group-predicate test & by-value/by-all
        gpredicate, gvalues = get_predicate(stub[0], by_group=True)
        indent += 1

        # the first two go at the end
        if gpredicate.is_group and gvalues is not None:
            gline = f"{indent * TAB}assert {gpredicate.name}(results[{group}], {', '.join(gvalues)})"
            agg_groups.append(gline)
        elif gpredicate.is_group:
            gline = f"{indent * TAB}assert {gpredicate.name}(results[{group}])"
            agg_groups.append(gline)
        if gpredicate.is_group or gpredicate is None:
            line += ''
        elif gvalues is not None:
            line += f"{indent * TAB}assert {gpredicate.name}(result, {', '.join(gvalues)})"
        else:
            line += f"{indent * TAB}assert {gpredicate.name}(result)"

        #

        # save if necessary
        if save_groups:
            line +=  f'\n{indent * TAB}groups[{groups[0][0]}].append({labels})'
        if save_results:
            line += f'\n{indent * TAB}results[{groups[0][0]}].append(result)'

        lines.append(line)
        indent -= 1

    # add the last group
    line = f"{indent * TAB}else:\n{(indent + 1) * TAB}raise FalconError('Failed to meet at least one group')"
    lines.append(line)
    lines.append('')

    # add the aggregate group operations
    lines.extend(agg_groups)

    # ==========================================

    # # deal with the groups
    # groups = defaultdict(list)
    # gb_groups = {}
    # group_predictes = {}
    #
    # # TODO: This needs work... need a separate function for all the cases & error handling...
    # # TODO: - The commented out code is for the group assert? Is it necessary?
    # #       -> fix it with a directive
    #
    # for stub in entry['stubs']:
    #
    #     stub['using-bin-fn'] = using_bin_fn
    #     stmt = make_if_group_stmt(stub, fn_name, args)
    #     groups[stub['group']].append(stmt)
    #
    #     if stub['kind'] == 'groupby-many-with-group':
    #         gb_groups[stub['group']] = (stub['group-predicate'], stub['group-values'])
    #
    #     if stub.get('group-predicate', False):
    #         group_predictes[stub['group']] = (stub['group-predicate'], stub['group-values'])
    #     else:
    #         group_predictes[stub['group']] = (None, None)
    #
    # # assert len(groups) > 1, "the number of groups must be greater than 1"
    #
    # indent += 1
    # groups = tuple(groups.items())
    #
    # # the first statement is an 'if'
    # cond = ' or '.join((predicate for predicate in groups[0][1])) if len(groups[0][1]) > 1 else groups[0][1][0]
    # case = '(' + ', '.join((lbl for lbl in labels)) + ')' if len(labels) > 1 else f'({labels[0]},)'
    # line = f'{indent * TAB}if {cond}:'
    #
    # # TODO: check that the first one is not a group predicate!!!
    #
    # if stub['kind'] == 'groupby-many-with-group':
    #     group = groups[0][0]
    #     pd = PREDICATES.get(gb_groups[group][0], (None, None, None, None))
    #     line += f'\n{(indent + 1) * TAB}assert {pd[0]}(result)'
    #
    # # line += f'\n{(indent + 1) * TAB}groups[{groups[0][0]}].append((result, {case}))'
    # line +=  f'\n{(indent + 1) * TAB}groups[{groups[0][0]}].append({case})'
    # line += f'\n{(indent + 1) * TAB}results[{groups[0][0]}].append(result)'
    #
    # lines.append(line)
    #
    # for group, stmts in groups[1:]:
    #
    #     # note: group is (name, args ∨ [])
    #
    #     cond = ' or '.join((predicate for predicate in stmts)) if len(stmts) > 1 else stmts[0]
    #     line = f'{indent * TAB}elif {cond}:'
    #
    #     # check what kind of predicate should be applied & valid & stuff
    #     if stub['kind'] == 'groupby-many-with-group':
    #
    #         pd = PREDICATES.get(gb_groups[group][0], (None, None, None, None))
    #
    #         if len(stub['group-values']) > 0:
    #             # print(stub['group-values'], len(stub['group-values']))
    #             args = ', '.join(stub['group-values'])
    #         else:
    #             args = None
    #
    #         # print('args ', args, group, group_predictes[group])
    #
    #         # if it is a group predicate or has no name, skip it
    #         if pd.is_group or pd[0] is None:
    #             line += ''                      # do nothing...
    #         elif args is not None:
    #             # print('has args ', args, type(args))
    #             line += f'\n{(indent + 1) * TAB}assert {pd.name}(result, {args})'
    #         else: # elif PREDICATES.get(pd.name, False):
    #             line += f'\n{(indent + 1) * TAB}assert {pd.name}(result)'
    #
    #     line += f'\n{(indent + 1) * TAB}groups[{group}].append({case})'
    #     line += f'\n{(indent + 1) * TAB}results[{group}].append(result)'
    #     lines.append(line)

    # line = f"{indent * TAB}else:\n{(indent + 1) * TAB}FalconError('Failed to meet at least one group')"
    # lines.append(line)
    #
    # # this might need to be optional
    # lines.append('')
    #
    # # # add group assert statements
    # for group, pd in group_predictes.items():
    #
    #     if pd[0] is None: continue
    #
    #     if grp_pd := PREDICATES.get(pd[0], False):
    #         pd_name = grp_pd[0]
    #     else:
    #         # raise FalconError(f"Predicate {pd[0]} not found"
    #         warnings.warn(f"Predicate {pd[0]} not found")
    #
    #     # write the group assert statement, if it is a group-predicate
    #     if not grp_pd[3]:
    #         continue
    #     if pd[1] == []:
    #         line = f'{indent * TAB}assert {pd_name}(results[{group}])'
    #     else:
    #         line = f"{indent * TAB}assert {pd_name}(results[{group}], {', '.join(pd[1])})"
    #
    #     lines.append(line)

    indent -= 1

    if followup and save_results:
        line = f'\n{indent * TAB}{followup}(results)'
        lines.append(line)
    elif followup and save_groups:
        line = f'\n{indent * TAB}{followup}(groups)'
        lines.append(line)
    elif followup and save_groups and save_results:
        line = f'\n{indent * TAB}{followup}(groups, results)'
        lines.append(line)

    lines.append('')

    return '\n'.join(lines)


def basic_Winnow(entry) -> str:

    # winnow - predicates must hold for every group member, n groups, m predicates
    #        - predicates must hold for each group

    indent: int = 0
    lines = ['']

    directives = get_directives(entry)

    # message = directives['message']
    # pyfunc = directives['pyfunc']
    dvars = entry['domain']                                         # the domain names
    labels = directives['labels']
    algo = directives['algo']
    params = directives['params']
    fn_name = directives['fn_name']

    args = ', '.join(labels)
    fn_sig = '{}({})'.format(fn_name, args)

    # the def name
    lines.extend((f'def test_groupby_{fn_name}():', ''))

    # w1 has a separate bin function defined
    w1 = '''
try:
    result = {}
except Exception as e:
    result = e
                
try:
    group = {}(result)
except Exception as e:
    raise FalconError('Failed to properly partition the function')
    '''

    w2 = '''
try:
    group = {}
except Exception as e:   
    raise FalconError('Failed to properly partition the function')
'''

    indent += 1

    # build the for loop, naked/with custom iterator/generic & no parameters
    if len(labels) == 1:
        template = indent * TAB + "for {} in {}:".format(labels[0], dvars[0])
    elif len(params) > 0:
        template = indent * TAB + 'for {} in {}({}, {}):'.format(', '.join(labels), algo, ', '.join(dvars), ', '.join(params))
    else:
        template = indent * TAB + "for {} in {}({}):".format(', '.join(labels), algo, ', '.join(dvars))

    lines.append(template)

    # build the template
    if entry['bin'] is not None:
        line = textwrap.indent(w1.format(fn_sig, entry['bin']), TAB * 2)
        lines.append(line)
        using_bin_fn = True
    else:
        line = textwrap.indent(w2.format(fn_sig), TAB * 2)
        lines.append(line)
        using_bin_fn = False

    # deal with the groups
    groups = defaultdict(list)

    for stub in entry['stubs']:

        stub['using-bin-fn'] = using_bin_fn

        # if using_bin_fn:
        stmt = make_assert_group_stmt(stub, fn_name, args)
        # else:
        #     stmt = make_assert_stmt(stub, fn_name, args, indent)

        groups[stub['group']].append(stmt)

    # assert len(groups) > 1, "the number of groups must be greater than 1"

    indent += 1

    groups = tuple(groups.items())

    # first one is a special case, ie 'if'
    line = (indent * TAB) + f'if group == {groups[0][0]}:\n' + ((indent + 1) * TAB) + '\n'.join(groups[0][1])
    lines.append(line)

    # TODO: if there are multiple statements, this will fail.

    for group, stmt in groups[1:]:
        line = (indent * TAB) + f'elif group == {group}:\n' + ((indent + 1) * TAB) + '\n'.join(stmt)
        lines.append(line)

    # add failure case
    failure = (indent * TAB) + f'else:\n' + ((indent + 1) * TAB) + 'raise FalconError("Failed to meet at least one group") \t\t# TODO…'
    lines.append(failure)

    lines.append('')

    return '\n'.join(lines)


def basic_Winnow2(entry) -> str:

    # winnow - predicates must hold for every group member, n groups, m predicates

    indent: int = 0
    lines = ['']

    directives = get_directives(entry)

    # message = directives['message']
    # pyfunc = directives['pyfunc']
    dvars = entry['domain']                                         # the domain names
    labels = directives['labels']
    algo = directives['algo']
    params = directives['params']
    fn_name = directives['fn_name']
    followup = directives['follow-up']

    # these are for the log
    use_log = directives['use-log']
    log_name = directives['log-name']

    # these are the minimum and maximum number of predicates that should be meet.
    if entry['directives'].get(':min', False):
        minimum = entry['directives'][':min']['value']
    else:
        minimum = 1

    if entry['directives'].get(':max', False):
        maximum = entry['directives'][':max']['value']
    else:
        maximum = None

    args = ', '.join(labels)
    fn_sig = '{}({})'.format(fn_name, args)

    # the def name
    lines.extend((f'def test_winnow_{fn_name}():', ''))

#     # w1 has a separate bin function defined
#     w1 = '''
# try:
#     result = {}
# except Exception as e:
#     result = e
#
# try:
#     group = {}(result)
# except Exception as e:
#     raise FalconError('Failed to properly partition the function')
#     '''

    w2 = '''
try:
    result = {}
except Exception as e:
    result = e
'''

    indent += 1

    line = (indent * TAB) + 'groups = defaultdict(list)\n'
    lines.append(line)

    # build the for loop, naked/with custom iterator/generic & no parameters
    if len(labels) == 1:
        template = indent * TAB + "for {} in {}:".format(labels[0], dvars[0])
    elif len(params) > 0:
        template = indent * TAB + 'for {} in {}({}, {}):'.format(', '.join(labels), algo, ', '.join(dvars), ', '.join(params))
    else:
        template = indent * TAB + "for {} in {}({}):".format(', '.join(labels), algo, ', '.join(dvars))

    lines.append(template)

    # build the template
    line = textwrap.indent(w2.format(fn_sig, entry['bin'], ', '.join(labels)), TAB * 2)
    lines.append(line)
    using_bin_fn = False

    # deal with the groups
    groups = defaultdict(list)

    for stub in entry['stubs']:

        stub['using-bin-fn'] = using_bin_fn
        stmt = make_if_group_stmt(stub, fn_name, args)
        groups[stub['group']].append(stmt)

    # assert len(groups) > 1, "the number of groups must be greater than 1"

    indent += 1
    groups = tuple(groups.items())

    # the first statement is an 'if'
    # cond = ' or '.join((predicate for predicate in groups[0][1])) if len(groups[0][1]) > 1 else groups[0][1][0]
    # case = '(' + ', '.join((lbl for lbl in labels)) + ')' if len(labels) > 1 else f'({labels[0]},)'
    # line = f'{indent * TAB}if {cond}:\n{(indent + 1) * TAB}groups[{groups[0][0]}].append((result, {case}))'
    # lines.append(line)

    case = '(' + ', '.join((lbl for lbl in labels)) + ')' if len(labels) > 1 else f'({labels[0]},)'

    for group, stmts in groups:
        cond = ' or '.join((predicate for predicate in stmts)) if len(stmts) > 1 else stmts[0]
        line = f'{indent * TAB}if {cond}:\n{(indent + 1) * TAB}groups[{group}].append((result, {case}))'
        lines.append(line)

    lines.append('')

    # deal with the group predicates
    for stub in entry['stubs']:

        if (stub['kind'].startswith('predicate')) and (stub.get('predicate', '') not in PREDICATES):
            raise FalconError(f'Predicate "{stub["predicate"]}" not found')

        pd = PREDICATES[stub['group-predicate']][0]
        stmt = f"{indent * TAB}assert {pd}(groups[{stub['group']}], {', '.join(stub['group-values'])})"

        lines.append(stmt)

    # add an 'if not captured…'
    if use_log:
        line = '\n' + (indent * TAB) + 'if count == 0:\n' + ((indent+1) * TAB) + 'oracles["random-test"].append((({}), repr(result)))'.format(', '.join(labels))
        lines.append(line)

    lines.append('')

    line = f'{(indent * TAB)}assert count <= {minimum}, f"The minimum number of predicates has not been met - met: {{count}}, min: {minimum}"'
    lines.append(line)

    if maximum is not None:
        line = (indent * TAB) + f'assert count > {maximum}, f"Exceed number of predicates met - met: {{count}}, max: {maximum}"'
        lines.append(line)

    if followup:
        line = f'\n{indent * TAB}{followup}(groups)'
        lines.append(line)

    indent -= 1

    lines.append('')

    return '\n'.join(lines)


def basic_Satisfy2(entry):

    # at least 1 or more predicates must be true
    indent: int = 0
    directives = get_directives(entry)

    message = directives['message']
    pyfunc = directives['pyfunc']
    dvars = entry['domain']                                         # the domain names
    labels = directives['labels']
    algo = directives['algo']
    params = directives['params']
    fn_name = directives['fn_name']

    # these are for the log
    use_log = directives['use-log']
    log_name = directives['log-name']

    # these are the minimum and maximum number of predicates that should be meet.
    if entry['directives'].get(':min', False):
        minimum = entry['directives'][':min']['value']
    else:
        minimum = 1

    if entry['directives'].get(':max', False):
        maximum = entry['directives'][':max']['value']
    else:
        maximum = None

    # write tests ------
    lines = ['', pyfunc, '']
    indent += 1

    if message:
        line = indent * TAB + '# ' + message.strip('"') + nl
        lines.append(line)

    # lines.append((indent * TAB + 'errors = []\n'))
    if use_log:
        lines.append((indent * TAB + 'oracles = defaultdict(list)\n'))

    # build the for loop, naked/with custom iterator/generic & no parameters
    if len(dvars) == 1:
        template = indent * TAB + "for {} in {}:".format(','.join(labels), dvars[0])
    elif len(params) > 0:
        template = indent * TAB + 'for {} in {}({}, {}):'.format(', '.join(labels), algo, ', '.join(dvars), ', '.join(params))
    else:
        template = indent * TAB + "for {} in {}({}):".format(', '.join(labels), algo, ', '.join(dvars))

    lines.append(template)

    args = ', '.join(labels)
    fn_sig = '{}({})'.format(fn_name, args)

    header = f"""
try:
    result = {fn_sig}
except Exception as error:
    result = error

count = 0
"""

    # has_error = True    -> this was on the code, removing it...

    # line = textwrap.indent(header.format(fn_sig), TAB * 2)
    line = textwrap.indent(header, TAB * 2)
    lines.append(line)

    indent += 1

    for stub in entry['stubs']:

        # the actual test assertion
        stmt = make_assert_stmt(stub, 'result', None, True)

        if stub['kind'].startswith('predicate'):

            # this is cheating and bad form
            #remove the left
            test = stmt.lstrip('assert').lstrip()           # otherwise a weird bug with result < 4 --> sult < 4

            #remove the right, if needed
            if stub['error-message'] is not None:
                test = test.rstrip(', ' + stub['error-message'])

            lines.append((indent * TAB) + 'if ' + test + ':')
            lines.append(((indent+1) * TAB) + 'count += 1')

            if use_log:
                lines.append(((indent+1) * TAB) + f"oracles['{stub['predicate']}'].append((({', '.join(labels)}), repr(result)))")

            # lines.append(((indent+1) * TAB) + stmt)

            # # assume that the error has been caught
            # if PREDICATES[stub['predicate']][2]:
            #     lines.append(((indent+1) * TAB) + 'has_error = False')
        elif stub['kind'] == 'code':
            line = '\n' + (indent * TAB) + stub['value'] + '\n'
            lines.append(line)

    # finish    part of the has_error stuff
    # line = '\n' + (indent * TAB) + 'if has_error:\n' + ((indent+1) * TAB) + 'errors.append((({}), result))'.format(', '.join(labels))
    # lines.append(line)
    # lines.append('')

    # add an 'if not captured…'
    if use_log:
        line = '\n' + (indent * TAB) + 'if count == 0:\n' + ((indent+1) * TAB) + 'oracles["random-test"].append((({}), repr(result)))'.format(', '.join(labels))
        lines.append(line)

    lines.append('')

    line = (indent * TAB) + f'assert count >= {minimum}, f"The minimum number of predicates has not been met - met: {{count}}, min: {minimum}  [with {{result}}]"'
    lines.append(line)

    if maximum is not None:
        line = (indent * TAB) + f'assert count > {maximum}, f"Exceed number of predicates met - met: {{count}}, max: {maximum}"'
        lines.append(line)

    # this doesn't work...
    # line = (indent * TAB) + f'assert len(errors) == 0, f"Unaccounted for errors - {{len(errors)}} errors occurred"'
    # lines.append(line)

    indent -= 1         # out of the for-loop

    if use_log:
        logname = "./FalconTestLog.txt" if not log_name else log_name
        line = '\n' + (indent * TAB) + f'write_to_log("{logname}", {{"name": {fn_name}, "predicates": oracles}})'
        lines.append(line)

    lines.append('')

    return '\n'.join(lines)