# Wisho - Japanese Dictionary Backend

Backend for a Japanese-English dictionary application (inspired by jisho.org), with a JMdict parser included.

## About JMdict

**JMdict** is a multilingual Japanese-English dictionary database maintained by the [Electronic Dictionary Research and Development Group](https://www.edrdg.org/).

**File Format**: Large XML file (~150MB uncompressed) with a DTD that defines entity shortcuts for part-of-speech tags and other metadata. Example structure:

```xml
<!DOCTYPE JMdict [
<!ENTITY n "n">        <!-- noun -->
<!ENTITY v5u "v5u">    <!-- verb type -->
]>
<JMdict>
  <entry>
    <ent_seq>1206730</ent_seq>           <!-- unique ID -->
    <k_ele><keb>学校</keb></k_ele>        <!-- kanji form -->
    <r_ele><reb>がっこう</reb></r_ele>    <!-- reading (kana) -->
    <sense><pos>&n;</pos><gloss>school</gloss></sense>
  </entry>
</JMdict>
```

**Parser Requirements**: Must use `load_dtd=True, resolve_entities=True` with lxml to handle entity resolution. Without DTD loading, entities like `&n;` won't be resolved.

**How This Project Uses It**:

1. Parse XML entries into immutable DTOs for validation
2. Normalize into a lighter relational SQL schema (removes XML verbosity, optimizes for queries)
3. Entry IDs (`<ent_seq>`) become primary keys (no auto-increment)
4. Reading restrictions (`<re_restr>`) map to valid kanji-reading pairs
5. Priority tags (`<ke_pri>`, `<re_pri>`) unified in single `EntryPriority` table

## Project Architecture

**Data Flow**: JMdict XML → Parser → DTOs → Database Seeder → PostgreSQL

1. **Parser** (`src/wisho/jmdict/parser.py`): Uses lxml to parse JMdict_e XML with DTD resolution
2. **DTOs** (`src/wisho/jmdict/dto.py`): Immutable Pydantic models with validation (frozen=True)
3. **Seeder** (`src/wisho/db/seed.py`): Maps DTOs to SQLAlchemy ORM models
4. **Models** (`src/wisho/db/jmdict.py`): SQLAlchemy 2.0 declarative models with `Mapped[T]` annotations

**Key Pattern**: Always call `session.flush()` after adding parent records to get auto-generated IDs before creating children. See all 4 flush calls in `src/wisho/db/seed.py`.

## Setup Commands

```bash
# Install dependencies (uses uv package manager)
uv sync

# Start PostgreSQL container
docker compose up -d

# Access database shell
docker compose exec db psql -U wisho -d wisho_db

# Run database seeding (parses entire JMdict_e file)
uv run -m wisho.db
```

## Database Schema

Normalized relational model in `src/wisho/db/jmdict.py`:

- `Entry`: Root table, ID is JMdict `<ent_seq>` (not auto-increment)
- `Kanji`, `Reading`: One-to-many children with text and priorities
- `EntryPriority`: Unified frequency table using XOR constraint (either `kanji_id` OR `reading_id`, never both)
- `Sense`: Ordered meanings with `Gloss` translations and `SensePOS` part-of-speech tags
- `ReadingRestriction`: Valid reading-kanji pairs from `<re_restr>`

## Migrations

**Tool**: Monotome (template-based SQL migrations)  
**Location**: `src/migrations/` with one directory per table  
**Pattern**: Files use `__SCHEMA__` placeholder, declare dependencies via `--- requires: <table>/<file>.sql` comments

**Apply migrations**:

```bash
cd src/migrations
uv run monotome apply postgresql+psycopg://wisho:wisho@localhost:5432/wisho_db
```

**Check migration status**:

```bash
cd src/migrations
uv run monotome status postgresql+psycopg://wisho:wisho@localhost:5432/wisho_db
```

**To add a new table**:

1. Create directory in `src/migrations/<table_name>/`
2. Add `01-table.sql` with CREATE TABLE statement
3. Declare parent table dependencies at top of file

## Testing

**Run all tests**:

```bash
uv run pytest
```

**Test data**: `src/tests/data/jmdicte_samples.xml` (small XML samples for parsing tests)

**This project follows TDD (Test-Driven Development)**:

- Always run existing tests when making changes to ensure nothing breaks
- Add new unit tests when working on untested features

## Code Conventions

**Linting**: Ruff with strict rules (see `pyproject.toml`)

- Mandatory type hints (`ANN`)
- Security checks (`S`)
- Pathlib over os.path (`PTH`)
- Line length: 120 characters
- Double quotes for strings

**Before committing**:

```bash
ruff format     # Auto-format code
ruff check      # Check for issues
```

## Key Files

- `src/resources/JMdict_e`: Large XML dictionary file (150MB+, not in git)
- `src/wisho/jmdict/parser.py`: XML parsing with namespace-aware attribute extraction
- `src/wisho/db/seed.py`: Critical seeding logic with flush() pattern
- `src/migrations/migrations.yaml`: Monotome configuration
