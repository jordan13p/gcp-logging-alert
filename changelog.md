# Changelog

## [3.0.2] - Jun 05, 2023

### Fixed

- 'time_delta' referenced before assignment

## [3.0.1] - Jun 05, 2023

### Fixed

- 刪除測試的 log

## [3.0.0] - Jun 05, 2023

### Changed

- 重構為物件導向架構

## [2.4.3] - Mar 20, 2023

## Add

- 新增要計數的環境變數設定

## [2.4.2] - Mar 20, 2023

## Fixed

- 修改 Counts 多環境一分鐘只會有一個訊息 Bug

## [2.4.1] - Mar 20, 2023

## Fixed

- 修改 gcsfuse log

## [2.4.0] - Mar 20, 2023

## Add

- 新增區分 Preprod Discord 頻道訊息

## [2.3.5] - Mar 10, 2023

## Fixed

- 修改 url 的時間範圍

## [2.3.4] - Feb 7, 2023

## Fixed

- 修改 error code 正則

## [2.3.3] - Dec 27, 2022

## Fixed

- Dev Discord 新增 sleep 隨機秒數來修復傳訊息收到 429 rate limit

## [2.3.2] - Dec 27, 2022

## Changed

- 修改 `EXTERNAL_API_UNAUTHORIZED` counts 次數 15 次以上才通知

## [2.3.1] - Dec 26, 2022

## Fixed

- 新增 sleep 隨機秒數來修復 Discord 傳訊息收到 429 rate limit

## [2.3.0] - Dec 23, 2022

## Add

- 新增檢查 messages 內容長度

## [2.2.0] - Dec 7, 2022

## Add

- 新增 `Namespaces` 資訊到 Counts messages 中

## [2.1.0] - Dec 7, 2022

## Add

- 新增 `Namespaces` 資訊到 Error Log messages 中

## [2.0.0] - Oct 18, 2022

## Add

- Dockerfile 新增 `gcsfuse` 工具
- 新增 `gcsfuse_run.sh` 來 mount GCS Bucket，並啟動 flask server
- 新增使用 `gcsfuse` 的環境變數

### Changed

- 更新 README.md
- 修改 Dockerfile 寫法
- 修改儲存時間 list 的 txt 檔案儲存位置，由本地改為 GCS 上

### Fixed

- 移除重複 import 的 modoule

## [1.7.1] - Oct 13, 2022

### Fixed

- 修改 healthz 路徑

## [1.7.0] - Oct 13, 2022

## Add

- 新增 healthz 回傳健康檢查

## [1.6.0] - Oct 11, 2022

## Add

- 新增計數告警訊息的時間範圍單位轉換，由秒數轉換為天數及分鐘

### Fixed

- 調整計數的時間訊息內容

## [1.5.1] - Oct 11, 2022

### Fixed

- 調整計數的訊息內容

## [1.5.0] - Oct 11, 2022

## Add

- 新增計數 `EXTERNAL_API_UNAUTHORIZED`，24 小時內超過 10 次，發出告警訊息

## [1.4.1] - Oct 11, 2022

### Changed

- 調整計數時間範圍的單位，由分鐘改為秒數

## [1.4.0] - Sep 6, 2022

### Added

- errorLog 及 counts 新增接收測試環境的 logging-alert (僅 discord)

### Changed

- 修改環境變數
- 調整 discord, telegram 傳送順序，使 discord 每分鐘可以傳到 30 則訊息

### Fixed

- 修正訊息的 Cloud Logging 連結
- 移除未使用的 `time` module

## [1.3.5] - Aug 30, 2022

### Fixed

- 改回傳 204 給 Pub/Sub，且不傳送超過一分鐘數量限制的訊息

## [1.3.4] - Aug 29, 2022

### Fixed

- 訊息的 Cloud Logging 連結新增 `&project=<PROJECT_ID>` 來修復缺少權限的提示

## [1.3.3] - Aug 19, 2022

### Added

- 新增 `extend_data.py` module，將擴增資料的 functions 拆出來

## [1.3.2] - Aug 15, 2022

### Changed

- 告警 URL 的搜尋條件新增 `http_load_balancer` 的 resource type

## [1.3.1] - Jul 20, 2022

### Changed

- 更新 counts 的 Log URL 不帶 Severity 搜尋條件

## [1.3.0] - Jul 14, 2022

### Added

- 新增錯誤訊息可以在 Cloud Run Logs 區分 Severity

### Fixed

- 程式發生錯誤時，使用 204 取代 400 回傳給 Pub / Sub，避免不斷重傳訊息

## [1.2.1] - Jul 13, 2022

### Fixed

- 修正 `counts` Error Code 正則

## [1.2.0] - Jun 28, 2022

### Added

- 為避免觸碰訊息數量限制，新增 N 秒內只傳送 1 次訊息的功能，且 count 仍會顯示總數
- N 秒設定為 60 秒，並寫入環境變數中，可視情況修改
- 新增 changelog.md

### Changed

- 更新 README.md `counts` 功能說明

### Removed

- 移除 `1.1.11` 功能

## [1.1.11] - Jun 28, 2022

### Added

- 新增觸碰到訊息數量限制時，由原先每計數一次就傳送一次通知，改為每 10 次傳送一次通知

## [1.1.10] - Jun 8, 2022

### Fixed

- 修正 `counts` Cloud Logging 連結網址的過濾條件 (Error Code)

## [1.1.9] - Jun 8, 2022

### Changed

- 更新 README.md 訊息數量限制的注意事項
- 更新 README.md 建立 Pub / Sub Topic 的參數

### Fixed

- 修正 `counts` 的 Cloud Logging 連結網址

## [1.1.8] - Jun 7, 2022

### Fixed

- 修正傳送訊息數量的限制，加入例外處理

> telegram bot message limit: 20 messages / min
> discord webhook message limit: 30 messages / min

## [1.1.7] - May 20, 2022

### Changed

- 更新 README.md 資源說明

### Fixed

- 修正 `counts` 取到錯誤的 Error Code

## [1.1.6] - May 18, 2022

### Fixed

- fix message value to string

## [1.1.5] - May 17, 2022

### Changed

- 改寫 check time list function

## [1.1.4] - May 17, 2022

### Fixed

- 加入 lock 來修復同時寫入檔案的錯誤

## [1.1.3] - May 16, 2022

### Changed

- 更新 README.md
- 更新 test 腳本
- 註解 counts time list 輸出的測試

### Removed

- 移除 `externalAPI` route

## [1.1.2] - May 16, 2022

### Fixed

- 修復 cloud sdk docker image to use apline version

## [1.1.1] - May 16, 2022

### Fixed

- 修復 counts 訊息內容

## [1.1.0] - May 16, 2022

### Added

- 新增及重構 `counts` route functions

### Changed

- 更新環境變數

## [1.0.6] - May 13, 2022

### Fixed

- 修復 Bad Request 條件

## [1.0.5] - May 13, 2022

### Fixed

- fix return 400 Bad Request

## [1.0.4] - May 12, 2022

### Changed

- Update alert message content
- Rewrite get alert message data in externalAPI route

### Fixed

- 修改 alert message data 中的 dtime 及 timestamp 取得

## [1.0.3] - May 11, 2022

### Changed

- Update gitignore
- 優化 dockerfile

## [1.0.2] - May 10, 2022

### Changed

- 啓用 discord message channel

## [1.0.1] - May 10, 2022

### Added

- README.md
- Start using logging alert

### Changed

- 更新環境變數

## [1.0.0] - May 9, 2022

### Added

- Logging alert first commit
- 建立 Cloud build CI/CD
