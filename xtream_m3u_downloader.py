#!/usr/bin/env python3
import os
import requests
import argparse
from requests.auth import HTTPBasicAuth

def download_m3u(base_url, username, password, output_path):
    try:
        # 构造认证URL
        auth = HTTPBasicAuth(username, password)
        api_url = f"{base_url}/player_api.php?username={username}&password={password}"
        
        # 验证凭据
        print("正在验证Xtream Codes凭据...")
        check = requests.get(api_url, auth=auth, timeout=10)
        if check.status_code != 200:
            raise Exception(f"认证失败，HTTP状态码: {check.status_code}")

        # 获取M3U列表
        m3u_url = f"{base_url}/get.php?username={username}&password={password}&type=m3u_plus"
        print(f"正在下载M3U列表: {m3u_url}")
        
        with requests.get(m3u_url, stream=True, auth=auth, timeout=30) as r:
            r.raise_for_status()
            os.makedirs(output_path, exist_ok=True)
            filepath = os.path.join(output_path, "playlist.m3u")
            
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"成功更新M3U文件: {filepath}")
            return True

    except Exception as e:
        print(f"操作失败: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Xtream Codes M3U下载器')
    parser.add_argument('--base_url', required=True, help='Xtream服务器基础URL')
    parser.add_argument('--username', required=True, help='Xtream账号')
    parser.add_argument('--password', required=True, help='Xtream密码')
    parser.add_argument('--output', default='./xtream_downloads', help='输出目录')
    args = parser.parse_args()
    
    download_m3u(
        args.base_url.rstrip('/'),
        args.username,
        args.password,
        args.output
    )

if __name__ == "__main__":
    main()
