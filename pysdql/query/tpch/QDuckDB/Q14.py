from pysdql.query.tpch.const import (LINEITEM_TYPE, PART_TYPE)

from pysdql.extlib.sdqlpy.sdql_lib import *


@sdql_compile({"li": LINEITEM_TYPE, "pa": PART_TYPE})
def query(li, pa):
    # Insert
    results = df_aggr_2.sum(lambda x: {x[0].concat(record({"promo_revenue": ((((100.0) * (x[0].sumcase_a))) / (x[0].suml_extendedprice1l_discount))})): x[1]})
    
    # Complete

    return results