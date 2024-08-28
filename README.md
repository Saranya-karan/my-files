# my-files

# Have your project as follows
```
├── my-files
│   ├── credentials
│   │   ├── certificate.pem.crt
│   │   ├── credentials.json
│   │   ├── private.pem.key
│   ├── fetch_credentials.py
│   ├── main.py
│   ├── simple1.py
└── .gitignore
```

Contents of the `credentials.json` can be as follows
```json
{
    "wifi_ssid": "xxxx",
    "wifi_password": "xxxx",
    "client_id": "xxxx",
    "aws_endpoint": "xxxx.iot.xxxx.amazonaws.com",
    "pub_topic": "xxxx",
    "sub_topic": "xxxx"
}
```