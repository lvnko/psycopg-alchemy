# Week #025 ~ #028

## 1. Psycopg 在 Python 上的使用

### 1.1. `with` 陳述式與資料庫交易 (Transaction) 處理

在 Psycopg 中使用 `with` 陳述式可以有效地管理資料庫連線和交易。當程式碼區塊在 `with` 陳述式中執行時，它會建立一個交易上下文。如果在該區塊內發生任何例外情況，交易將會自動回滾 (rollback)，確保資料庫的完整性，避免部分完成的操作。相反地，如果 `with` 陳述式中的程式碼區塊成功執行完畢且沒有引發任何例外，則交易將會自動提交 (commit)，將所有變更永久保存到資料庫中。這種自動管理機制簡化了錯誤處理，並確保了交易的原子性，即交易中的所有操作要麼全部成功，要麼全部失敗回滾。

此外，當使用 `with` 陳述式管理連線時，無論程式碼區塊是成功退出還是因例外中斷，連線 (`conn`) 都會在 `with` 區塊結束時自動關閉。這表示開發者不需要手動呼叫 `conn.close()`，從而減少了資源洩漏的風險，並使程式碼更加簡潔。

### 1.2. 資料型別對應

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

#### 1.2.1. Postgre + Psycopy 資料型別的轉換特性
PostgreSQL 在處理用戶輸入的資料時，會自動進行類型轉換。以下是一些常見資料型別的轉換特性：

*   **BOOLEAN**: 可以接受 `TRUE`, `FALSE`, `'t'`, `'f'`, `'1'`, `'0'` 等字面值。
*   **DECIMAL**: 可以儲存具有指定精度的小數。在 Python 中轉換為 `float` 可能會犧牲精度，建議使用 `Decimal` 型別。
*   **DOUBLE PRECISION**: 可以儲存雙精度浮點數，通常具有約 15 位小數的精度。
*   **INT**: 可以儲存整數。
*   **VARCHAR**: 可以儲存可變長度的字串。

#### 1.2.2. 使用 Psycopg 的額外注意事項：

Psycopg 通常能夠自動將 Python 的原生資料型別轉換為對應的 PostgreSQL 型別。然而，對於某些特定的 PostgreSQL 型別，例如 `UUID` 和 `JSON`/`JSONB`，Psycopg 提供了特定的轉換器或適配器 (`UUID_adapter()` 和 `Json()`)，建議使用這些工具來確保正確的轉換和處理。

值得注意的是，雖然 PostgreSQL 的 `DECIMAL` 或 `NUMERIC` 型別在概念上可以對應到 Python 的 `float`，但在實際應用中，將高精度的 `DECIMAL` 資料轉換為 `float` 可能會導致精度損失。為了保留完整的精度，建議在 Python 中使用 `Decimal` 型別來處理這些資料。

此外，在使用 Psycopg 的 `execute` 方法進行參數綁定時，如果只有一個參數需要綁定，請確保將該參數放在一個單元素的 tuple 中，並在元素後加上逗號 (例如：`(value,)`)，以避免潛在的語法錯誤。

### 1.3. 標準錯誤 (Error)

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

### 1.4. 伺服器端與客戶端游標 (Server-Side vs Client-Side Cursors)

在 Psycopg 中，游標 (cursor) 是用於執行資料庫操作和遍歷結果集的對象。Psycopg 支援兩種主要的游標類型：客戶端游標 (client-side cursor) 和伺服器端游標 (server-side cursor)。

#### 1.4.1. 客戶端游標 (Client-Side Cursor)

這是 Psycopg 的預設行為。當使用客戶端游標時，執行查詢後，整個結果集會一次性從資料庫伺服器傳輸到客戶端 (即你的 Python 應用程式) 的記憶體中。這對於處理小型到中等大小的結果集非常方便，因為你可以快速地在記憶體中訪問所有資料。

然而，如果查詢返回的結果集非常大，使用客戶端游標可能會導致客戶端應用程式消耗大量記憶體，甚至可能導致記憶體不足錯誤 (out of memory errors)。

#### 1.4.2. 伺服器端游標 (Server-Side Cursor)

伺服器端游標允許你在資料庫伺服器上建立一個游標，並按需從伺服器獲取結果集的子集。這意味著整個結果集不會一次性載入到客戶端記憶體中，而是在你遍歷游標時分批獲取。

