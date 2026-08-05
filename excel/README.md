# Excel delivery contract

The Sprint 5 workbook will contain these sheets: `Dashboard`, `Portfolio`, `Funds`, `Stocks`, `Overlap`, `Forecast`, `Risk`, `Settings`, and `PowerQuery`.

The workbook will use parameterized Power Query sources aimed at the public API, with a named `Refresh Portfolio` action. Release assets are published through GitHub Releases and surfaced via `GET /excel`.

No spreadsheet is generated in Sprint 1: the system has no holdings data yet, and creating a populated-looking financial workbook before the source and calculation methodologies are agreed would be misleading.
