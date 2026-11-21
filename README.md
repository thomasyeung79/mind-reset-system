# Mind Reset System

A local, multilingual Streamlit demo for fictional check-ins. It offers four perspectives with four topics each in Chinese, English and Korean. Dashboard and Story Mode use the same session result.

## Run locally

Use Python 3.13, the version used to test this snapshot, in a virtual environment.

```sh
python -m pip install -r requirements.txt
python -m streamlit run perspective_app.py --server.address 127.0.0.1
```

`main.py` is a compatibility launcher for the same app. Keep the bind address on loopback and keep CORS and XSRF protection enabled.

Use fictional check-ins only. Check-ins stay in the current browser session and can be cleared with **Clear session**. This demo is for general reflection and does not provide diagnosis or treatment.

The four perspectives are Psychology, Christianity, Buddhism and Taoism. Psychology offers automatic or manual topic selection. The other perspectives use manual selection. The public snapshot ships with empty approved-content catalogs. An unavailable message is expected when you generate a result.

```sh
python -m unittest discover -s tests -v
```
