from pydantic import BaseModel
from pydantic import Field


class PostgresExplain(BaseModel):
    class PostgresExplainPlan(BaseModel):
        class PostgresExplainPlanBuffer(BaseModel):
            hit: int | None = Field(None, alias="Shared Hit Blocks")
            read: int | None = Field(None, alias="Shared Read Blocks")
            write: int | None = Field(None, alias="Shared Written Blocks")

        type: str = Field(..., alias="Node Type")
        name: str | None = Field(None, alias="Relation Name")
        alias: str | None = Field(None, alias="Alias")
        startup: float | None = Field(None, alias="Startup Cost")
        total: float | None = Field(None, alias="Total Cost")

        plan_rows: int | None = Field(None, alias="Plan Rows")
        plan_width: int | None = Field(None, alias="Plan Width")

        actual_rows: int | None = Field(None, alias="Actual Rows")
        actual_loops: int | None = Field(None, alias="Actual Loops")
        actual_startup_time: float | None = Field(None, alias="Actual Startup Time")
        actual_total_time: float | None = Field(None, alias="Actual Total Time")

        buffers: PostgresExplainPlanBuffer | None = Field(None, alias="Buffers")
        plans: list["PostgresExplainPlan"] = Field(default_factory=list, alias="Plans")  # type:ignore

        filter: str | None = Field(None, alias="Filter")
        index: str | None = Field(None, alias="Index Cond")
        join: str | None = Field(None, alias="Join Type")

        class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True

    plan: PostgresExplainPlan = Field(..., alias="Plan")
    planning: float | None = Field(None, alias="Planning Time")
    execution: float | None = Field(None, alias="Execution Time")

    class Config:
        allow_population_by_field_name = True
