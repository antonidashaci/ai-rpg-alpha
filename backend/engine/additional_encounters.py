"""
Additional Combat Encounters for The Northern Realms
===================================================

More diverse and challenging combat encounters:
- Ancient guardians and magical constructs
- Mercenary bands and elite soldiers
- Magical anomalies and summoned creatures
- Environmental hazards and survival encounters
- Boss-level threats and epic confrontations
"""

from typing import Tuple, List
from .combat_system import Enemy, EnvironmentalFeature, TerrainType
from .fantasy_encounters import FantasyEncounters


class AdditionalEncounters:
    """Library of additional combat encounters"""

    @staticmethod
    def ancient_guardian() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Ancient Guardian - Magical construct defender
        A combat encounter featuring an ancient magical guardian
        """
        enemies = [
            Enemy(
                name="Ancient Stone Guardian",
                health=80,
                max_health=80,
                attack_power=18,
                defense=6,
                intelligence=8,
                morale=100  # Constructs don't flee
            )
        ]

        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Ancient Runes",
                description=(
                    "Glowing runes on the chamber walls. Disrupting them could weaken the guardian, "
                    "but might trigger magical backlash."
                ),
                is_destructible=True,
                damage_potential=25,
                uses_remaining=3
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Unstable Magic",
                description=(
                    "The air shimmers with unstable magical energy. "
                    "This could be weaponized against the guardian."
                ),
                damage_potential=20,
                uses_remaining=2
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Stone Pillars",
                description="Massive stone pillars provide excellent cover from magical attacks.",
                provides_cover=True
            )
        ]

        context = (
            "🏛️ **ANCIENT GUARDIAN**\n\n"
            "You stand in a chamber that hasn't seen visitors in centuries. "
            "At the far end, a massive stone guardian stirs to life, its eyes glowing "
            "with ancient magic. Runes along its body pulse with power.\n\n"
            "'INTRUDERS DETECTED,' it booms in a voice like grinding stone. "
            "'YOU SHALL NOT PASS. THE SECRETS OF THIS PLACE REMAIN HIDDEN.'\n\n"
            "This guardian has protected these ruins for longer than any kingdom has existed. "
            "Its magic is ancient and powerful, but ancient magic can be unpredictable."
        )

        return enemies, environment, context

    @staticmethod
    def mercenary_band() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Elite Mercenary Band - Professional soldiers for hire
        A combat encounter with skilled, well-equipped mercenaries
        """
        enemies = [
            Enemy(
                name="Mercenary Captain",
                health=45,
                max_health=45,
                attack_power=16,
                defense=4,
                intelligence=12,
                morale=85
            ),
            Enemy(
                name="Elite Mercenary",
                health=35,
                max_health=35,
                attack_power=14,
                defense=3,
                intelligence=8,
                morale=75
            ),
            Enemy(
                name="Elite Mercenary",
                health=35,
                max_health=35,
                attack_power=14,
                defense=3,
                intelligence=8,
                morale=75
            ),
            Enemy(
                name="Mercenary Archer",
                health=25,
                max_health=25,
                attack_power=12,
                defense=2,
                intelligence=9,
                morale=70
            )
        ]

        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Barricades",
                description="The mercenaries have set up defensive barricades for cover.",
                provides_cover=True
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Supply Wagon",
                description=(
                    "A wagon loaded with supplies. Destroying it could create chaos "
                    "and force the mercenaries to break formation."
                ),
                is_destructible=True,
                damage_potential=20,
                uses_remaining=1
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.ELEVATED,
                name="Hill Overlook",
                description="Higher ground provides tactical advantage and better visibility.",
                elevation_bonus=2
            )
        ]

        context = (
            "⚔️ **ELITE MERCENARIES**\n\n"
            "A band of elite mercenaries blocks your path. Their captain, a scarred veteran "
            "with cold eyes, assesses you professionally.\n\n"
            "'Well now,' he says with a mercenary's grin. 'You look like you might be worth "
            "something. Hand over your valuables and we'll let you pass. Or don't - makes no "
            "difference to us.'\n\n"
            "These are professionals - well-trained, well-equipped, and utterly without mercy. "
            "They fight for gold, not glory, which makes them both predictable and dangerous."
        )

        return enemies, environment, context

    @staticmethod
    def magical_anomaly() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Magical Anomaly - Unstable magical phenomenon
        A combat encounter with magical instability and summoned creatures
        """
        enemies = [
            Enemy(
                name="Arcane Horror",
                health=40,
                max_health=40,
                attack_power=15,
                defense=2,
                intelligence=5,
                morale=100  # Magical constructs
            ),
            Enemy(
                name="Mana Elemental",
                health=30,
                max_health=30,
                attack_power=12,
                defense=4,
                intelligence=3,
                morale=100
            ),
            Enemy(
                name="Spell Aberration",
                health=25,
                max_health=25,
                attack_power=10,
                defense=1,
                intelligence=2,
                morale=100
            )
        ]

        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Mana Storm",
                description=(
                    "Unstable magical energy swirls through the area. "
                    "This could be directed against the anomalies."
                ),
                damage_potential=30,
                uses_remaining=3
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Focusing Crystals",
                description=(
                    "Large crystals that focus magical energy. "
                    "Destroying them could disrupt the anomalies' power source."
                ),
                is_destructible=True,
                damage_potential=25,
                uses_remaining=2
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Stone Formations",
                description="Natural stone formations provide cover from magical attacks.",
                provides_cover=True
            )
        ]

        context = (
            "✨ **MAGICAL ANOMALY**\n\n"
            "The air crackles with unstable magic. What should be solid ground shimmers "
            "and warps as if reality itself is breaking down. Strange creatures of pure "
            "magical energy manifest and attack.\n\n"
            "This place has been corrupted by wild magic - spells gone wrong, experiments "
            "that escaped their creators' control. The magical anomalies don't think or feel, "
            "but they react to magical energy with terrifying power.\n\n"
            "Your own magic could be a liability here. The wild magic might turn your spells "
            "against you, or amplify them beyond control."
        )

        return enemies, environment, context

    @staticmethod
    def frost_elemental() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Frost Elemental - Ice and cold themed encounter
        A combat encounter with elemental cold and environmental hazards
        """
        enemies = [
            Enemy(
                name="Greater Frost Elemental",
                health=70,
                max_health=70,
                attack_power=16,
                defense=5,
                intelligence=6,
                morale=100  # Elementals don't flee
            ),
            Enemy(
                name="Ice Shard",
                health=20,
                max_health=20,
                attack_power=8,
                defense=8,
                intelligence=2,
                morale=100
            ),
            Enemy(
                name="Ice Shard",
                health=20,
                max_health=20,
                attack_power=8,
                defense=8,
                intelligence=2,
                morale=100
            )
        ]

        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Ice Spikes",
                description=(
                    "Sharp ice formations that can be used as improvised weapons. "
                    "The cold makes them brittle and dangerous."
                ),
                damage_potential=15,
                uses_remaining=4
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Snow Drifts",
                description="Deep snow provides cover but slows movement.",
                provides_cover=True
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Frozen Waterfall",
                description=(
                    "A frozen waterfall that could be shattered to create an avalanche "
                    "or used as a weapon against the elementals."
                ),
                is_destructible=True,
                damage_potential=35,
                uses_remaining=1
            )
        ]

        context = (
            "🧊 **FROST ELEMENTAL**\n\n"
            "The temperature drops suddenly as a massive frost elemental manifests from "
            "the swirling snow. Its body is composed of living ice and driven snow, "
            "crackling with frozen lightning.\n\n"
            "'COLD... SO COLD...' it whispers in a voice like cracking ice. "
            "'JOIN THE FROZEN SILENCE.'\n\n"
            "This creature is born of the deepest winter magic. It radiates cold that "
            "can freeze blood in veins and turn weapons brittle. Fire and heat are "
            "its greatest weaknesses, but in this frozen wasteland, heat is scarce."
        )

        return enemies, environment, context

    @staticmethod
    def shadow_assassins() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Shadow Assassins - Stealth and darkness themed encounter
        A combat encounter with invisible or shadow-based enemies
        """
        enemies = [
            Enemy(
                name="Shadow Master",
                health=40,
                max_health=40,
                attack_power=18,
                defense=3,
                intelligence=14,
                morale=80
            ),
            Enemy(
                name="Shadow Assassin",
                health=25,
                max_health=25,
                attack_power=15,
                defense=2,
                intelligence=10,
                morale=75
            ),
            Enemy(
                name="Shadow Assassin",
                health=25,
                max_health=25,
                attack_power=15,
                defense=2,
                intelligence=10,
                morale=75
            ),
            Enemy(
                name="Shadow Wraith",
                health=30,
                max_health=30,
                attack_power=12,
                defense=4,
                intelligence=6,
                morale=100
            )
        ]

        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Deep Shadows",
                description=(
                    "The shadows here are unnaturally deep. "
                    "The assassins use them for cover and ambush."
                ),
                provides_cover=True
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Darkness Field",
                description=(
                    "An area of supernatural darkness. "
                    "Light sources are dimmed and visibility is reduced."
                ),
                damage_potential=0,
                uses_remaining=0  # Permanent effect
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Light Crystals",
                description=(
                    "Crystals that emit bright light. "
                    "Destroying them increases the darkness but weakens the assassins."
                ),
                is_destructible=True,
                damage_potential=20,
                uses_remaining=3
            )
        ]

        context = (
            "🌑 **SHADOW ASSASSINS**\n\n"
            "Darkness falls unnaturally fast as shadowy figures emerge from the gloom. "
            "The Shadow Master regards you with eyes like bottomless voids.\n\n"
            "'The shadows have marked you for death,' he whispers. 'We are the darkness "
            "that waits for all mortals.'\n\n"
            "These assassins are masters of stealth and shadow magic. They can become "
            "invisible, strike from darkness, and leave no trace. Light is their enemy, "
            "but in this perpetual twilight, light is hard to come by."
        )

        return enemies, environment, context

    @staticmethod
    def corrupted_beast() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Corrupted Beast - Mutated creature encounter
        A combat encounter with a magically corrupted monster
        """
        enemies = [
            Enemy(
                name="Corrupted Behemoth",
                health=90,
                max_health=90,
                attack_power=20,
                defense=7,
                intelligence=4,
                morale=100  # Berserk rage
            )
        ]

        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Corruption Pools",
                description=(
                    "Pools of glowing corruption that spread the magical mutation. "
                    "The beast draws power from them."
                ),
                damage_potential=25,
                uses_remaining=3
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Crystal Growths",
                description=(
                    "Mutated crystals that feed the corruption. "
                    "Destroying them could weaken the beast."
                ),
                is_destructible=True,
                damage_potential=30,
                uses_remaining=2
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Ancient Trees",
                description="Massive trees provide cover from the beast's charges.",
                provides_cover=True
            )
        ]

        context = (
            "🦠 **CORRUPTED BEHEMOTH**\n\n"
            "What was once a mighty forest creature has been twisted by dark magic into "
            "something monstrous. Its flesh pulses with unnatural growths, and its eyes "
            "glow with corrupted power.\n\n"
            "'RAGE... HUNGER... DESTROY...' it bellows in a voice that sounds like "
            "breaking bones and bubbling corruption.\n\n"
            "This poor creature was once a guardian of the forest, but dark magic has "
            "warped it into a engine of destruction. The corruption gives it immense "
            "strength but also makes it vulnerable to purification magic."
        )

        return enemies, environment, context

    @staticmethod
    def storm_elemental() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Storm Elemental - Lightning and wind themed encounter
        A combat encounter with electrical and aerial threats
        """
        enemies = [
            Enemy(
                name="Storm Elemental",
                health=60,
                max_health=60,
                attack_power=17,
                defense=4,
                intelligence=7,
                morale=100
            ),
            Enemy(
                name="Lightning Sprite",
                health=15,
                max_health=15,
                attack_power=10,
                defense=2,
                intelligence=4,
                morale=100
            ),
            Enemy(
                name="Lightning Sprite",
                health=15,
                max_health=15,
                attack_power=10,
                defense=2,
                intelligence=4,
                morale=100
            ),
            Enemy(
                name="Wind Wisp",
                health=20,
                max_health=20,
                attack_power=8,
                defense=6,
                intelligence=5,
                morale=100
            )
        ]

        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Lightning Rod",
                description=(
                    "A metal rod that attracts lightning. "
                    "Could be used to channel the storm elemental's power against it."
                ),
                damage_potential=35,
                uses_remaining=2
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.ELEVATED,
                name="Hill Top",
                description="Higher ground where the storm is more intense but visibility is better.",
                elevation_bonus=3
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Ancient Oak",
                description=(
                    "A massive tree that could be struck by lightning. "
                    "The elemental seems drawn to it."
                ),
                is_destructible=True,
                damage_potential=25,
                uses_remaining=1
            )
        ]

        context = (
            "⛈️ **STORM ELEMENTAL**\n\n"
            "Thunder crashes as a massive storm elemental manifests from the raging tempest. "
            "Its body is composed of swirling clouds and crackling lightning, eyes like "
            "thunderheads.\n\n"
            "'STORM... WIND... LIGHTNING...' it howls in a voice like rolling thunder. "
            "'ALL WILL BE SWEPT AWAY!'\n\n"
            "This creature is the living embodiment of the storm. It commands wind and "
            "lightning with terrifying power. Metal armor and weapons are dangerous "
            "near it - they attract its electrical fury like lightning rods."
        )

        return enemies, environment, context

    @staticmethod
    def get_all_additional_encounters() -> List[str]:
        """Get list of all additional encounter types"""
        return [
            "ancient_guardian",
            "mercenary_band",
            "magical_anomaly",
            "frost_elemental",
            "shadow_assassins",
            "corrupted_beast",
            "storm_elemental"
        ]

    @staticmethod
    def get_random_additional_encounter() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """Get a random additional encounter"""
        encounters = AdditionalEncounters.get_all_additional_encounters()
        encounter_type = random.choice(encounters)

        # Map encounter types to methods
        encounter_methods = {
            "ancient_guardian": AdditionalEncounters.ancient_guardian,
            "mercenary_band": AdditionalEncounters.mercenary_band,
            "magical_anomaly": AdditionalEncounters.magical_anomaly,
            "frost_elemental": AdditionalEncounters.frost_elemental,
            "shadow_assassins": AdditionalEncounters.shadow_assassins,
            "corrupted_beast": AdditionalEncounters.corrupted_beast,
            "storm_elemental": AdditionalEncounters.storm_elemental
        }

        method = encounter_methods.get(encounter_type)
        if method:
            return method()
        else:
            # Fallback to bandit ambush
            return FantasyEncounters.bandit_ambush()

