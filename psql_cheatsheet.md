# PostgreSQL psql Cheat Sheet

A quick reference for working with PostgreSQL inside the `psql` terminal.

---

## 🔑 Basics
| Command | Description |
|---------|-------------|
| `\q` | Quit `psql` |
| `\?` | Show help on `psql` commands |
| `\l` | List all databases |
| `\c dbname` | Connect to a specific database |
| `\conninfo` | Show current connection info |

---

## 📊 Tables & Schema
| Command | Description |
|---------|-------------|
| `\dt` | List all tables in the current database |
| `\d tablename` | Show table structure (columns, types, constraints) |
| `\dn` | List schemas |
| `\df` | List functions |
| `\dv` | List views |

---

## 🔍 Data Queries
| Command                             | Description                                    |
| ----------------------------------- | ---------------------------------------------- |
| `SELECT * FROM tablename;`          | View all rows in a table                       |
| `SELECT column FROM tablename;`     | View one column                                |
| `SELECT * FROM tablename LIMIT 10;` | View first 10 rows                             |
| `\x`                                | Toggle expanded display (better for wide rows) |



## ⚡ Database Management
| Command | Description |
|---------|-------------|
| `\du` | List roles (users) |
| `\password username` | Change a user’s password |
| `\timing` | Show execution time for queries |

---

## 🧹 Debug / Maintenance
| Command | Description |
|---------|-------------|
| `\! clear` | Clear the terminal screen |
| `\! command` | Run a shell command without leaving `psql` |
| `\set VERBOSITY verbose` | Get more detailed error messages |

---

## 🐳 Docker + Compose Commands
| Command | Description |
|---------|-------------|
| `docker compose -f docker-compose.dev.yml exec db psql -U $DB_USER -d $DB_NAME` | Connect to Postgres inside the running `db` container |
| `docker compose -f docker-compose.dev.yml exec db psql -U postgres` | Connect as default `postgres` superuser |
| `docker compose -f docker-compose.dev.yml logs db` | View Postgres logs |
| `docker compose -f docker-compose.dev.yml restart db` | Restart the DB container |

---

## ✅ Most Useful for Dao of Life
- `\dt` → check if `news`, `event`, `posts` exist  
- `SELECT * FROM news;` → confirm your seed worked  
- `\q` → cleanly exit  

---
