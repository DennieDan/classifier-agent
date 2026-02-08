```bash
docker build -t classifier-agent --no-cache .
```

```bash
docker run -p 8000:8000 --name classifier-agent classifier-agent
```

Prompt for worker: explain to them

- HS-Code is Harmonized System Code so that they do not need to search.
- Ask it to give thought process.
