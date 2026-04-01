import enum


class Operator(enum.StrEnum):
    eq = "__eq__"
    ne = "__ne__"
    gt = "__gt__"
    gte = "__ge__"
    lt = "__lt__"
    lte = "__le__"
    in_ = "in_"
    int_ = "not_in"
    like = "like"
    between = "between"
    is_ = "is_"
    ist_ = "is_not"


class Direction(enum.StrEnum):
    asc = "asc"
    desc = "desc"
