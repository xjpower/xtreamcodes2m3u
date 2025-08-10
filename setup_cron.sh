
#!/bin/bash

# 设置HTTPS定时任务
if [ $# -lt 5 ]; then
    echo "Usage: $0 <python_script> <https_url> <username> <password> <output_dir> <cron_expr>"
    echo "Example: $0 /path/to/xtream_https_downloader.py https://example.com user pass /home/user/xtream_downloads \"0 3 * * *\""
    exit 1
fi

SCRIPT=$1
HTTPS_URL=$2
USER=$3
PASS=$4
OUT_DIR=$5
CRON_EXPR=$6

(crontab -l 2>/dev/null; echo "$CRON_EXPR /usr/bin/python3 $SCRIPT --base_url \"$HTTPS_URL\" --username \"$USER\" --password \"$PASS\" --output \"$OUT_DIR\"") | crontab -

echo "HTTPS定时任务已配置:"
crontab -l