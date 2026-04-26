# 食譜收藏系統 - 流程圖與資料流設計 (Flowchart)

本文件基於 PRD（產品需求文件）與 Architecture（系統架構），視覺化使用者的操作路徑與系統內部的資料處理流程。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者從進入網站（首頁）開始，如何操作各項主要功能（搜尋、新增、分類、隨機推薦、查看詳細與編輯筆記等）。

```mermaid
flowchart LR
    A([使用者開啟網站]) --> B[首頁 - 食譜列表]
    
    B --> C{選擇操作}
    
    C -->|搜尋/查詢| D[輸入關鍵字搜尋]
    D --> B
    
    C -->|切換分類| E[點擊特定分類標籤]
    E --> B
    
    C -->|不知道吃什麼| F[點擊「隨機推薦」]
    F --> G[進入隨機食譜詳細頁]
    
    C -->|點擊特定食譜| G[食譜詳細頁]
    
    G --> H{操作食譜}
    H -->|新增筆記/編輯內容| I[進入編輯表單]
    I -->|儲存變更| G
    H -->|刪除食譜| J[彈出確認視窗並刪除]
    J --> B
    
    C -->|新增食譜| K{選擇新增方式}
    K -->|手動建立| L[手動填寫食譜表單]
    K -->|網址匯入| M[貼上網頁網址解析]
    
    L -->|送出儲存| G
    M -->|預填表單並確認| L
```

## 2. 系統序列圖（Sequence Diagram）

以下以「**使用者新增食譜**」這個核心情境為例，描述從前端送出表單到後端存入 SQLite 資料庫的完整資料流。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route (Controller)
    participant Model as Recipe Model (Model)
    participant DB as SQLite (Database)
    
    User->>Browser: 填寫新增食譜表單並點擊「儲存」
    Browser->>Route: POST /recipes/create (包含表單資料)
    Route->>Route: 驗證必填欄位 (名稱、食材等)
    Route->>Model: 呼叫建立食譜方法 (Create Recipe Object)
    Model->>DB: 執行 INSERT INTO SQL 語句
    DB-->>Model: 寫入完成，回傳成功狀態
    Model-->>Route: 回傳新建立的食譜 ID
    Route-->>Browser: HTTP 302 重新導向至 /recipes/{id} (詳細頁)
    Browser->>User: 頁面跳轉並顯示剛新增的食譜內容
```

## 3. 功能清單對照表

在接下來的開發中，我們將需要實作以下路由（Routes）以對應上述的流程圖操作：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **瀏覽食譜列表 (首頁)** | `/` 或 `/recipes` | `GET` | 顯示所有食譜，支援分類或關鍵字搜尋的 Query String |
| **新增食譜 (顯示表單)** | `/recipes/create` | `GET` | 顯示手動新增食譜的 HTML 表單 |
| **新增食譜 (送出資料)** | `/recipes/create` | `POST` | 接收表單資料並寫入資料庫 |
| **網址快速匯入預覽** | `/recipes/import` | `POST` | 接收外部網址，後端嘗試解析並回傳至建立表單 |
| **查看食譜詳細內容** | `/recipes/<id>` | `GET` | 根據 ID 查詢資料庫並顯示單一食譜內容與筆記 |
| **編輯食譜與筆記 (表單)**| `/recipes/<id>/edit` | `GET` | 顯示包含既有資料的編輯表單 |
| **編輯食譜與筆記 (儲存)**| `/recipes/<id>/edit` | `POST` | 接收更新資料並複寫資料庫內容 |
| **刪除食譜** | `/recipes/<id>/delete` | `POST` | 從資料庫中刪除指定 ID 的食譜，為防 CSRF 建議用 POST |
| **隨機推薦食譜** | `/recipes/random` | `GET` | 從資料庫中隨機撈取一筆食譜並重導向至其詳細頁面 |
| **管理分類標籤** | `/categories` | `GET` / `POST` | 查看與新增自訂的分類標籤 |
