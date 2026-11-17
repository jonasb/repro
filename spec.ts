import { always } from "@antithesishq/bombadil";
import { extract } from "@antithesishq/bombadil/browser";
export { clicks } from "@antithesishq/bombadil/browser/defaults/actions";

const result = extract((state) => state.document.querySelector("#result")?.textContent ?? "");

export const workerRuns = always(() => !result.current.startsWith("worker failed"));
