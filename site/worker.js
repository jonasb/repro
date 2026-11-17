// Loads shared.js on demand, as a highlighter loads a language when asked to, and reports a
// failure back to the page, as a worker pool does.
self.onmessage = async () => {
  try {
    const { double } = await import("./shared.js");
    self.postMessage(`worker says ${double(21)}`);
  } catch (error) {
    self.postMessage(`worker failed: ${error}`);
  }
};
