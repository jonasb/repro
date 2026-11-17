// Serves site/ on http://127.0.0.1:8765.
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join } from "node:path";

const root = new URL("./site/", import.meta.url).pathname;
const types = { ".html": "text/html", ".js": "text/javascript" };

createServer(async (request, response) => {
  const path = new URL(request.url, "http://localhost").pathname;
  const file = join(root, path === "/" ? "index.html" : path);
  try {
    const body = await readFile(file);
    response.writeHead(200, { "Content-Type": types[extname(file)] ?? "application/octet-stream" });
    response.end(body);
  } catch {
    response.writeHead(404).end();
  }
}).listen(8765, "127.0.0.1", () => console.log("Serving http://127.0.0.1:8765"));
