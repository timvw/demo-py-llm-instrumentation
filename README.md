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

Install instrumentation package(s):

```bash
rye add openinference-instrumentation-openai
```

Use [opentelemetry-instrument](https://opentelemetry.io/docs/languages/python/getting-started/#run-the-instrumented-app) to launch the sample aplication:

```bash
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
rye run opentelemetry-instrument \
    --service_name demo \
    --traces_exporter otlp \
    --exporter_otlp_endpoint 0.0.0.0:4317 \
    --exporter_otlp_traces_insecure true \
    python -m demo.01_openai_chat
```

And now you can observe the traces in Phoenix:

![screenshot of traces in phoenix](./images/openai-traces.png)

