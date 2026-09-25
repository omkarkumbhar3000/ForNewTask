/**
 * Shape contracts for the data layer, as JSDoc typedefs.
 *
 * These describe what `tools/obj015_build_dashboard_data.py` emits. The app is
 * plain JSX rather than TypeScript, so these are documentation plus editor hints — but they
 * are the authority on what a page may assume. Any numeric field can also be the string
 * "N/A": that means the figure was never measured, and the UI must render an empty state
 * rather than a zero.
 */

/**
 * @typedef {number|"N/A"} Measured
 * A measured number, or "N/A" when the run never captured it.
 */

/**
 * @typedef {Object} Run
 * @property {string}   id                 Run folder stamp, e.g. "2026-08-05_114315".
 * @property {string}   date               ISO date part of the stamp.
 * @property {string}   projectId
 * @property {string}   type               Human classification of what the run was.
 * @property {string}   status             "Complete" | "Aborted" | …
 * @property {string}   environment
 * @property {Measured} flows
 * @property {Measured} total              Test cases reached.
 * @property {Measured} executed           Passed + failed. Excludes withheld.
 * @property {Measured} passed
 * @property {Measured} failed
 * @property {Measured} blocked            Withheld at call time by a safety guard.
 * @property {Measured} successRate        Test-case level, percent.
 * @property {Measured} durationMin
 * @property {string}   durationBasis      Where the duration figure came from.
 * @property {Measured} distinctEndpoints
 * @property {Measured} latencyMeanMs
 * @property {Measured} latencyMedianMs
 * @property {Measured} latencyP95Ms
 * @property {number}   findings           Findings sourced from this run's evidence.
 * @property {number}   evidenceFiles
 * @property {string}   runFolder          Workspace-relative path.
 * @property {boolean}  isBaseline         True for the N-1 comparison run.
 * @property {boolean}  isCurrent          True for the latest substantive run (N).
 * @property {boolean}  substantive        False for probes and aborted runs.
 */

/**
 * @typedef {Object} KpiTile
 * @property {string}   id
 * @property {string}   label
 * @property {Measured} value
 * @property {Measured} previous
 * @property {string}   unit
 * @property {"up-good"|"down-good"|"neutral"} direction  Which way is good.
 * @property {string}   hint
 */

/**
 * @typedef {Object} BenchmarkMetric
 * @property {string}       metric
 * @property {boolean}      indent      Sub-row of the metric above it.
 * @property {string}       previous    Display string, may be "N/A".
 * @property {string}       current
 * @property {string}       delta
 * @property {string}       note
 * @property {string}       group
 * @property {number|null}  previousNum Numeric form, or null if not a number.
 * @property {number|null}  currentNum
 */

/**
 * @typedef {Object} Finding
 * @property {string}      id
 * @property {string}      title
 * @property {string}      priority
 * @property {string}      severityLabel  Original wording from the source document.
 * @property {"Critical"|"High"|"Medium"|"Low"|"Informational"} severity  Normalised bucket.
 * @property {string}      effort
 * @property {string}      scope          The measured scope of the finding.
 * @property {string|null} jira           Ticket key when raised.
 * @property {string}      status         "Raised" | "Not raised" | source wording.
 * @property {string}     [remediation]
 * @property {string}     [impact]
 */

/**
 * @typedef {Object} FindingSet
 * @property {string}    id
 * @property {string}    name
 * @property {string}    description
 * @property {string}    source          Workspace-relative path this set was read from.
 * @property {Finding[]} items
 * @property {{severity:string,count:number}[]} severityRollup
 * @property {number}    total
 * @property {number}    raised
 */

/**
 * @typedef {Object} Gap
 * @property {string} item         What is missing.
 * @property {string} why          Why it is missing.
 * @property {string} wouldClose   What would produce it.
 */

export {}