使用伺服器端游標的主要優勢在於處理大型結果集時顯著減少客戶端記憶體的使用。這對於需要處理數百萬甚至數十億行資料的應用程式來說至關重要。

#### 1.4.3. 潛在應用場景

*   **處理大型報告或資料匯出**: 當你需要從資料庫中匯出大量資料到檔案或生成大型報告時，伺服器端游標可以避免記憶體問題。
*   **資料 ETL (Extract, Transform, Load)**: 在 ETL 過程中，從源資料庫提取大量資料時，使用伺服器端游標可以更有效地管理記憶體。
*   **需要逐行處理大型結果集**: 如果你的應用程式需要對大型結果集中的每一行進行處理，而不是一次性載入所有資料，伺服器端游標是更合適的選擇。

#### 1.4.4. 如何在 Psycopg 中使用伺服器端游標

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

### 1.5. 利用 pandas 作為資料處理的工具

利用 pandas 處理 structured data 的優勢，把從 Postgres 讀取下來的資料做整理及清洗 (過濾) 並寫回資料庫中為以後取用。
可參考：``advanced_cases/pandas_pg2.py``

利用 pandas 處理從 PostgreSQL 讀取的資料，不僅能高效地進行資料清洗、轉換和分析，還能輕鬆地將處理後的資料寫回資料庫。這在資料科學、商業智慧和 ETL (Extract, Transform, Load) 流程中尤為重要。例如，在金融業，可以使用 pandas 清洗交易數據、計算指標並存回資料庫；在電商領域，則可用於分析用戶行為、處理訂單數據並更新庫存。這種結合方式極大地提高了資料處理的靈活性和效率。

### 1.6. Python Class 與 PostgreSQL 的直接交互

把 Python Class 轉換成 Insert SQL Statement
可參考：``advanced_cases/python_class.py``

將 Python Class 直接映射到資料庫操作，如生成 INSERT 語句，是實現簡易 ORM (Object-Relational Mapping) 的一種方式。這種方法使得資料庫操作更加物件導向，提高了程式碼的可讀性和可維護性。在開發 Web 應用程式或後端服務時，可以使用此技術來簡化資料模型的定義和資料的持久化。例如，可以定義一個 `User` Class，其屬性對應資料庫表格的欄位，然後直接使用 Class 實例來生成 SQL 語句，減少手動編寫重複的 SQL 程式碼。

### 1.7. 分檔案管理資料庫密鑰資訊

避免直接曝露驗證資訊在代碼中，利用 db.ini 與 Config Parser (configparser) 把驗證所需的資訊 (例：用戶名、密碼與密鑰等) 分開管理
可參考：``config_parser/config_parser.py``

將資料庫密鑰等敏感資訊儲存在獨立的設定檔 (如 .ini 檔案) 中，並使用 Config Parser 進行讀取，是業界通用的安全實踐。這有效避免了將敏感資訊硬編碼在程式碼中，降低了意外洩露的風險，尤其是在使用版本控制系統時。此外，這種方法也使得在不同環境 (開發、測試、生產) 中部署應用程式變得更加靈活，只需修改設定檔即可切換資料庫連線資訊，無需更改程式碼。這在微服務架構和雲端部署中尤為重要。

### 1.8 SQLAlchemy 的應用

SQLAlchemy 作為一個Python的ORM（對象關係映射）工具，開發者可以使用它建立數據庫連接，定義模型和映射，並執行基本的CRUD操作。

#### 1.8.1. 優勢 (Advantages)

SQLAlchemy 提供了許多優勢，使其成為 Python 中廣泛使用的資料庫工具：

*   **靈活性與控制力**: SQLAlchemy 提供了 ORM 和 Core 兩種使用方式。ORM 提供了高層次的抽象，簡化了資料庫操作；而 Core 則允許開發者編寫原始 SQL，提供了更精細的控制。這種靈活性使得 SQLAlchemy 能夠適應各種複雜的資料庫需求。
*   **強大的 ORM**: SQLAlchemy 的 ORM 功能強大且靈活，支援多種繼承策略、關聯關係映射和複雜查詢。它可以將 Python 物件無縫地映射到資料庫表格，簡化了資料的持久化和檢索。
*   **連接池與效能**: SQLAlchemy 內建了連接池管理，可以有效地管理資料庫連接，減少連接建立和關閉的開銷，提高應用程式的效能。
*   **資料庫方言支援**: SQLAlchemy 支援多種資料庫系統，並提供了相應的資料庫方言 (Dialect)，使得在不同資料庫之間遷移變得更加容易。
*   **活躍的社群與完善的文檔**: SQLAlchemy 擁有活躍的社群和完善的文檔，為開發者提供了豐富的資源和支援。

