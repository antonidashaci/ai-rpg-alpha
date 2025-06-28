# Scene 01 – Prologue: Whispers at Midnight

**Location**: Duskwind Marches – a moss-covered causeway outside the hamlet of Ravenrest.

**Opening Blurb** (English)
> Midnight fog coils over the cobblestones as you kneel before an obsidian monolith half-buried in reeds.  A tremor ripples through the air—the stone hums like distant harp strings tuned to a dying star.  Your breath turns to frost despite summer heat, and a single phrase crawls inside your skull: *"They are hungry still…"*

**Branching Choices**
1. *Reach out and touch the stone* → Ability check – WIS save (DC 12).  
   • Success → Node `scene_01_touch_success`  
   • Fail    → Node `scene_01_touch_fail`
2. *Study the runes without touching* → INT (Arcana) check (DC 14) → `scene_01_study`  
3. *Back away silently* → Stealth DEX check (DC 10) → `scene_01_withdraw`

**Flags & Effects**
* On any **success**, set `$has_obelisk_vision = true`.
* On **fail**, apply status `Lingering Dread` (−1 to next WIS check).

---
### Localisation Keys (lang/en.yml)
```
scene_01.opening: "Midnight fog coils over the cobblestones…"
scene_01.choice.touch: "Reach out and touch the stone"
scene_01.choice.study: "Study the runes without touching"
scene_01.choice.withdraw: "Back away silently"
```

---
*File created: 29-Jun-2025 – Author: AI* 