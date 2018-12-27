# Set Slack profile status when in the coworking

Use

```python
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
SLACK_API_KEY=app-api-key python app.py
```

The slack app needs to have `users.profile:write` scope permission.