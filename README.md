# Upload OSS

**A simple tool for uploading object to Aliyun OSS.**

## Requirements

- Python module requests
- Python module oss
- Python module Flask
- Python module gunicorn

## Module Installation

```
pip install -r requirements.txt
```

## Usage

Before use, copy Configs.example.py to Configs.py, and set the constants of ACCESS_KEY_ID, ACCESS_KEY_SECRET, OSS_ENDPOINT, BUCKET_NAME. If you want to use cutt.ly short url service, please also set URL_SHORTENER_API_KEY.

**Upload file to oss**

```
python main.py -f /path/to/file -d /oss/dir/you/want/to/upload
```

**Generate signed url and short url**

```
python gen_signed_url.py -f /path/to/saved/signed_url/file
```

or

```
python gen_signed_url.py -n uploaded_object_name
```

**Web UI to generate short url**

```
gunicorn -w 4 -b 0.0.0.0:4000 server:app
```

Access http://your-ip:4000 to visit the web interface

## LICENSE

**MIT**


