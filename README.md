# fallow: `#private` class methods never get Istanbul coverage

`fallow health --coverage` never uses the coverage map for an ECMAScript private method (`#priv()`). It always falls back to the static estimate (`coverage_source: "estimated"`), even when the method is fully covered by tests. A public method with the same body in the same class is matched and scored from the map.

Reproduced with fallow 3.30.0 and 3.32.0 (latest on npm), with vitest 4.1.11 and `@vitest/coverage-v8` 4.1.11.

## Steps

```bash
pnpm install
pnpm coverage   # vitest --run --coverage (v8 provider, json reporter)
pnpm health     # fallow health --coverage coverage/coverage-final.json --max-crap 5 --max-cyclomatic 3 --format json
```

`src/a.ts` has a class with `pub(x)` and `#priv(x)`, each a 6-way `if` chain, and `callPriv(x)`, which calls `#priv`. `src/a.test.ts` calls `pub` and `callPriv` for 0..7, so every branch of both methods runs.

## Expected

`#priv` is scored from the map like `pub`: `coverage_pct: 100`, `coverage_source: "istanbul"`, CRAP 6.0.

## Actual

```text
pub    line 2   coverage_pct 100.0  coverage_source istanbul   crap 6.0
#priv  line 11  coverage_pct (none) coverage_source estimated  crap 13.8
```

## The coverage map does record the method

v8 coverage converted by v8-to-istanbul (what `@vitest/coverage-v8` writes) records the private method as an anonymous entry at the method's own position, with its call count:

```text
pub            decl 2:2-2:6    loc.start 2:25   calls 8
(anonymous_1)  decl 11:2-11:8  loc.start 11:27  calls 8
callPriv       decl 20:2-20:11 loc.start 20:30  calls 8
```

Renaming that entry to `#priv` in `coverage-final.json` does not change the result.

## Cause

`IstanbulFileCoverage::lookup_function` (`crates/engine/src/health/scoring.rs`) returns `None` for every unit with `is_private_member` set, before any name or position matching runs. The rule came in 3.21.0 (fallow-rs/fallow#2448, "Private class members no longer take coverage from the function that encloses them"), whose changelog entry says "No instrumenter records a `#member` in its function map". v8-to-istanbul does record one, as `(anonymous_N)` at the member's own `decl` position, so the anonymous positional fallback that already serves arrow functions would find the right entry. For comparison, renaming `pub`'s entry to `(anonymous_0)` still matches through that fallback.

So a codebase that keeps its logic in `#private` methods sees every one of them scored as if untested, however well it is covered.
