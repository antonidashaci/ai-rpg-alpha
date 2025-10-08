"""
Fantasy Combat Encounters for The Northern Realms
==================================================

Epic fantasy encounters featuring:
- Dragon battles
- Orc war parties
- Undead hordes
- Political assassins
- Magical creatures
"""

from typing import Tuple, List
from .combat_system import Enemy, EnvironmentalFeature, TerrainType


class FantasyEncounters:
    """Library of fantasy-themed combat encounters"""
    
    @staticmethod
    def dragon_encounter() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Epic dragon battle - High difficulty
        
        Solutions:
        - Direct combat (very difficult)
        - Use dragon-slaying ballista
        - Negotiate (high charisma required)
        - Lure into trap using environment
        """
        enemies = [
            Enemy(
                name="Crimsonwing the Red Dragon",
                health=150,
                max_health=150,
                attack_power=25,
                defense=8,
                intelligence=15,
                morale=150,  # Dragons don't flee easily
                position="airborne"
            )
        ]
        
        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Ancient Dragon-Slaying Ballista",
                description=(
                    "A massive ballista from the old dragon wars. One shot could pierce dragon scales, "
                    "but it requires time to reload and aim."
                ),
                is_destructible=False,
                damage_potential=60,
                uses_remaining=2
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.ELEVATED,
                name="Crumbling Tower Ruins",
                description="High ground provides cover from dragon fire and better vantage point.",
                elevation_bonus=3,
                provides_cover=True
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Burning Dragonfire",
                description="Pools of dragon fire from previous attacks. Dangerous but could be weaponized.",
                damage_potential=20,
                uses_remaining=3
            )
        ]
        
        context = (
            "🐉 **DRAGON ENCOUNTER**\n\n"
            "Crimsonwing descends from the skies, wings blotting out the sun. "
            "The ancient red dragon's scales gleam like molten metal. Her roar shakes the very earth.\n\n"
            "'So, the marked one finally arrives,' she rumbles, voice like grinding stone. "
            "'You carry the scent of my kind. Perhaps you are worth speaking to... or perhaps you are merely prey.'\n\n"
            "This is a battle that will be sung of for generations—if you survive to tell it."
        )
        
        return enemies, environment, context
    
    @staticmethod
    def orc_warband() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Orc raiding party - Medium difficulty
        
        Solutions:
        - Head-on combat
        - Ambush from forest
        - Challenge warchief to duel
        - Cause infighting
        """
        enemies = [
            Enemy(
                name="Grok the Warchief",
                health=45,
                max_health=45,
                attack_power=12,
                defense=4,
                intelligence=7,
                morale=90
            ),
            Enemy(
                name="Orc Berserker",
                health=30,
                max_health=30,
                attack_power=10,
                defense=2,
                intelligence=4,
                morale=70
            ),
            Enemy(
                name="Orc Berserker",
                health=30,
                max_health=30,
                attack_power=10,
                defense=2,
                intelligence=4,
                morale=70
            ),
            Enemy(
                name="Orc Shaman",
                health=20,
                max_health=20,
                attack_power=8,
                defense=1,
                intelligence=10,
                morale=60
            )
        ]
        
        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Dense Forest",
                description="Thick trees provide excellent cover and ambush opportunities.",
                provides_cover=True
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Orc Campfire",
                description="Large campfire. Could cause chaos if knocked into their supplies.",
                is_destructible=True,
                damage_potential=15,
                uses_remaining=1
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Unstable Cliff Edge",
                description="The camp is near a cliff. Enemies could be forced over the edge.",
                damage_potential=40,
                uses_remaining=2
            )
        ]
        
        context = (
            "⚔️ **ORC WARBAND**\n\n"
            "You've tracked the orc raiders to their camp. Grok the Warchief stands at the center, "
            "barking orders in the harsh orc tongue. His warriors sharpen their axes, preparing for another raid.\n\n"
            "They haven't spotted you yet. You could attack now, or... perhaps there are other options. "
            "Orcs respect strength. A challenge to single combat might work. Or you could turn their own "
            "brutality against them.\n\n"
            "Choose your approach carefully."
        )
        
        return enemies, environment, context
    
    @staticmethod
    def undead_legion() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Undead horde - Medium difficulty
        
        Solutions:
        - Holy magic/blessed weapons
        - Destroy necromancer
        - Use sacred ground
        - Burn the bodies
        """
        enemies = [
            Enemy(
                name="Dark Necromancer",
                health=25,
                max_health=25,
                attack_power=9,
                defense=2,
                intelligence=14,
                morale=100  # Undead don't fear
            ),
            Enemy(
                name="Skeletal Warrior",
                health=15,
                max_health=15,
                attack_power=6,
                defense=3,
                intelligence=2,
                morale=100
            ),
            Enemy(
                name="Skeletal Warrior",
                health=15,
                max_health=15,
                attack_power=6,
                defense=3,
                intelligence=2,
                morale=100
            ),
            Enemy(
                name="Skeletal Warrior",
                health=15,
                max_health=15,
                attack_power=6,
                defense=3,
                intelligence=2,
                morale=100
            ),
            Enemy(
                name="Zombie Brute",
                health=35,
                max_health=35,
                attack_power=8,
                defense=1,
                intelligence=1,
                morale=100
            )
        ]
        
        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Sacred Altar",
                description=(
                    "An ancient altar to the gods of light. Its holy power could destroy undead, "
                    "but requires activation."
                ),
                damage_potential=50,
                uses_remaining=1
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Oil Lanterns",
                description="Numerous oil lanterns. Fire is particularly effective against undead.",
                is_destructible=True,
                damage_potential=20,
                uses_remaining=3
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Ancient Crypts",
                description="Stone crypts provide cover, but be careful not to awaken what sleeps within.",
                provides_cover=True
            )
        ]
        
        context = (
            "💀 **UNDEAD LEGION**\n\n"
            "The stench of death fills the air. A necromancer stands among ancient graves, "
            "his dark magic animating the fallen. Skeletal warriors rise from their tombs, "
            "and a massive zombie brute shambles forward.\n\n"
            "'You dare disturb my work?' the necromancer hisses. 'Very well. Join my collection.'\n\n"
            "The undead feel no fear, no mercy. But they have weaknesses. Holy magic, fire, "
            "destroying their master... Choose your strategy wisely."
        )
        
        return enemies, environment, context
    
    @staticmethod
    def royal_assassins() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Political assassination attempt - High difficulty
        
        Solutions:
        - Quick combat before they strike
        - Negotiate/bribe
        - Turn them against their employer
        - Use shadows for counter-ambush
        """
        enemies = [
            Enemy(
                name="Master Assassin",
                health=30,
                max_health=30,
                attack_power=15,
                defense=2,
                intelligence=13,
                morale=80
            ),
            Enemy(
                name="Shadow Blade",
                health=20,
                max_health=20,
                attack_power=12,
                defense=1,
                intelligence=9,
                morale=70
            ),
            Enemy(
                name="Shadow Blade",
                health=20,
                max_health=20,
                attack_power=12,
                defense=1,
                intelligence=9,
                morale=70
            )
        ]
        
        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Darkened Corridors",
                description="Shadows everywhere. Good for stealth, but assassins use them too.",
                provides_cover=True
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Chandelier",
                description="Heavy chandelier above. Could be dropped on enemies.",
                is_destructible=True,
                damage_potential=25,
                uses_remaining=1
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Poisoned Wine",
                description="Wine laced with poison. Could be used against the assassins themselves.",
                damage_potential=30,
                uses_remaining=1
            )
        ]
        
        context = (
            "🗡️ **ROYAL ASSASSINS**\n\n"
            "They strike in the night. Three figures emerge from shadows, blades gleaming. "
            "The master assassin speaks softly: 'Nothing personal. Just business. Someone wants you dead.'\n\n"
            "These are professionals—trained killers from the Shadow Guild. But professionals can be reasoned with. "
            "They work for coin, not loyalty. Perhaps their employer paid enough... or perhaps you can pay more.\n\n"
            "Or you could simply kill them first. The choice is yours, but choose quickly. "
            "They won't wait long."
        )
        
        return enemies, environment, context
    
    @staticmethod
    def troll_bridge() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Classic troll encounter - Easy/Medium difficulty
        
        Solutions:
        - Combat (troll regenerates)
        - Pay toll
        - Solve riddle
        - Burn the troll (fire stops regeneration)
        """
        enemies = [
            Enemy(
                name="Bridge Troll",
                health=60,
                max_health=60,
                attack_power=14,
                defense=5,
                intelligence=6,
                morale=85
            )
        ]
        
        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Old Wooden Bridge",
                description="The bridge itself is old and could collapse under the troll's weight.",
                is_destructible=True,
                damage_potential=30,
                uses_remaining=1
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Torch Fire",
                description="Burning torches. Trolls are vulnerable to fire—it stops their regeneration.",
                damage_potential=25,
                uses_remaining=3
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.COVER,
                name="Large Boulders",
                description="Massive rocks near the bridge provide cover from troll attacks.",
                provides_cover=True
            )
        ]
        
        context = (
            "🌉 **THE TROLL'S BRIDGE**\n\n"
            "'WHO DARES CROSS GRUG'S BRIDGE?' bellows the massive troll, blocking your path. "
            "He stands twice your height, green skin covered in scars, massive club in hand.\n\n"
            "'You pay toll! Gold or... Grug likes riddles too. Or...' he grins, showing yellow teeth, "
            "'...Grug bash you and take gold anyway!'\n\n"
            "Classic troll problem. They regenerate quickly, making straight combat difficult. "
            "But trolls hate fire. And they're not very bright. There are always options..."
        )
        
        return enemies, environment, context
    
    @staticmethod
    def frost_giant_raid() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
        """
        Frost Giant attacking a village - High difficulty
        
        Solutions:
        - Heroic combat
        - Lure into trap
        - Negotiate for village's safety
        - Use fire magic
        """
        enemies = [
            Enemy(
                name="Frost Giant Jarl",
                health=100,
                max_health=100,
                attack_power=20,
                defense=7,
                intelligence=9,
                morale=100
            ),
            Enemy(
                name="Frost Giant Warrior",
                health=60,
                max_health=60,
                attack_power=15,
                defense=5,
                intelligence=6,
                morale=85
            )
        ]
        
        environment = [
            EnvironmentalFeature(
                feature_type=TerrainType.HAZARDOUS,
                name="Burning Buildings",
                description=(
                    "The village burns. Giants are vulnerable to fire, but using it is risky."
                ),
                damage_potential=30,
                uses_remaining=2
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.DESTRUCTIBLE,
                name="Village Watchtower",
                description="Tall watchtower. Could collapse on the giants.",
                is_destructible=True,
                damage_potential=35,
                uses_remaining=1
            ),
            EnvironmentalFeature(
                feature_type=TerrainType.ELEVATED,
                name="Rooftops",
                description="Village rooftops provide elevation advantage against the giants.",
                elevation_bonus=2
            )
        ]
        
        context = (
            "❄️ **FROST GIANT RAID**\n\n"
            "The village is under attack! Two frost giants—massive, blue-skinned, wielding enormous axes—"
            "tear through buildings. Villagers flee in terror. The Jarl laughs, his voice like avalanches:\n\n"
            "'We take what we want! The weak serve the strong!'\n\n"
            "You are vastly outmatched in size and strength. But giants are slow, and they fear fire. "
            "The village is burning around you—that fire could be a weapon. Or you could try to reason "
            "with them, offer tribute, buy time...\n\n"
            "Whatever you do, do it fast. Lives are at stake."
        )
        
        return enemies, environment, context

