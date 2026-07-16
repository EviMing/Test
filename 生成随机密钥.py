import secrets
import string

#[定义函数] 生成由 数字与大小写字母 组成的 指定字符长度 的密钥
def generate_strong_key(length=128):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

key = generate_strong_key(128)
print(key)