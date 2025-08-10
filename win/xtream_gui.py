import tkinter as tk
from tkinter import ttk, messagebox
import os
import requests
from requests.auth import HTTPBasicAuth
import threading

class XtreamDownloader:
    def __init__(self, root):
        self.root = root
        root.title("Xtream M3U下载器 v1.0")
        root.geometry("500x300")
        
        # 主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入区域
        ttk.Label(main_frame, text="服务器地址:").grid(row=0, column=0, sticky=tk.W)
        self.url_entry = ttk.Entry(main_frame, width=40)
        self.url_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="用户名:").grid(row=1, column=0, sticky=tk.W)
        self.user_entry = ttk.Entry(main_frame, width=40)
        self.user_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="密码:").grid(row=2, column=0, sticky=tk.W)
        self.pass_entry = ttk.Entry(main_frame, width=40, show="*")
        self.pass_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(main_frame, text="保存路径:").grid(row=3, column=0, sticky=tk.W)
        self.path_entry = ttk.Entry(main_frame, width=40)
        self.path_entry.insert(0, os.path.expanduser("~/Downloads"))
        self.path_entry.grid(row=3, column=1, pady=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.download_btn = ttk.Button(btn_frame, text="下载M3U", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)
        
        # 日志区域
        self.log_text = tk.Text(main_frame, height=5, state="disabled")
        self.log_text.grid(row=6, column=0, columnspan=2, sticky="ew")
        
    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        
    def start_download(self):
        url = self.url_entry.get().strip()
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        path = self.path_entry.get().strip()
        
        if not all([url, username, password, path]):
            messagebox.showerror("错误", "请填写所有字段")
            return
            
        self.download_btn.config(state="disabled")
        self.progress["value"] = 0
        self.log("开始下载任务...")
        
        thread = threading.Thread(
            target=self.download_m3u,
            args=(url, username, password, path),
            daemon=True
        )
        thread.start()
        
    def download_m3u(self, base_url, username, password, output_path):
        try:
            if not base_url.startswith(("http://", "https://")):
                base_url = "http://" + base_url
                
            api_url = f"{base_url}/player_api.php"
            m3u_url = f"{base_url}/get.php?username={username}&password={password}&type=m3u_plus"
            
            self.update_progress(10)
            self.log("正在验证服务器连接...")
            
            auth = HTTPBasicAuth(username, password)
            session = requests.Session()
            session.verify = False  # 禁用SSL验证(仅用于测试环境)
            
            # 测试连接
            response = session.get(api_url, auth=auth, timeout=10)
            if response.status_code != 200:
                raise Exception(f"服务器返回错误: {response.status_code}")
                
            self.update_progress(30)
            self.log("连接验证成功，开始下载...")
            
            # 下载M3U文件
            with session.get(m3u_url, stream=True, auth=auth, timeout=30) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                os.makedirs(output_path, exist_ok=True)
                filepath = os.path.join(output_path, "playlist.m3u")
                
                with open(filepath, 'wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = 30 + int(70 * (downloaded / total_size)) if total_size > 0 else 100
                        self.update_progress(progress)
                        
                self.log(f"下载完成！文件已保存到:\n{filepath}")
                self.update_progress(100)
                messagebox.showinfo("成功", "M3U文件下载完成！")
                
        except Exception as e:
            self.log(f"错误: {str(e)}")
            messagebox.showerror("错误", f"下载失败: {str(e)}")
        finally:
            self.root.after(0, lambda: self.download_btn.config(state="normal"))
            
    def update_progress(self, value):
        self.root.after(0, lambda: self.progress.config(value=value))

if __name__ == "__main__":
    root = tk.Tk()
    app = XtreamDownloader(root)
    root.mainloop()
