```bash
docker build -t classifier-agent --no-cache .
```

```bash
docker run -p 8000:8000 --name classifier-agent classifier-agent
```
