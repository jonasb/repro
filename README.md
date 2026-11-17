# Bombadil: instrumented scripts throw `window is not defined` in a web worker

When a module web worker loads a script with dynamic `import()`, Bombadil intercepts that request and instruments the script for coverage. The instrumented script starts with `window.__bombadil__ = …`, and a worker has no `window`, so the import fails with `ReferenceError: window is not defined`. The same page works without Bombadil, and with Bombadil when file instrumentation is off.

Reproduced with Bombadil 0.7.10 (latest on npm), on macOS arm64 with its bundled Chromium.

## Steps

```bash
pnpm install
pnpm serve              # serves site/ on http://127.0.0.1:8765 (keep it running)
pnpm test               # bombadil browser test --headless --time-limit 10s --exit-on-violation http://127.0.0.1:8765/ spec.ts
pnpm test:inline-only   # the same with --instrument-javascript inline
```

`site/index.html` has a "Start worker" button. A click starts `site/worker.js` as a module worker and sends it a message. The worker loads `site/shared.js` with `await import("./shared.js")` and posts the result back, or `worker failed: <error>` if the import throws. The page shows that in `#result`.

`spec.ts` exports Bombadil's default `clicks` and one property, `workerRuns`: `#result` never starts with `worker failed`.

## Expected

The worker imports `shared.js` and the page shows `worker says 42`, as it does in a browser without Bombadil.

## Actual

`pnpm test` fails on the first click:

```text
workerRuns was violated:

as of 00:00.000, it should always be the case that () => !result.current.startsWith("worker failed"), however at 00:00.057, result = "worker failed: ReferenceError: window is not defined"
```

`pnpm test:inline-only` (file instrumentation off) passes: about 280 clicks in 10 seconds, each showing `worker says 42`.

## Cause

With `RUST_LOG=bombadil_browser::browser::instrumentation=debug`, every click logs

```text
intercepted and instrumented request: http://127.0.0.1:8765/shared.js
```

So the worker's dynamic import is intercepted and instrumented, while the worker's own script, `worker.js`, is never intercepted. The instrumentation prepends a prelude that reads and writes `window`:

```js
window.__bombadil__ = window.__bombadil__ || {
        edges_previous: new Uint8Array(65536),
        edges_current: new Uint8Array(65536),
        previous: 0,
```

In a dedicated, shared or service worker the global object is not `window`, so the prelude throws before the module runs. `globalThis.__bombadil__` would work in both windows and workers. Alternatively, scripts a worker requests could be left uninstrumented, as the worker's own script already is.

## Where this came from

An app that highlights code in a pool of module workers (`@pierre/diffs`, which loads grammars on demand). Under Bombadil the workers intermittently failed to initialize with `window is not defined` at line 1, column 1 of a chunk they import.
