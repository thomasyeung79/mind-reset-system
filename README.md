# 心境 MindHarmony AI

*让科学与古老智慧共同照亮内心。*

MindHarmony AI is being developed as a cross-cultural, interfaith AI platform for personal growth and well-being. It uses psychology education as its scientific foundation and offers distinct Christian, Buddhist and Taoist perspectives. Each perspective stands on its own, with religious teachings clearly distinguished from scientific findings.

The current local Streamlit demo uses fictional check-ins. It offers four topics per perspective in Chinese, English and Korean. Dashboard and Story Mode use the same session result. The demo makes no external AI calls.

## Run locally

Use Python 3.13, the version used to test this snapshot, in a virtual environment.

```sh
python -m pip install -r requirements.txt
python -m streamlit run perspective_app.py --server.address 127.0.0.1
```

`main.py` is a compatibility launcher for the same app. Keep the bind address on loopback and keep CORS and XSRF protection enabled.

Use fictional check-ins only. Check-ins stay in the current browser session and can be cleared with **Clear session**. This demo is for general reflection and does not provide diagnosis or treatment.

## Read-only public demo candidate

Run `python -m streamlit run public_demo.py` locally to view fictional examples.
Language, perspective and view tabs only switch what is already displayed.
This candidate never displays catalog article text. The hosting platform may log visits and usage.
Keep the existing local entry point and its loopback policy for interactive check-ins.

The four perspectives are Psychology, Christianity, Buddhism and Taoism. Psychology offers automatic or manual topic selection. The other perspectives use manual selection. The public snapshot ships with empty approved-content catalogs. An unavailable message is expected when you generate a result.

```sh
python -m unittest discover -s tests -v
```
