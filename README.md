# Week #025 ~ #028

## Psycopg 在 Python 上的使用

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
| `JSON`, `JSONB`            | Applied Psycopg plugin to convert `dict` and `list` |
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

### 標準錯誤 (Error)

在 Psycopg 中，錯誤處理是健壯應用程式的關鍵部分。Psycopg 定義了一個豐富的異常層次結構，所有異常都繼承自 `psycopg2.Error` 基類。這使得開發者可以根據需要捕獲特定類型的錯誤。

主要的錯誤類別包括：

*   **Warning**: 表示非致命的警告。
*   **Error**: 所有其他錯誤的基類。
    *   **InterfaceError**: 與資料庫接口相關的錯誤，例如無法建立連線。
    *   **DatabaseError**: 與資料庫操作相關的錯誤。
        *   **DataError**: 處理資料時發生的錯誤，例如資料超出範圍或類型不匹配。
        *   **OperationalError**: 資料庫操作相關的錯誤，不是由程式設計錯誤引起，例如連線中斷、資料庫不可用、記憶體不足等。
        *   **IntegrityError**: 違反資料庫完整性約束的錯誤，例如違反唯一約束、外鍵約束等。
        *   **InternalError**: 資料庫內部錯誤，例如游標無效。
        *   **ProgrammingError**: 程式設計錯誤，例如 SQL 語法錯誤、表格不存在或嘗試創造同名的表格、參數數量不匹配等。
        *   **NotSupportedError**: 嘗試執行不支援的操作時發生的錯誤。

在 Python 程式碼中，可以使用 `try...except` 塊來捕獲這些異常，以便優雅地處理錯誤並採取適當的恢復措施，例如回滾交易或記錄錯誤信息。

### 伺服器端與客戶端游標 (Server-Side vs Client-Side Cursors)

在 Psycopg 中，游標 (cursor) 是用於執行資料庫操作和遍歷結果集的對象。Psycopg 支援兩種主要的游標類型：客戶端游標 (client-side cursor) 和伺服器端游標 (server-side cursor)。

**客戶端游標 (Client-Side Cursor)**

這是 Psycopg 的預設行為。當使用客戶端游標時，執行查詢後，整個結果集會一次性從資料庫伺服器傳輸到客戶端 (即你的 Python 應用程式) 的記憶體中。這對於處理小型到中等大小的結果集非常方便，因為你可以快速地在記憶體中訪問所有資料。

然而，如果查詢返回的結果集非常大，使用客戶端游標可能會導致客戶端應用程式消耗大量記憶體，甚至可能導致記憶體不足錯誤 (out of memory errors)。

**伺服器端游標 (Server-Side Cursor)**

伺服器端游標允許你在資料庫伺服器上建立一個游標，並按需從伺服器獲取結果集的子集。這意味著整個結果集不會一次性載入到客戶端記憶體中，而是在你遍歷游標時分批獲取。

使用伺服器端游標的主要優勢在於處理大型結果集時顯著減少客戶端記憶體的使用。這對於需要處理數百萬甚至數十億行資料的應用程式來說至關重要。

**潛在應用場景**

*   **處理大型報告或資料匯出**: 當你需要從資料庫中匯出大量資料到檔案或生成大型報告時，伺服器端游標可以避免記憶體問題。
*   **資料 ETL (Extract, Transform, Load)**: 在 ETL 過程中，從源資料庫提取大量資料時，使用伺服器端游標可以更有效地管理記憶體。
*   **需要逐行處理大型結果集**: 如果你的應用程式需要對大型結果集中的每一行進行處理，而不是一次性載入所有資料，伺服器端游標是更合適的選擇。

**如何在 Psycopg 中使用伺服器端游標**

要在 Psycopg 中使用伺服器端游標，你需要在建立游標時指定一個名稱。例如：

```python
import psycopg2

conn = psycopg2.connect(...)
with conn.cursor('my_server_side_cursor') as cursor:
    cursor.execute("SELECT * FROM large_table;")
    # 現在你可以使用 fetchone() 或 fetchmany() 按需獲取資料
    for row in cursor:
        print(row)
```

請注意，伺服器端游標通常需要在一個事務塊 (transaction block) 內使用，並且在事務結束時會自動關閉。

## Postgres Terminal Command

```shell
psql -h localhost -U postgres
# e.g. psql -U <username> -d <dbname> -h <host> -p <port>
```

## 有用資源
- Psycopg 使用說明 [[連結](https://www.psycopg.org/docs/)]
    * 錯誤代碼列表 [[連結](https://www.psycopg.org/docs/errors.html#sqlstate-exception-classes)]
