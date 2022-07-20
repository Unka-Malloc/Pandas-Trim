from pysdql.core.dtypes.ConditionalUnit import CondUnit
from pysdql.core.dtypes.ColumnExpr import ColExpr
from pysdql.core.dtypes.IsinExpr import IsinExpr
from pysdql.core.dtypes.ExtExpr import ExtExpr


class ColUnit:
    def __init__(self, relation, col_name: str):
        """
        ColUnit 在被创建的时候总是作为Relation的元素出现，因此必定存在IterExpr
        :param relation:
        :param col_name:
        """
        self.relation = relation
        self.name = col_name

    @property
    def year(self):
        return ExtExpr(col=self,
                       ext_func='Year')

    @property
    def month(self):
        return

    @property
    def day(self):
        return

    def new_expr(self, new_str) -> str:
        return f'{new_str}.{self.name}'

    @property
    def expr(self):
        return f'{self.relation.key}.{self.name}'

    def __repr__(self):
        return self.expr

    def __hash__(self):
        return hash((self.relation.iter_expr.key, self.name))

    def __lt__(self, other) -> CondUnit:
        """
        Less than
        :param other:
        :return:
        """
        if type(other) == str:
            other = f'"{other}"'
        isjoin = False
        if type(other) == ColUnit:
            isjoin = True
        return CondUnit(unit1=self, operator='<', unit2=other, isjoin=isjoin)
        # return f'{self.column} < {other}'

    def __le__(self, other) -> CondUnit:
        """
        Less than or Equal
        :param other:
        :return:
        """
        if type(other) == str:
            other = f'"{other}"'
        isjoin = False
        if type(other) == ColUnit:
            isjoin = True
        return CondUnit(unit1=self, operator='<=', unit2=other, isjoin=isjoin)
        # return f'{self.column} <= {other}'

    def __gt__(self, other) -> CondUnit:
        """
        Greater than
        :param other:
        :return:
        """
        if type(other) == str:
            other = f'"{other}"'
        isjoin = False
        if type(other) == ColUnit:
            isjoin = True
        return CondUnit(unit1=other, operator='<', unit2=self, isjoin=isjoin)
        # return f'{self.column} > {other}'

    def __ge__(self, other) -> CondUnit:
        """
        Greater than or Equal
        :param other:
        :return:
        """
        if type(other) == str:
            other = f'"{other}"'
        isjoin = False
        if type(other) == ColUnit:
            isjoin = True
        return CondUnit(unit1=other, operator='<=', unit2=self, isjoin=isjoin)
        # return f'{self.column} >= {other}'

    def __eq__(self, other) -> CondUnit:
        """
        Equal
        :param other:
        :return:
        """
        if type(other) == str:
            other = f'"{other}"'
        isjoin = False
        if type(other) == ColUnit:
            isjoin = True
        return CondUnit(unit1=self, operator='==', unit2=other, isjoin=isjoin)
        # return f'{self.column} == {other}'

    def __ne__(self, other) -> CondUnit:
        """
        Not equal
        :param other:
        :return:
        """
        if type(other) == str:
            other = f'"{other}"'
        isjoin = False
        if type(other) == ColUnit:
            isjoin = True
        return CondUnit(unit1=self, operator='!=', unit2=other, isjoin=isjoin)
        # return f'not ({self.column} == {other})'

    def __add__(self, other):
        return ColExpr(unit1=self, operator='+', unit2=other, inherit_from=self.relation)

    def __radd__(self, other):
        return ColExpr(unit1=other, operator='+', unit2=self, inherit_from=self.relation)

    def __sub__(self, other):
        return ColExpr(unit1=self, operator='-', unit2=other, inherit_from=self.relation)

    def __rsub__(self, other):
        return ColExpr(unit1=other, operator='-', unit2=self, inherit_from=self.relation)

    def __mul__(self, other):
        return ColExpr(unit1=self, operator='*', unit2=other, inherit_from=self.relation)

    def __rmul__(self, other):
        return ColExpr(unit1=other, operator='*', unit2=self, inherit_from=self.relation)

    def __truediv__(self, other):
        return ColExpr(unit1=self, operator='/', unit2=other, inherit_from=self.relation)

    def __rtruediv__(self, other):
        return ColExpr(unit1=other, operator='/', unit2=self, inherit_from=self.relation)

    def isin(self, vals, ext=None):
        if type(vals) == ColUnit:
            return IsinExpr(self, vals)

        if type(vals) == list or type(vals) == tuple:
            if len(vals) == 0:
                raise ValueError()
            if len(vals) == 1:
                return vals[0]

            tmp_list = []
            for i in vals:
                if type(i) == str:
                    i = f'"{i}"'
                if ext:
                    tmp_list.append(CondUnit(unit1=ext, operator='==', unit2=i))
                else:
                    tmp_list.append(CondUnit(unit1=self, operator='==', unit2=i))

            a = tmp_list.pop()
            b = tmp_list.pop()
            tmp_cond = a | b
            if tmp_list:
                for i in tmp_list:
                    tmp_cond |= i
            # print(tmp_cond)
            return tmp_cond

    @property
    def str(self):
        return self

    def startswith(self, pattern: str):
        return ExtExpr(self, 'StrStartsWith', pattern)

    def endswith(self, pattern: str):
        return ExtExpr(self, 'StrEndsWith', pattern)

    def contains(self, *args):
        return ExtExpr(self, 'StrContains', args)

    def not_contains(self, *args):
        return ExtExpr(self, 'not_StrContains', args)

    def substring(self, start, end):
        return ExtExpr(self, 'SubString', (start, end))