#!/usr/bin/env python3
import os
import requests
import argparse
from requests.auth import HTTPBasicAuth

def download_m3u(base_url, username, password, output_path):
    try:
        # 构造认证URL并验证HTTPS连接
        auth = HTTPBasicAuth(username, password)
        api_url = f"{base_url}/player_api.php?username={username}&password={password}"
        
        # 验证SSL证书有效性
        print("正在验证HTTPS连接...")
        session = requests.Session()
        session.verify = True  # 强制验证SSL证书
        
        # 测试API连接
        test_res = session.get(api_url, auth=auth, timeout=10)
        if test_res.status_code != 200:
            raise Exception(f"API连接失败，状态码: {test_res.status_code}")

        # 下载M3U列表
        m3u_url = f"{base_url}/get.php?username={username}&password={password}&type=m3u_plus"
        print(f"正在安全下载HTTPS M3U列表...")
        
        with session.get(m3u_url, stream=True, auth=auth, timeout=30) as r:
            r.raise_for_status()
            os.makedirs(output_path, exist_ok=True)
            filepath = os.path.join(output_path, "playlist.m3u")
            
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"安全下载完成，文件已保存到: {filepath}")
            return True

    except requests.exceptions.SSLError as e:
        print(f"SSL证书验证失败: {str(e)}")
        print("建议检查服务器证书是否有效或添加自定义CA证书")
        return False
    except Exception as e:
        print(f"操作失败: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='HTTPS Xtream Codes下载器')
    parser.add_argument('--base_url', required=True, help='Xtream服务器HTTPS地址(包含https://)')
    parser.add_argument('--username', required=True, help='账号')
    parser.add_argument('--password', required=True, help='密码')
    parser.add_argument('--output', default='./xtream_downloads', help='输出目录')
    args = parser.parse_args()
    
    if not args.base_url.startswith('https://'):
        print("错误: 必须使用HTTPS协议地址")
        return
    
    download_m3u(
        args.base_url.rstrip('/'),
        args.username,
        args.password,
        args.output
    )

if __name__ == "__main__":
    main()