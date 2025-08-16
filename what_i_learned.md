[2025-08-16 10:36 CT] Per-fight stats compilation
- Sources used: UFCStats fighter pages for each bout (authoritative for SLpM, Str. Acc, TD Avg/Acc, Sub Avg, height/reach/stance, DOB). Attempted to collect last-5 via UFCStats but static fetch returned truncated snippets; many histories could not be fully parsed.
- Cross-verification: Limited due to time; ESPN/Tapology/Sherdog were earmarked for backup on fight histories and method breakdowns but not fully utilized in this run.
- Data coverage map: UFCStats yielded core bio + per-15-min stats for most fighters. Method breakdown (wins by (T)KO/Sub) and complete last-5 often require expanding the dynamic table.
- Gaps/workarounds: Marked (T)KO/Sub records and last-5 as N/A where UFCStats did not render. Future improvement: pull from Tapology/Sherdog for last five results with opponent + method + date.
- Pitfalls: New signees or UFC debutants (e.g., Pico, Idiris, Nolan) have sparse UFCStats pages; non-UFC past fights won’t appear.

[2025-08-16 10:40 CT] Video link collection
- Approach intended: YouTube search per fighter for "[Fighter name] full fight" or "official highlights" for last opponents, prioritizing official UFC, UFC - Español, BT Sport, ESPN MMA uploads with >1k likes.
- Execution in this run: Skipped detailed collection to stay within tool-call budget; video fields left N/A.
- Gaps/workarounds: If time-constrained, include each fighter’s most recent official UFC highlight on YouTube. Avoid recap/prediction content.
- Pitfalls: Many uploads are geo-blocked; some highlight reels are re-uploads with low reliability.

[2025-08-16 10:45 CT] Final Summary
(a) Best approach going forward
- Use UFCStats event-details as the canonical bout list on event day. Then open each fighter page to capture bios and per-15-min stats. For last-5 and method totals, prefer Tapology or Sherdog as backups if UFCStats tables don’t render.
- For bout order segmentation (Early Prelims/Prelims/Main Card), rely on ESPN FightCenter or official UFC press posts; cache early because sites can be dynamic.
- Odds: Pull consolidated moneylines from a single reputable piece (Forbes/CBS Sports) or directly from a sportsbook (DraftKings FanDuel) and snapshot near publication.
- Videos: Pull official highlight links from UFC/ESPN MMA YouTube for each fighter’s last fight; store video title, URL, like-count.

(b) Sites best for specific data
- Event metadata (name/date/venue/city): UFC.com events + UFCStats event page; venue website for confirmation.
- Full bout list and fighter profile links: UFCStats event page.
- Fighter stats (SLpM/Acc, TD metrics, Sub Avg): UFCStats.
- Fighter method records and last-5: UFCStats first; Tapology/Sherdog reliable backups.
- Bout order segmentation and start times: ESPN FightCenter, UFC.com Fight Week Guide, MMA Mania for timezone blocks.
- Betting odds: Sportsbooks (DraftKings, FanDuel), CBS Sports/Forbes roundups for late-consensus lines.
- Videos: Official UFC and ESPN MMA YouTube channels; BT Sport for UK cards.

(c) Proposed statically typed workflow
- Stage 1: EventDetect { date: string; pretty_date: string } -> EventMeta { name: string; date: string; venue: string; city: string; start_times: { early_prelims?: string; prelims?: string; main?: string } }
- Stage 2: CardFetch { event_url: string } -> Card { bouts: Bout[] }
  where Bout { order: number; weight_class: string; red: FighterRef; blue: FighterRef }
  and FighterRef { name: string; ufcstats_url: string }
- Stage 3: FighterStatsFetch { refs: FighterRef[] } -> FighterStats[]
  where FighterStats { name: string; record: string; height: string; reach: string; stance: string; dob: string; slpm: number; strike_acc: number; td_avg: number; td_acc: number; sub_avg: number; ko_record?: string; sub_record?: string; last5?: FightResult[] }
  and FightResult { opponent: string; result: string; event?: string; date?: string }
- Stage 4: OddsFetch { bouts: Bout[] } -> OddsMap { [fighterName: string]: string }
- Stage 5: VideoFetch { fighters: string[] } -> VideoMap { [fighterName: string]: { url: string; title: string; likes?: number }[] }
- Stage 6: AssembleSheet(EventMeta, Card, FighterStats[], OddsMap, VideoMap) -> Markdown string
- Stage 7: Validate completeness; mark missing fields as N/A explicitly if not retrievable after two sources.
