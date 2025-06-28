# Lore Bible – Realm of Umbraterra  
*(WIP – PRD v2 path)*

---
## 1. Cosmology & Setting
Umbraterra is a single, moon-shrouded continent floating on a prime material plane. Celestial bodies are dim; twin crescent moons drift across a violet sky. Ancient legends speak of a **" first sundering"** in which time itself fractured, leaving scars—today manifested as **Obelisks of Echoing Stone**.

**Time Eaters** («Chronovores») lurk beyond the Veil, feeding on temporal currents. When an obelisk awakens (marked by a chorus of whispered clocks), a breach opens and Chronovores spill into reality, devouring memories, ageing forests overnight or reversing rivers' flow.

---
## 2. Geography – Eight Sovereignties
| # | Realm | Alignment flavour | One-line description |
|---|-------|-------------------|-----------------------|
| 1 | **Valakar Dominion** | Lawful Neutral | Imperial heartland of marble forums and iron-willed legions.
| 2 | **Duskwind Marches** | Chaotic Neutral | Fog-drenched wetlands where smugglers and freedom cults thrive.
| 3 | **Ashenreach Wastes** | Lawful Evil | Volcanic badlands ruled by drake-taming warlords.
| 4 | **Hollowveil Kingdom** | Neutral Good | Misty highlands blessed by silver-leaf oaks and wandering spirits.
| 5 | **Stormglen Isles** | Chaotic Good | Seafaring republic of corsairs and storm-priests.
| 6 | **Miridorn Highlands** | Lawful Good | Stout dwarf-holds; rune-forges hum beneath snow peaks.
| 7 | **Thaloria Grove** | Chaotic Good | Twilight forest where elder elves guard world-roots.
| 8 | **Umbral Court** | Neutral Evil | Shadow-swallowed city where echoes rule in place of people.

Travel between realms is perilous; caravan seasons and political tensions act as soft gates for branching quests.

---
## 3. Magic System (Skyrim-inspired Schools)
| School | Essence | Example Spells (Novice→Master) |
|--------|---------|---------------------------------|
| **Destruction** | Elemental force | Ember Dart → Frost Lance → Storm Pillar → Cataclysm Strike |
| **Restoration** | Vital mending | Mend Flesh → Purge Toxin → Revive → Aegis of Dawn |
| **Illusion** | Mind & senses | Candleglow → Muffle Step → Phantasmal Army → Dark Mirror |
| **Conjuration** | Summoning, binding | Spirit Spark → Bonehand → Rift Guardian → Nether Legion |
| **Alteration** | Matter & time | Featherweight → Ironhide → Warp Step → Sundry of Seconds |
| **Enchanting** | Item infusion | Sigil Mark → Echo Glyph → Soul Vow → Eternity Seal |

Ranks: **Novice ⮕ Apprentice ⮕ Adept ⮕ Expert ⮕ Master**.  Learning requires trainers, grimoires, or risking obelisk whispers.

---
## 4. Playable Classes & Backgrounds
* **Swordsman** – Weapon master; battle stances.  
* **Wizard** – Any magic school; fragile but versatile.  
* **Rogue** – Stealth, locks, critical strikes.  
* **Cleric** – Restoration & light, channel divinity.  
* **Ranger** – Ranged precision, animal link.  
* **Occultist** (unlock) – Obelisk-born; manipulates time shards.

### Background Generator (player chooses one)
| Origin | Hook | Example attribute perk |
|--------|------|------------------------|
| Exiled Noble | Usurped by kin | +1 CHA, bonus purse |
| Haunted Scholar | Obelisk visions since childhood | +1 INT, free "Candleglow" |
| Mercenary Drifter | Fought in Ashenreach sieges | +1 STR, cheap armour |
| Grove Acolyte | Raised by Thaloria druids | +1 WIS, animal empathy |
| Void Orphan | Found at a dormant obelisk | +1 DEX, detect obelisks |

Character creation flow: Background → Class → Auto-set base attributes per class, then 2 discretionary points.

---
## 5. Factions (4 Orders + 4 Cults)
| Name | Alignment | Goal |
|------|-----------|------|
| **Order of the Silver Flame** | LG | Seal obelisks, purge undeath |
| **Chronomancers' Conclave** | LN | Study time fractures, morally grey |
| **Ironblood Free Company** | CN | Profit off chaos, sellswords |
| **Veil Walkers Guild** | CG | Smuggle refugees across realms |
| **Nightshade Cabal** | CE | Harness obelisks to rewrite fate |
| **Eclipse Choir** | NE | Worship Chronovores, spread entropy |
| **Red Ember Sect** | LE | Draconic supremacy, forge war golems |
| **Whispered Hand** | N  | Information brokers; neutrality facade |

---
## 6. Alignment & Karma
Double axis **Law (-5) ↔ Chaos (+5)**, **Evil (-5) ↔ Good (+5)**.  Faction quests and critical choices shift values.  Thresholds: ±3 alters NPC stance; ±5 locks/unlocks realm areas.

---
## 7. Quest Framework
* **Main Arcs (4)**  
  1. *Shards of the First Sundering* – locate obelisk inscriptions.  
  2. *Echoes in Hollowveil* – time-looped plague mystery.  
  3. *Drakefire Rebellion* – Ashenreach war escalation.  
  4. *Siege of the Shadow Court* – political intrigue in Umbral Court.
* **Final Threat** – Confront **Time Eaters** once ≥80 % quest progress.
* **Endings** – 3 major (Seal, Bargain, Devour) + 2 hidden (Ascend, Collapse).

---
## 8. Dynamic World Counters
* **Obelisk Resonance** (global %) – ticks up daily; higher means stronger anomalies.  
* **War Momentum** (Ashenreach ↔ Valakar) – changes via events; affects borders.

---
## 9. Visual & Audio Style
* **Art** – Dark-fantasy, semi-realistic, corrupted textures (see sample portrait). Prompt archetype: "oil-on-canvas, muted violets, eldritch cracks".  
* **Music** – Orchestral strings with low drone (Expedition 33 mood). Event/location specific tracks.

---
## 10. Translation Strategy
All narrative text externalised to YAML under `lang/en.yml`, keyed per passage.  Twine nodes use `[[passage-id]]` look-ups to engine-side localisation.

---
*(End of draft.  Edits/additions welcome.)* 