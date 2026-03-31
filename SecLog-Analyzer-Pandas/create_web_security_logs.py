import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 设置随机种子保证结果可复现
np.random.seed(42)

# 模拟数据量
num_records = 5000

# 1. 模拟 IP 地址
ips = [f"192.168.1.{i}" for i in range(1, 50)] + \
      [f"10.0.0.{i}" for i in range(1, 20)] + \
      ["220.181.38.149", "157.245.120.88", "45.33.21.11"] # 模拟几个外部攻击源

# 2. 模拟请求路径和攻击载荷
normal_urls = ["/index.html", "/login", "/api/v1/user", "/products", "/cart"]
attack_payloads = [
    "'; DROP TABLE users; --",
    "<script>alert('XSS')</script>",
    "admin' OR '1'='1",
    "../../etc/passwd",
    "union select null, user(), database()"
]

data = {
    "timestamp": [datetime.now() - timedelta(minutes=np.random.randint(0, 10000)) for _ in range(num_records)],
    "source_ip": np.random.choice(ips, num_records),
    "method": np.random.choice(["GET", "POST", "PUT", "DELETE"], num_records, p=[0.6, 0.3, 0.05, 0.05]),
    "status_code": np.random.choice([200, 302, 401, 403, 404, 500], num_records, p=[0.7, 0.1, 0.05, 0.05, 0.05, 0.05]),
    "response_time_ms": np.random.randint(10, 2000, num_records),
    "url": np.random.choice(normal_urls, num_records)
}

# 随机注入攻击载荷
df = pd.DataFrame(data)
attack_indices = np.random.choice(df.index, size=int(num_records * 0.08), replace=False)
df.loc[attack_indices, "url"] = df.loc[attack_indices, "url"] + "?id=" + np.random.choice(attack_payloads, len(attack_indices))

# 保存为 CSV
df.to_csv("web_security_logs.csv", index=False)
print("数据集 web_security_logs.csv 已生成！")