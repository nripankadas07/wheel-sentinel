# User brief and comparison

**User:** Python maintainer validating a wheel before sharing it.

**Pain:** Source tests do not prove archive paths, RECORD hashes or artifact completeness; extracting an unreviewed archive risks unsafe paths.

**Need:** Inferred artifact validation need, not verified customer demand or claims about competitor omissions.

**Capability:** Bounded ZIP inspection without extraction, unsafe path/symlink detection and RECORD hash/size verification.

**Acceptance:** Valid artifact, tampered bytes, traversal without extraction, missing RECORD and decompressed-size budget.

**Discovery:** Python wheel release checklists.

**Portfolio:** agent-sbom analyzes agent capabilities and dep-audit scans advisories. Neither verifies the bytes and member paths inside a wheel.


## Search coverage

GitHub query `wheel check in:name,description`, sorted by stars descending; observation 2026-10-04T12:43:43.256298+00:00. The top ten search results were screened for relevance. Search is not an exhaustive global ranking. Established comparables outside that query were also inspected; highest-star relevant comparable found among this researched set is identified below. Stars are research context, not technical performance.

Highest-star relevant comparable found: [pypa/twine](https://github.com/pypa/twine), 1790 stars.

| Comparable | Stars | Last push UTC | License | Workflow and tradeoff |
| --- | ---: | --- | --- | --- |
| [jwodder/check-wheel-contents](https://github.com/jwodder/check-wheel-contents) | 169 | 2026-07-20T12:44:47Z | MIT | Wheel content lint rules and a documented pip workflow; open issue 52 requests RECORD checking. This project focuses on bounded archive paths and RECORD integrity. |
| [pypa/twine](https://github.com/pypa/twine) | 1790 | 2026-10-01T19:56:02Z | Apache-2.0 | Package publishing and metadata workflow with established docs; no publishing or registry access in this MVP. |
| [mgedmin/check-manifest](https://github.com/mgedmin/check-manifest) | 293 | 2026-08-04T18:39:30Z | MIT | Source distribution manifest consistency; artifact byte verification is a separate task. |

README installation and example workflows and available recent issues were inspected. Push time does not prove active support, and mature alternatives cover broader domains. No competitor installations or equivalent performance workloads were measured. Time to first result and runtime performance comparisons are unmeasured. Tests prove only this implementation. Demand is inferred unless an issue is linked explicitly; no users, adoption or results are fabricated.

Related verified issue title: [RECORD check ?](https://github.com/jwodder/check-wheel-contents/issues/52). This is evidence of a related question, not a request for this project or proof of current competitor behavior.
