# Mind Reset System

A local Streamlit demo for multilingual reflection with fictional inputs.
General reflection only. It offers no diagnosis or treatment.

## Run locally

Use Python 3.11 or later in a virtual environment.

```sh
python -m pip install -r requirements.txt
python -m streamlit run main.py
```

The default bind address is 127.0.0.1. Keep CORS and XSRF protection enabled.
Use the sidebar for Chinese, English or Korean. Choose an automatic or manual
secular topic, then generate a fictional check-in. Dashboard and Story Mode
display the same result. No release-approved guidance is included. The labeled
interface example is separate from the content catalog.

Results live in the current session. Use Clear session to reset the demo.
This snapshot has no religious view, accounts, saved history or hosted service.

```sh
python -m unittest discover -s tests -v
```
