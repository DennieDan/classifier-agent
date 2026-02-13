## NiceGUI interface

From the project root, install dependencies and run the UI:

```bash
pip install -r requirements.txt
python run_ui.py
```

Then open [http://localhost:8080](http://localhost:8080) in your browser. The UI has a left sidebar with conversation list, a main area for input (or process/conversation view), and a plus button (top right) to start a new prompt.

---

```bash
docker build -t classifier-agent --no-cache .
```

```bash
docker run -p 8000:8000 --name classifier-agent classifier-agent
```

Prompt for worker: explain to them

- HS-Code is Harmonized System Code so that they do need to search.
- Ask it to give thought process.

* Exactly the same
  Personal deodorant: I cannot verify if a product called "Personal deodorant" falls under any heading in the table you provided. Can I help you with anything else?
  Radiator panels: 8504.90.31 and 8504.90.41.

* High ambiguity

Supervisor:

- Only return 1 result
  - Among all possibilities return by the search agent, give the (score for each + explanation) -> as feedback and choose the best one
  - Compare it with the threshold: if low then give the whole feedback to the search agent
- need to identify the main feature of it
  **The Overlap**: "Modular solar-powered IoT sensors for agricultural moisture tracking.
  " (Is
  it 8541 Solar or 9025 Sensors?)
  -> it is 9025 because its main feature is meter
  **The Vague Input**: "High-grade industrial polymers for medical 3D printing." (Requires autonomous recursive search for chemical composition).
  **The Multi-Component**: "Electric vehicle charging station with integrated advertising LED display."

## Pareto Frontier Evaluation

| Model                        | Latency           | accuracy | Token cost/permit   |
| ---------------------------- | ----------------- | -------- | ------------------- |
| cloud openai gpt4o           | 125s              |          | 5700 token/$0.0108  |
| cloud llama3.3-70b-versatile | 110s              |          | 27900 token/$0.00   |
| local llama3.1 8b            | 112s              |          | 41000 token (local) |
| local llama3 groq tool use   | 117s              | High     | 13200 token (local) |
| local mistral 7b             | Cannot call tools |
