from pysdql.core.api import (
    # db_driver
    driver,

    # dtypes
    relation,
    CompoExpr,
    CondExpr,
    DictExpr,
    RecExpr,
    VarExpr,
    OpExpr,
    ConcatExpr,

    # data_loader
    read_tbl,
)
from pysdql.const import (
    PART_COLS,
    SUPPLIER_COLS,
    PARTSUPP_COLS,
    CUSTOMER_COLS,
    ORDERS_COLS,
    LINEITEM_COLS,
    NATION_COLS,
    REGION_COLS
)


def merge(*args, on=None, name=None, optimize=False):
    if name is None:
        name = 'R'

    ie_list = []
    ik_list = []
    iv_list = []
    op_list = []
    col_list = []
    icol_list = []

    for r in args:
        ie_list.append(str(r.iter_expr))
        ik_list.append(str(r.iter_expr.key))
        iv_list.append(str(r.iter_expr.val))
        icol_list.append(r.cols)
        col_list += r.cols
        op_list += r.operations

    iv_str = " * ".join(iv_list)

    if on:
        result = VarExpr(name, CompoExpr(ie_list, CondExpr(on, DictExpr({concat_cols(ik_list, icol_list): 1}), DictExpr({}))))
        op_list.append(OpExpr('pysdql_merge_on', result))
    else:
        result = VarExpr(name, CompoExpr(ie_list, DictExpr({concat_cols(ik_list, icol_list): 1})))
        op_list.append(OpExpr('pysdql_merge', result))

    return relation(name=name,
                    cols=col_list,
                    operations=op_list)


def concat(keys: list) -> str:
    keys.reverse()
    k1 = keys.pop()
    k2 = keys.pop()
    ce = ConcatExpr(rec1=k1, rec2=k2)
    keys.reverse()
    for k in keys:
        ce = ce.concat(k)
    return str(ce)


def concat_cols(keys: list, cols: list):
    cols_dict = dict(zip(keys, cols))
    tmp_dict = {}

    for k in cols_dict.keys():
        for c in cols_dict[k]:
            tmp_dict[f'{c}'] = f'{k}.{c}'

    return RecExpr(tmp_dict)

