# Week #025 ~ #028

## Psycopg 在 Pythong 上的使用

### `with` 陳述式與交易 (Transaction) 處理

在 Psycopg 中使用 `with` 陳述式可以有效地管理資料庫連線和交易。當程式碼區塊在 `with` 陳述式中執行時，它會建立一個交易上下文。如果在該區塊內發生任何例外情況，交易將會自動回滾 (rollback)，確保資料庫的完整性，避免部分完成的操作。相反地，如果 `with` 陳述式中的程式碼區塊成功執行完畢且沒有引發任何例外，則交易將會自動提交 (commit)，將所有變更永久保存到資料庫中。這種自動管理機制簡化了錯誤處理，並確保了交易的原子性，即交易中的所有操作要麼全部成功，要麼全部失敗回滾。

此外，當使用 `with` 陳述式管理連線時，無論程式碼區塊是成功退出還是因例外中斷，連線 (`conn`) 都會在 `with` 區塊結束時自動關閉。這表示開發者不需要手動呼叫 `conn.close()`，從而減少了資源洩漏的風險，並使程式碼更加簡潔。

### 資料型別對應

以下是常見的 Postgres/Psycopg 資料型別及其對應的 Python 資料型別：

| Postgres/Psycopg Data Type | Python Data Type |
| -------------------------- | ---------------- |
| `NULL`                     | `None`           |
| `BOOLEAN`                  | `bool`           |
| `INTEGER`                  | `int`, `long`    |
| `BIGINT`                   | `int`, `long`    |
| `SMALLINT`                 | `int`, `long`    |
| `NUMERIC`, `DECIMAL`       | `Decimal`, `float` |
| `DOUBLE PRECISION`, `REAL` | `float`          |
| `BYTEA`                    | `bytes`          |
| `VARCHAR`, `TEXT`          | `str`, `unicode` |
| `DATE`                     | `datetime.date`  |
| `TIME`, `TIMEZ`            | `time`           |
| `TIMESTAMP`,`TIMESTAMPTZ`  | `datetime.datetime` |
| `ARRAY`                    | `list`           |
| Composite types `IN` syntax | `tuple`, `namedtuple` |
| `JSON`, `JSONB`            | Applied Psycopg plugin to convert `dict` and `list`   |
| `UUID`                     | `uuid.UUID`      |

#### Postgre + Psycopy 資料型別的轉換特性
PostgreSQL 在處理用戶輸入的資料時，會自動進行類型轉換。以下是一些常見資料型別的轉換特性：

*   **BOOLEAN**: 可以接受 `TRUE`, `FALSE`, `'t'`, `'f'`, `'1'`, `'0'` 等字面值。
*   **DECIMAL**: 可以儲存具有指定精度的小數。在 Python 中轉換為 `float` 可能會犧牲精度，建議使用 `Decimal` 型別。
*   **DOUBLE PRECISION**: 可以儲存雙精度浮點數，通常具有約 15 位小數的精度。
*   **INT**: 可以儲存整數。
*   **VARCHAR**: 可以儲存可變長度的字串。

#### 使用 Psycopg 的額外注意事項：

Psycopg 通常能夠自動將 Python 的原生資料型別轉換為對應的 PostgreSQL 型別。然而，對於某些特定的 PostgreSQL 型別，例如 `UUID` 和 `JSON`/`JSONB`，Psycopg 提供了特定的轉換器或適配器 (`UUID_adapter()` 和 `Json()`)，建議使用這些工具來確保正確的轉換和處理。

值得注意的是，雖然 PostgreSQL 的 `DECIMAL` 或 `NUMERIC` 型別在概念上可以對應到 Python 的 `float`，但在實際應用中，將高精度的 `DECIMAL` 資料轉換為 `float` 可能會導致精度損失。為了保留完整的精度，建議在 Python 中使用 `Decimal` 型別來處理這些資料。

此外，在使用 Psycopg 的 `execute` 方法進行參數綁定時，如果只有一個參數需要綁定，請確保將該參數放在一個單元素的 tuple 中，並在元素後加上逗號 (例如：`(value,)`)，以避免潛在的語法錯誤。

## 有用資源
- Psycopg 使用說明 [[連結](https://www.psycopg.org/docs/)]
