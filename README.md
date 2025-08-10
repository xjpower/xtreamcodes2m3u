# xtreamcodes2m3u
Convert xtream codes to m3u, support HTTP/HTTPS link download, and automatically update downloaded files

xtream_https_downloader.py 用于下载https地址的链接

xtream_m3u_downloader.py 用于下载http地址的链接

win目录中为windows版本带GUI

功能特点

‌强制HTTPS验证‌：程序会严格验证服务器SSL证书有效性，确保通信安全


‌双重认证机制‌：同时使用HTTP基本认证和URL参数认证


‌安全下载‌：采用流式传输避免内存溢出，支持大文件下载


‌自动重试‌：内置连接超时处理机制（30秒超时）


‌错误处理‌：包含详细的SSL证书验证失败提示



使用说明

安装依赖：pip install requests

测试运行：

bashCopy Codepython3 xtream_https_downloader.py \
  --base_url https://your-xtream-server.com \
  --username YOUR_USERNAME \
  --password YOUR_PASSWORD \
  --output /path/to/save
设置每日自动更新：

bashCopy Codechmod +x setup_cron.sh
./setup_cron.sh /path/to/xtream_https_downloader.py \
  https://your-xtream-server.com \
  USER PASS \
  /path/to/save \  "0 3 * * *"


关于urllib3 v2仅支持OpenSSL 1.1.1+的解决方案


解决方案

方案1：升级OpenSSL
推荐将系统OpenSSL升级到1.1.1或更高版本：

对于RHEL/CentOS 7用户：

默认提供1.0.2k，需考虑升级到RHEL/CentOS 8+或手动编译安装新版本

对于Debian/Ubuntu用户：

Ubuntu 18.04+和Debian 10+默认提供OpenSSL 1.1.1

方案2：降级urllib3
如果无法升级OpenSSL，可以降级urllib3到v1.x版本：

textCopy Codepip install "urllib3<2.0"


——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

win版本使用
主要功能特点：

原生Windows GUI界面，使用标准tkinter组件
支持HTTPS/HTTP协议自动识别
包含进度条和日志显示区域
多线程下载避免界面卡顿
自动创建输出目录结构
默认保存路径设为用户下载文件夹
使用说明：

安装Python 3.8+和依赖库：pip install -r requirements.txt
直接运行：python xtream_gui.py
填写服务器地址、账号信息后点击下载按钮
注意事项：

生产环境建议启用SSL证书验证(修改session.verify=True)
如需定时任务可配合Windows任务计划程序使用
界面支持高DPI显示缩放



