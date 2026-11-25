# basic — impl-plan (spec-ticket fixture)

## IMPL-A — Schema first

Create the table.

**依赖：** 无。**挡住：** IMPL-B、IMPL-C。

**Verify:** the table exists.

## IMPL-B — Read API

**依赖：** IMPL-A。**挡住：** IMPL-D。

**Verify:** GET returns rows.

## IMPL-C — Write API

C's dependency on A is stated only on A's side (one-sided edge, must be reported).

**依赖：** 无。**挡住：** IMPL-D。

**Verify:** POST stores a row.

## IMPL-D — UI page

**依赖：** IMPL-B、IMPL-C。**挡住：** 无。

**Verify:** the page lists and adds rows.
