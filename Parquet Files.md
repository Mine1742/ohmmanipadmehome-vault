# Apache Parquet

[[Data Analytics Hub]] | [[DP-600 Study Guide]]

Columnar storage file format used across Fabric (Lakehouse Delta tables are Parquet under the hood), Spark, Data Factory/Dataflow Gen2, Synapse, and most modern data lake tooling.

## Columnar vs. row-based

Row-based formats (CSV, JSON) store data one full record at a time — everything for row 1, then everything for row 2. Parquet stores data one **column** at a time — every value in column A, then every value in column B.

This matters because analytics queries almost never touch every column. `SELECT AVG(amount) FROM sales` only needs the `amount` column — a columnar engine reads just that column off disk and skips the rest. A row-based format has to read every row in full even though 9 of the 10 columns are irrelevant to the query.

## Why it's fast and small

- **Column pruning** — only the columns a query actually references get read from disk/network, which is most of the I/O savings.
- **Compression** — values within a single column tend to be similar (same data type, often repetitive or low-cardinality), so per-column compression ratios beat compressing a mixed row of different data types together. Typical Parquet files are 75-90% smaller than the equivalent CSV.
- **Predicate pushdown** — Parquet stores min/max statistics per column "chunk," so an engine can skip entire chunks that can't possibly match a `WHERE` filter without reading them at all.
- **Schema embedded in the file** — column names and data types travel with the data, unlike CSV where the schema has to be inferred or supplied separately.

## Where it shows up in Fabric

- **Delta Lake tables** (the default table format in a Fabric Lakehouse) are Parquet files plus a transaction log — this is why Lakehouse "tables" behave like a database but are really just folders of `.parquet` files.
- **Direct Lake mode** in Power BI reads Parquet/Delta files directly out of OneLake into the semantic model's memory format, skipping a separate import or DirectQuery step — this is only possible because Parquet's columnar layout is close enough to how the VertiPaq engine already wants the data.
- **Dataflow Gen2 / Data pipelines** commonly write intermediate and Silver/Gold outputs as Parquet or Delta rather than CSV, precisely to get compression and column pruning for downstream queries.

## Practical notes

- Parquet is a binary format — not human-readable by opening it in a text editor. Use `pandas.read_parquet()`, DuckDB, or a Fabric Lakehouse/notebook to inspect one.
- Individual Parquet files are typically written in a partitioned/sharded set (many `part-*.parquet` files under one folder) rather than as a single file, so Delta table "files" are really directories.
- Good fit: analytical/OLAP workloads (aggregations, wide scans, few columns per query). Poor fit: transactional/OLTP workloads (frequent single-row reads/writes) — that's still a job for row-based storage or a proper database engine.
