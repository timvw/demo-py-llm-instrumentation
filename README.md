# demo-py-llm-instrumentation

Run [phoenix](https://github.com/Arize-ai/phoenix) server to observe your application:

```bash
 rye run arize-phoenix serve
```

Now you can browse to http://0.0.0.0:6006 and find the following:

![screenshot of empty phoenix project](./images/empty.png)

Create a .env file by copying [.env.example](.env.example) and adapting the values.

Now run a sample application:

```bash
rye run python -m demo.01_openai_chat
```