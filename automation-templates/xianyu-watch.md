# Xianyu scheduled watch template

For a recurring ChatGPT watch, use a stable ASCII watch id, for example:
- `requests/leica-m11.json`
- `requests/lhy-linear-power.json`

Request file shape:

```json
{
  "keyword": "老虎鱼线性电源",
  "run_marker": "change this each run"
}
```

Updating that file triggers `Xianyu Watch Request`. Read:
- `results/<watch-id>.json`

Every alert must include direct original item URLs.

Cadence guidance:
- fast-moving commodity electronics: hourly
- niche HiFi/cameras/pipes: every 2–6 hours unless the user requests otherwise
- never schedule more frequently than hourly
- use one broad query per run; only one narrower follow-up if clearly necessary
- stop extra queries if Module B returns login/verification/risk-control errors

This per-watch path avoids collisions between multiple scheduled product watches.
