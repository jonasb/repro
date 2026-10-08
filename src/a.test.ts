import { expect, test } from "vitest";
import { A } from "./a.ts";

test("every branch of pub and #priv", () => {
  const a = new A();
  const seen = new Set<string>();
  for (let i = 0; i < 8; i++) {
    seen.add(a.pub(i));
    seen.add(a.callPriv(i));
  }
  expect([...seen].sort()).toEqual(["a", "b", "c", "d", "e", "f"]);
});
