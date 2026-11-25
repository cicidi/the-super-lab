# links — impl-plan (spec-ticket fixture for ARD-Q: links and anchors)

## IMPL-A — 读侧 store

Build the read store described in [the design](../design/links-design.md#cache).

**依赖：** 无。**挡住：** IMPL-B。

**Verify:** a read returns a cached row.

## IMPL-B — Write path (v2)

See [IMPL-A](#impl-a--读侧-store) and the [standard](../../../../skills/spec-organize/SPEC-STANDARD.md).

**依赖：** IMPL-A。**挡住：** 无。

**Verify:** a write invalidates the cache.
