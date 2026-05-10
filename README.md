# Flora Voice SIP Realtime Agent

FastAPI service for handling OpenAI Realtime SIP calls with the Agents SDK.
Incoming calls are accepted through the Realtime Calls API, then a Flora Voice
agent helps callers order flowers using dummy function tools.

## Prerequisites

- Python 3.10+
- An OpenAI API key with Realtime API access
- A configured OpenAI webhook secret
- A Twilio account with Elastic SIP Trunking
- A public HTTPS endpoint for local development, for example ngrok

## Configure OpenAI

Create a webhook pointing to:

```text
https://<your-public-host>/openai/webhook
```

Subscribe it to the `realtime.call.incoming` event and set the signing secret as
`OPENAI_WEBHOOK_SECRET`.

## Configure Twilio Elastic SIP Trunking

On the trunk **Origination** tab, add:

```text
sip:proj_<your_project_id>@sip.api.openai.com;transport=tls
```

Attach a Twilio phone number to the trunk so inbound calls are forwarded to
OpenAI.

## Setup

```bash
export OPENAI_API_KEY=...
export OPENAI_WEBHOOK_SECRET=whsec_...
```

Optional realtime model override:

```bash
export OPENAI_REALTIME_MODEL=gpt-realtime-2
```

Run the FastAPI server:

```bash
uv run uvicorn app.app:app --host 0.0.0.0 --port 8000
```

Expose it publicly:

```bash
ngrok http 8000
```

## Dummy Tools

The realtime agent currently includes placeholder function tools in
`app/tools.py`:

- `create_user`
- `search_user`
- `search_flowers`
- `create_order`

Replace those implementations when the real Flora Voice API is ready.
