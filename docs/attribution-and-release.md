# Attribution and permitted-output review

Checked 8 November 2026. This record documents source requirements; it is not a legal opinion or a claim of provider approval of this project.

The [provider README](https://github.com/statsbomb/open-data) requests that public research, analysis and insights identify StatsBomb as the data source and use the official logo. Its media-pack link redirects to the Hudl Bynder collection. The selected white logo is marked External Use Approved. It is now displayed persistently in the dashboard sidebar and in Methods & coverage; provenance is recorded in assets/ATTRIBUTION.md.

The [user agreement](https://github.com/statsbomb/open-data/blob/master/LICENSE.pdf) permits research and sharing analytical conclusions while restricting redistribution of underlying data and commercial exploitation of both data and derived analysis. The agreement also asks users to register their interest through the provider website. No registration, terms acceptance, communication or public submission was performed in this task.

Release design: publish project-authored code and narrative findings, plus the official attribution asset. Do not commit raw JSON, source audit files, SQLite databases, or caches. A future host should retrieve the pinned data directly from the source into its private runtime. Serve analytical views, not a raw-event API or source-file download. Team/player summaries are analytical aggregations; this interpretation does not grant blanket rights to redistribute provider data. Keep use noncommercial. If the intended hosting or use changes, reassess the agreement before release.

GitHub source publication was authorized on 8 November 2026. No application deployment, account registration or provider endorsement is claimed. The GitHub connection must be verified at that point. Any provider logo accompanying exported portfolio figures must remain legible; screenshots taken before attribution was added are superseded by the review captures.
