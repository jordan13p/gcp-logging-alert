# Logging Alert

- 此專案為簡易的 Python Flask Server 專案，負責將 Log 訊息傳送至通訊軟體

## Demo

### 一般 Error Log

- Discord

  ![logging_alert_demo1](https://imgur.com/PYPZCmT.png)

- Telegram

  ![logging_alert_demo2](https://imgur.com/9dUNUU3.png)


### 計數 Error Log

- Discord

  ![logging_alert_counts_demo1](https://imgur.com/7RJrnuI.png)

- Telegram

  ![logging_alert_counts_demo2](https://imgur.com/QFP8Zit.png)

## 資源概覽

### Sinks (路由器)

1. logging-alerts-sinks-errorLog
2. logging-alerts-sinks-counts

### Pub / Sub and Topics

Topic <-> Sub

1. logging-alerts-sinks-errorLog <-> send-all-error-log-to-logging-alerts-sinks
2. logging-alerts-sinks-counts <-> send-error-log-counts-to-logging-alerts-sinks

### Cloud Run

1. Cloud Run: logging-alerts-sinks `/errorLog`
2. Cloud Run: logging-alerts-sinks `/counts`

### Cloud Storage

1. Bucket: logging_buckets
    - Directory: `logging-alerts-sinks/*`

## 架構說明

![logging_alert](https://imgur.com/fYVJPyJ.png)

1. Cloud Logging 依搜尋條件建立路由器 (sinks)，通知管道為 Pub / Sub
2. Pub / Sub 會收到告警訊息，並觸發 Cloud Run
3. Cloud Run 使用 Python 接收告警訊息，並轉發到 Telegram Bot 及 Discord Webhook
4. 記錄時間 list 的 txt 檔，會透過 `gcsfuse` 方式儲存到 GCS 指定的 Bucket

### 一般 Error Log

程式說明：

- Server 的路徑為 `/errorLog`
- 會接收所有的 error log 來做資料的整理，將需要的資訊傳送至通訊軟體
- 如須排除或指定 error log，可透過 Cloud Logging 的 `logging-alerts-sinks-errorLog` 路由器來設定

### 計數 Error Log

程式說明：

- Server 的路徑為 `/counts`
- 程式接收後，會自動判斷 error code、服務、時間範圍及計數的次數
- 此段程式為有狀態的程式，會將收到 log 當下往前檢查 N 分鐘，達到 M 次會發出告警訊息
- 將 N 分鐘內的 timestamp 使用 python list 儲存在服務的 `/docs/$cluster_name/$namespace_name/$container_name/$error_code.txt` 中
- 上述路徑之檔案會透過 `gcsfuse` 與 GCS 串接，可從 GCS 查看檔案內容
- 為避免觸碰 Telegram 每分鐘訊息限制，以及避免通知過吵，設定為 X 秒只會通知一次
- 時間範圍、次數及通知週期可透過環境變數 `.env` 設定，且可依照不同的 error log name 來設定不同的環境變數值

  ```bash
  # Example
  # gcsfuse
  LOCAL_MNT_DIR=./logging_alert/docs
  BUCKET=logging_buckets
  BUCKET_MNT_DIR=logging-alerts-sinks/

  # default send message period (unit: seconds)
  SEND_MESSAGE_PERIOD = 60
  
  # default TIME_RANGES or customize TIME_RANGES (unit: seconds)
  TIME_RANGES=600
  TIME_RANGES_EXTERNAL_API_UNAUTHORIZED=86400
  
  # default LIMIT_TIMES or customize LIMIT_TIMES
  LIMIT_TIMES=10
  LIMIT_TIMES_EXTERNAL_API_UNAUTHORIZED=10
  ```

新增要計數的 Error Log：

- 僅需要在 sinks 修改搜尋條件 or 新增不同搜尋條件的 sinks
- Pub / Sub 無須更改，皆送至同一個即可
- Cloud Run 的 `counts()` 程式也不用修改，程式會自動判斷

參考：

- <https://cloud.google.com/run/docs/tutorials/network-filesystems-fuse>

## 資料夾結構

- `run.py`：Run Server
- `/logging_alert/__init__.py`：flask server 相關設定
- `requirements.txt`：Python 會使用到的套件版本
- `Dockerfile`：將此專案打包成 Docker Image
- `cloudbuild.yaml`：CI / CD 自動化部署到 Cloud Run
- `/logging_alert/controllers/*`：flask server 路由位置設定
- `/logging_alert/docs/*`：將計數的時間資料儲存在本地，並且此路徑會透過 gcsfuse 掛載 GCS
- `/logging_alert/services/*`：Error Log 的程式邏輯
- `/logging_alert/utils/*`：一般 Error Log 與計數 Error Log 的共用程式
- `/logging_alert/test/*`：測試腳本及檔案

```bash
./logging-alert
├── Dockerfile
├── README.md
├── changelog.md
├── cloudbuild.yaml
├── gcsfuse_run.sh
├── logging_alert
│   ├── __init__.py
│   ├── controllers
│   │   ├── __init__.py
│   │   └── logging_alert.py
│   ├── docs
│   │   └── prod-asia-01
│   │       └── test-namespace
│   │           └── game-ap
│   │               ├── EXTERNAL_API_ERROR.txt
│   │               └── record_send_time.txt
│   ├── services
│   │   ├── __init__.py
│   │   ├── counts_check.py
│   │   ├── counts_data.py
│   │   ├── error_log_data.py
│   │   ├── init_data.py
│   │   ├── message_content.py
│   │   └── send_message.py
│   ├── tests
│   │   ├── scripts_test
│   │   │   ├── pub_sub_data.json
│   │   │   ├── pub_sub_data_error.json
│   │   │   └── test.sh
│   │   └── unit_test
│   │       ├── __init__.py
│   │       ├── test_error_log_data.py
│   │       └── test_init_data.py
│   └── utils
│       ├── __init__.py
│       ├── logger.py
│       └── messenger.py
├── requirements.txt
└── run.py
```

## 設定說明

### Telegram Bot

1. 在 Telegram 搜尋 [BotFather](https://telegram.me/botfather)，並按下「Start」的按鈕
2. 建立機器人 `/newbot`，並為機器人命名，且名稱結尾一定要是「_bot」或者「Bot」
3. 取得機器人的 token，及個人帳戶的 User ID

詳細步驟可參考：

- <https://marketingliveincode.com/?p=172>

><注意> Telegram Bot 群組訊息限制為每分鐘 20 則訊息

### Discord Webhook

1. 編輯頻道 > 整合 > 查看 webhook > 新增 webhook
2. 取得 webhook url

詳細步驟可參考：

- <https://10mohi6.medium.com/super-easy-python-discord-notifications-api-and-webhook-9c2d85ffced9>

><注意> Discord Webhook 訊息限制為每分鐘 30 則訊息

### Cloud Run IAM

1. 建立 Service Account
2. 向 Service Account 授予訪問 Cloud Storage 儲存桶的權限

```bash
$ gcloud iam service-accounts create cloud-run-fs-identity \
    --display-name "Cloud Run GCS Identity"

$ gcloud projects add-iam-policy-binding <PROJECT_ID> \
     --member "serviceAccount:cloud-run-fs-identity@<PROJECT_ID>.iam.gserviceaccount.com" \
     --role "roles/storage.objectAdmin"
```

### First Cloud Run Deploy

```bash
# deploy to cloud run
$ gcloud beta run deploy logging-alerts-sinks \
--image=us-docker.pkg.dev/<PROJECT_ID>/<PROJECT_NAME>/logging-alert:2.0.0 \
--region=asia-southeast1 \
--project=<PROJECT_ID> \
--execution-environment gen2 \
--service-account cloud-run-fs-identity \
--min-instances=0 \
--max-instances=1 \
--no-allow-unauthenticated

# (Optional)
$ gcloud run services update logging-alerts-sinks \
--update-env-vars TELEGRAM_USER_ID=$YOUR_TELEGRAM_USER_ID,TELEGRAM_TOKEN=$TELEGRAM_BOT_TOKEN,DISCORD_WEBHOOK_URL=$DISCORD_WEBHOOK_URL
```

#### <備註>

1. 專案中有 `.env` 設定，因此可不用額外設定環境變數
2. 執行順序：如果您在容器中設置預設環境變數，並在 Cloud Run 服務上設置具有相同名稱的環境變數，則該服務中設置的值優先
3. 如要使用第二代 Cloud Run 環境，部署指令需要加上 `beta`

參考：

- <https://cloud.google.com/run/docs/tutorials/pubsub#integrating-pubsub>
- <https://cloud.google.com/run/docs/configuring/environment-variables#precedence>
- <https://cloud.google.com/run/docs/configuring/cpu-allocation>

### Pub / Sub IAM

1. 建立 Service Account
2. 設定 Cloud Run 需要驗證才能訪問

```bash
$ gcloud iam service-accounts create cloud-run-pubsub-invoker \
    --display-name "Cloud Run Pub/Sub Invoker"

$ gcloud run services add-iam-policy-binding logging-alerts-sinks \
    --member=serviceAccount:cloud-run-pubsub-invoker@<PROJECT_ID>.iam.gserviceaccount.com \
    --role=roles/run.invoker \
    --region=asia-southeast1

$ gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member=serviceAccount:service-000000000000@gcp-sa-pubsub.iam.gserviceaccount.com \
    --role=roles/iam.serviceAccountTokenCreator
```

參考：

- <https://cloud.google.com/run/docs/tutorials/pubsub#integrating-pubsub>

### Pub / Sub

1. 依照不同的 Log 篩選條件，建立多個 Pub / Sub 主題
2. 設定 Pub / Sub 主題的 "訂閱項目"，並設定權限

```bash
$ gcloud pubsub topics create logging-alerts-sinks-errorLog
$ gcloud pubsub topics create logging-alerts-sinks-counts

$ gcloud pubsub subscriptions create send-all-error-log-to-logging-alerts-sinks --topic logging-alerts-sinks-errorLog \
   --ack-deadline=300 \
   --push-endpoint=$CLOUD_RUN_URL/errorLog \
   --push-auth-service-account=cloud-run-pubsub-invoker@<PROJECT_ID>.iam.gserviceaccount.com

$ gcloud pubsub subscriptions create send-error-log-counts-to-logging-alerts-sinks --topic logging-alerts-sinks-counts \
   --ack-deadline=300 \
   --push-endpoint=$CLOUD_RUN_URL/counts \
   --push-auth-service-account=cloud-run-pubsub-invoker@<PROJECT_ID>.iam.gserviceaccount.com
```

參考：

- <https://cloud.google.com/run/docs/tutorials/pubsub#integrating-pubsub>

### Cloud Logging Sinks (路由器)

記錄檔路由器分頁點選建立接收器 (sinks)：
  
1. 輸入接收器名稱
2. 接收器目標選擇 Cloud Pub / Sub 主題
3. 建立搜尋條件，當符合此條件會發出告警訊息

```bash
# logging-alerts-sinks-errorLog
# Error Log： admin-ap, game-ap
resource.type="k8s_container"
severity=ERROR
(resource.labels.container_name="admin-ap" OR
resource.labels.container_name="game-ap")
(jsonPayload.message!~"^.*(EXTERNAL_API_UNAUTHORIZED).*$" OR
textPayload!="")

# logging-alerts-sinks-counts
# Log： admin-ap, game-ap
resource.type="k8s_container"
jsonPayload.message=~"^.*(EXTERNAL_API_ERROR|EXTERNAL_API_UNAUTHORIZED).*$"
(resource.labels.container_name="admin-ap" OR
resource.labels.container_name="game-ap")
```

> <注意> EXTERNAL_API_UNAUTHORIZED 為暫時列入 counts

## Cloud Build

當此專案分支打上 tag 會觸發 Cloud Build 執行部署服務至 Cloud Run

```yaml
steps:
  # Build container image
  - name: gcr.io/cloud-builders/docker
    args: [ 'build', '-t', 'us-docker.pkg.dev/$PROJECT_ID/$PROJECT_NAME/logging-alert:$TAG_NAME', '.' ]

  # Push container image
  - name: gcr.io/cloud-builders/docker
    args: [ "push", "us-docker.pkg.dev/$PROJECT_ID/$PROJECT_NAME/logging-alert:$TAG_NAME" ]

  # Deploy container image to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk:alpine'
    entrypoint: gcloud
    args:
    - 'run'
    - 'deploy'
    - 'logging-alerts-sinks'
    - '--image'
    - 'us-docker.pkg.dev/$PROJECT_ID/$PROJECT_NAME/logging-alert:$TAG_NAME'
    - '--region'
    - 'asia-southeast1'

options:
  logging: GCS_ONLY
  # pool: # use private pool to connect private IP services
  #   name: ''

```

參考：

- <https://cloud.google.com/build/docs/deploying-builds/deploy-cloud-run>

## 測試說明

1. 此測試為簡易的本地測試，非使用 Python 的測試工具
2. `/logging_alert/test/pub_sub_data.json` 為模擬 Pub / Sub 送訊息至 Cloud Run 的資料
3. 測試需要將 `run.py` 中 `app.run()` 程式取消註解再執行

   ```python
   # run.py
   if __name__ == '__main__':
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
   ```

   ```bash
   # Run Flask server
   $ python run.py

   # Docker
   $ docker build -t logging_alert:0.0.1 . --no-cache
   $ docker run -p 8080:8080 -e PORT=8080 logging_alert:0.0.1
   ```

4. 當本地 Sever 開始執行後，執行腳本進行測試

   ```bash
   # run test
   # /logging_alert/test/test.sh
   $ ./test.sh
   ```

<備註>

1. 本地測試時，不要使用 `gcsfuse_run.sh` 執行，因權限問題 gcsfuse 本地無法使用
2. ARM 處理器在 Build Docker Image 時，需要設定 `linux/amd64`，否則會無法 Build
