# from cryptography.fernet import Fernet
# x = Fernet.generate_key()
# print(x)
# message = "HELLO WORlE"
# ins = Fernet(x)
# encMessage = ins.encrypt(message.encode())
# print(encMessage.decode("utf-8"))
# import jwt;  jwt.decode(jwt="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2Vya2V5IjoiRFJJVk8tS0ZaV1dFUlFESyIsImZpbGVrZXkiOiJGSUxFLUpSWVVDNEoiLCJleHAiOiIyMDIyLTA5LTE2IDIwOjQ3OjMwLjE2NjY5MSJ9.yVHWxLMYgdqiZ-RtzKyQavazsH9YbN8UHAjhPZ964uo", key= "SR4pa3ELt5IuXXrQap0A114M2pi-tJUCndhVPOy0Chc=", algorithms=["HS256"])
import time 
import datetime
from datetime import timezone
#dt = datetime.datetime("2022-09-16 20:53:30.301323")
#timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
print(datetime.datetime.now(tz=timezone.utc))