#### 1.8.2. 進階知識 (Advanced Knowledge)

深入了解 SQLAlchemy 可以進一步提升開發效率和應用程式效能：

*   **以 Engine 在底層做核心、而 Session 在為上層的街口**: 

    * **Engine** (或 Connection，屬於 SQLAlchemy Core 的一部分)，是與資料庫進行交互的核心，負責與資料庫建立實際的物理連接並管理連接池。它是 SQLAlchemy 與資料庫驅動程式交互的底層接口。
    而 Session (屬於 SQLAlchemy ORM 的一部分) 則提供了一個高層次的接口，用於管理 ORM 物件的狀態和與資料庫的交互。

    * **Session**: Session (屬於 SQLAlchemy ORM 的一部分) 提供了一個高層次的接口，用於管理 ORM 物件的狀態和與資料庫的交互。Session 通過 Engine (或 Connection) 來執行實際的 SQL 語句，但它提供了物件的持久化、身份映射、事務管理和生命週期等 ORM 功能，理解 Session 的這些特性對於編寫高效且可靠的資料庫應用程式非常重要。若想了解更多關於 Session 的使用方法及知識，可以參考這篇：[官方文件](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)。

    * **兩者放在一起，如何理解**: 可以將 Engine 視為資料庫連接的工廠和管理器，而 Session 則是與資料庫進行 ORM 級別交互的工作單元。一個 Engine 可以被多個 Session 使用，每個 Session 在需要時從 Engine 獲取連接。

*   **惰性載入與積極載入**: SQLAlchemy 支援惰性載入 (Lazy Loading) 和積極載入 (Eager Loading)。惰性載入在訪問關聯物件時才執行查詢，而積極載入則在查詢主物件時一併載入關聯物件。選擇合適的載入策略可以顯著影響查詢效能。若想更進一步瞭解它的實現技巧，可以參考包括 ``joinedload``、``subqueryload``與``selectinload`` 這些在使用 ``session`` 訪問時的設定選項。

*   **單元測試與模擬**: SQLAlchemy 提供了工具和模式，使得對資料庫交互的程式碼進行單元測試和模擬變得更加容易。
*   **遷移工具**: 結合 Alembic 等遷移工具，可以方便地管理資料庫模式的變更。

#### 1.8.3. 注意事項 (Things to Notice)

在使用 SQLAlchemy 時，需要注意一些事項：

*   **Session 的使用**: Session 不是執行緒安全的，每個執行緒應該使用自己的 Session。在 Web 應用程式中，通常每個請求使用一個 Session。
*   **事務管理**: 雖然 ORM 在某些情況下會自動管理事務，但在處理複雜操作時，明確地管理事務 (使用 `session.commit()`, `session.rollback()`) 是很重要的。
*   **SQLAlchemy Core 與 ORM 的選擇**: 根據具體需求選擇使用 SQLAlchemy Core 或 ORM。對於簡單的查詢和操作，Core 可能更直接；對於複雜的資料模型和業務邏輯，ORM 更具優勢。
*   **Serial 類型與 Flush**: 對應 Postgres 預設 database 設計的 flush 設定，有時需要用到它來避免作為 primary key 的 serial number 在沒有 (或沒能) ``session.commit()`` 時仍會增算的情況。理解 `session.flush()` 的作用以及它與 `session.commit()` 的區別對於處理某些特定的資料庫行為非常重要。

## 2. Postgres Terminal Command

```shell
psql -h localhost -U postgres
# e.g. psql -U <username> -d <dbname> -h <host> -p <port>
```

## 3. 有用資源
- Psycopg 使用說明 [[連結](https://www.psycopg.org/docs/)]
    * 錯誤代碼列表 [[連結](https://www.psycopg.org/docs/errors.html#sqlstate-exception-classes)]
- SQLAlchemy 簡單說出 10 個優點 [[連結](https://pajhome.org.uk/blog/10_reasons_to_love_sqlalchemy.html)]
- Python 資料庫應用程式介面規範 v2.0 (PEP 249) [[連結](https://peps.python.org/pep-0249/)]
