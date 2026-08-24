# Requirement ID Migration

[Overview](../../README.md) · [Requirements](requirements.md) · [Reference index](README.md)

Model version `0.9.0-baseline-candidate` replaced category-bearing requirement identifiers with neutral stable keys. Requirement wording, intent, classification, applicability, allocation, verification state, gaps, and approval state did not change because of the migration.

The former deferred records were moved out of the requirements collection. They now use `DEF-*` keys in a distinct `deferred_topics` collection.

| Old ID | New ID | Display name | Migration note |
|---|---|---|---|
| REQ-FUN-001 | REQ-001 | Relay outbound traffic | Requirement ID changed |
| REQ-FUN-002 | REQ-002 | Relay return traffic | Requirement ID changed |
| REQ-FUN-003 | REQ-003 | Maintain commanded station position | Requirement ID changed |
| REQ-FUN-004 | REQ-004 | Accept operator aircraft commands | Requirement ID changed |
| REQ-FUN-005 | REQ-005 | Return on low-battery condition | Requirement ID changed |
| REQ-FUN-006 | REQ-006 | Inhibit arming in Ground Safe | Requirement ID changed |
| REQ-FUN-007 | REQ-007 | Recover after payload loss | Requirement ID changed |
| REQ-FUN-008 | REQ-008 | Provide mode and health/status | Requirement ID changed |
| REQ-PER-001 | REQ-009 | Limit system unit cost | Requirement ID changed |
| REQ-PER-002 | REQ-010 | Provide on-station endurance | Requirement ID changed |
| REQ-PER-003 | REQ-011 | Limit system gross mass | Requirement ID changed |
| REQ-PER-004 | REQ-012 | Accommodate payload envelope | Requirement ID changed |
| REQ-PER-005 | REQ-013 | Enable single-operator deployment | Requirement ID changed |
| REQ-IFC-001 | REQ-014 | Standardize payload mount | Requirement ID changed |
| REQ-IFC-002 | REQ-015 | Provide regulated payload power | Requirement ID changed |
| REQ-IFC-003 | REQ-016 | Limit platform-to-payload interfaces | Requirement ID changed |
| REQ-IFC-004 | REQ-017 | Retain payload under flight loads | Requirement ID changed |
| REQ-SAF-001 | REQ-018 | Protect and retain battery | Requirement ID changed |
| REQ-SAF-002 | REQ-019 | Indicate armed state to operator | Requirement ID changed |
| REQ-CON-001 | REQ-020 | Prefer commercial components | Requirement ID changed |
| REQ-CON-002 | REQ-021 | Use open-source flight firmware | Requirement ID changed |
| REQ-CON-003 | REQ-022 | Exclude weapons and munitions | Requirement ID changed |
| REQ-CON-004 | REQ-023 | Avoid continuous-GNSS dependency | Requirement ID changed |
| REQ-DEF-001 | DEF-001 | Define RF implementation | Moved to deferred topics |
| REQ-DEF-002 | DEF-002 | Define antenna characteristics | Moved to deferred topics |
| REQ-DEF-003 | DEF-003 | Obtain spectrum authorization | Moved to deferred topics |
| REQ-DEF-004 | DEF-004 | Define contested-spectrum resilience | Moved to deferred topics |
| REQ-DEF-005 | DEF-005 | Complete export-control review | Moved to deferred topics |

Legacy IDs are prohibited in the active structured model and generated views. This mapping is the normal live-documentation exception.
