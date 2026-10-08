export class A {
  pub(x: number): string {
    if (x === 0) return "a";
    if (x === 1) return "b";
    if (x === 2) return "c";
    if (x === 3) return "d";
    if (x === 4) return "e";
    return "f";
  }

  #priv(x: number): string {
    if (x === 0) return "a";
    if (x === 1) return "b";
    if (x === 2) return "c";
    if (x === 3) return "d";
    if (x === 4) return "e";
    return "f";
  }

  callPriv(x: number): string {
    return this.#priv(x);
  }
}
