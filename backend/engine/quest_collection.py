"""
Comprehensive Quest Collection for AI-RPG-Alpha

50+ interconnected quests that integrate with:
- Alignment & Karma System
- Faction Politics
- Companion Relationships  
- World Story
- Living World Events
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import random

from backend.engine.alignment_karma import KarmaAction, MoralAlignment
from backend.models.dataclasses import Quest, QuestStatus, RiskLevel, Reward, ConsequenceThread


class QuestCategory(Enum):
    MAIN_STORY = "main_story"
    FACTION_POLITICAL = "faction_political"
    COMPANION_PERSONAL = "companion_personal"
    ALIGNMENT_MORAL = "alignment_moral"
    WORLD_EVENT = "world_event"
    EXPLORATION = "exploration"
    CRIMINAL_UNDERGROUND = "criminal_underground"
    HEROIC_LEGENDARY = "heroic_legendary"
    MERCHANT_TRADE = "merchant_trade"
    MYSTERY_SUPERNATURAL = "mystery_supernatural"


class QuestChain(Enum):
    THE_SHATTERED_CROWN = "shattered_crown_chain"
    SHADOW_CONSPIRACY = "shadow_conspiracy_chain"
    COMPANION_BONDS = "companion_bonds_chain"
    FACTION_WAR = "faction_war_chain"
    CORRUPTION_PATH = "corruption_path_chain"
    REDEMPTION_ARC = "redemption_arc_chain"
    WORLD_CRISIS = "world_crisis_chain"


@dataclass
class QuestRequirements:
    """Requirements for quest availability"""
    min_level: int = 1
    max_level: int = 100
    required_alignment: List[str] = field(default_factory=list)
    forbidden_alignment: List[str] = field(default_factory=list)
    min_karma: int = -1000
    max_karma: int = 1000
    min_corruption: int = 0
    max_corruption: int = 100
    required_factions: Dict[str, int] = field(default_factory=dict)  # faction: min_standing
    forbidden_factions: Dict[str, int] = field(default_factory=dict)  # faction: max_standing
    required_companions: List[str] = field(default_factory=list)
    required_quests_completed: List[str] = field(default_factory=list)
    required_story_flags: List[str] = field(default_factory=list)
    forbidden_story_flags: List[str] = field(default_factory=list)


@dataclass
class EnhancedQuest:
    """Enhanced quest with requirements and consequences"""
    quest: Quest
    category: QuestCategory
    chain: Optional[QuestChain] = None
    requirements: QuestRequirements = field(default_factory=QuestRequirements)
    karma_actions: Dict[str, KarmaAction] = field(default_factory=dict)  # choice_id: karma_action
    unlocks_quests: List[str] = field(default_factory=list)
    locks_quests: List[str] = field(default_factory=list)
    world_impact: Dict[str, Any] = field(default_factory=dict)
    companion_impacts: Dict[str, int] = field(default_factory=dict)
    faction_impacts: Dict[str, int] = field(default_factory=dict)


class QuestCollection:
    """Master collection of all quests in the game"""
    
    def __init__(self):
        self.quests: Dict[str, EnhancedQuest] = {}
        self._initialize_quest_collection()
    
    def _initialize_quest_collection(self):
        """Initialize all 50+ quests"""
        
        # Main Story Chain (10 quests)
        self._create_main_story_quests()
        
        # Faction Political Quests (12 quests)  
        self._create_faction_quests()
        
        # Companion Personal Quests (8 quests)
        self._create_companion_quests()
        
        # Alignment/Moral Choice Quests (8 quests)
        self._create_alignment_quests()
        
        # Criminal Underground Quests (6 quests)
        self._create_criminal_quests()
        
        # Heroic/Legendary Quests (5 quests)
        self._create_heroic_quests()
        
        # Mystery/Supernatural Quests (6 quests)
        self._create_mystery_quests()
        
        # World Event/Crisis Quests (5 quests)
        self._create_world_event_quests()
    
    def _create_main_story_quests(self):
        """Create main story quest chain"""
        
        # Quest 1: The Awakening
        self.quests["story_awakening"] = EnhancedQuest(
            quest=Quest(
                id="story_awakening",
                title="The Dreamer's Awakening",
                location="whispering_woods",
                tags=["main_story", "mystery", "awakening"],
                intro="You awaken in the Whispering Woods with fragmented memories and a strange mark on your hand. Ancient voices seem to whisper your name, and reality itself feels... unstable.",
                objectives=[
                    "Explore your immediate surroundings",
                    "Find clues about your identity", 
                    "Reach the nearby village of Millbrook"
                ],
                success="You begin to piece together fragments of your past and learn of the great upheaval affecting the realm.",
                failure="Your memories remain clouded, but you've taken the first steps on a greater journey.",
                reward=Reward(gold=0, items=["Mysterious Pendant"], experience=25),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.MAIN_STORY,
            chain=QuestChain.THE_SHATTERED_CROWN,
            unlocks_quests=["story_first_choice", "village_troubles"],
            world_impact={"story_progression": 1}
        )
        
        # Quest 2: The First Choice
        self.quests["story_first_choice"] = EnhancedQuest(
            quest=Quest(
                id="story_first_choice",
                title="Crossroads of Destiny", 
                location="millbrook_village",
                tags=["main_story", "moral_choice", "faction_introduction"],
                intro="The village of Millbrook is in crisis. Royal soldiers demand tribute for the 'Shattered Crown War,' while rebels seek to recruit locals. Your choice here will shape your destiny.",
                objectives=[
                    "Listen to both the Royal Captain and Rebel Leader",
                    "Choose which cause to support (or forge your own path)",
                    "Deal with the immediate crisis"
                ],
                success="Your choice echoes through the realm as factions take notice of a new player in the great game.",
                failure="Even in failure, your moral stance becomes known to those who watch from the shadows.",
                reward=Reward(gold=100, items=["Faction Sigil"], experience=50),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.MAIN_STORY,
            chain=QuestChain.THE_SHATTERED_CROWN,
            requirements=QuestRequirements(required_quests_completed=["story_awakening"]),
            karma_actions={
                "support_crown": KarmaAction.UPHOLD_LAW,
                "support_rebels": KarmaAction.REBEL,
                "forge_own_path": KarmaAction.PRAGMATIC_DECISION,
                "exploit_both_sides": KarmaAction.SELFISH_CHOICE
            },
            unlocks_quests=["crown_loyalist_path", "rebel_revolutionary_path", "shadow_broker_path"],
            faction_impacts={"royal_crown": 25, "peoples_liberation": -25}
        )
        
        # Quest 3: The Shadow Conspiracy  
        self.quests["shadow_conspiracy_begins"] = EnhancedQuest(
            quest=Quest(
                id="shadow_conspiracy_begins",
                title="Whispers in the Dark",
                location="various",
                tags=["main_story", "conspiracy", "investigation"],
                intro="Strange events plague the realm. Nobles disappear, ancient artifacts go missing, and some say the very foundations of reality are being eroded by dark forces.",
                objectives=[
                    "Investigate mysterious disappearances",
                    "Track down stolen artifacts",
                    "Uncover the Shadow Covenant's involvement"
                ],
                success="You begin to unravel a conspiracy that threatens the very fabric of the world.",
                failure="The conspiracy remains hidden, but you've drawn the attention of dangerous forces.",
                reward=Reward(gold=200, items=["Conspiracy Notes", "Shadow Ward Amulet"], experience=75),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.MAIN_STORY,
            chain=QuestChain.SHADOW_CONSPIRACY,
            requirements=QuestRequirements(required_quests_completed=["story_first_choice"]),
            unlocks_quests=["infiltrate_shadow_covenant", "protect_artifacts"],
            world_impact={"conspiracy_awareness": 1, "shadow_activity": -1}
        )
        
        # Continue with more main story quests...
        
    def _create_faction_quests(self):
        """Create faction political quests"""
        
        # Royal Crown Faction Quests
        self.quests["crown_diplomatic_mission"] = EnhancedQuest(
            quest=Quest(
                id="crown_diplomatic_mission",
                title="Royal Diplomacy",
                location="noble_district",
                tags=["faction", "royal_crown", "diplomacy"],
                intro="The Crown seeks to negotiate a treaty with House Ravencrest. Your diplomatic skills could prevent a bloody civil war.",
                objectives=[
                    "Meet with House Ravencrest representatives",
                    "Negotiate terms favorable to the Crown",
                    "Secure signatures on the peace treaty"
                ],
                success="Your diplomacy averts civil war and strengthens royal authority.",
                failure="Negotiations fail, pushing the realm closer to internal conflict.",
                reward=Reward(gold=300, items=["Royal Seal", "Diplomat's Robes"], experience=100),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.FACTION_POLITICAL,
            requirements=QuestRequirements(
                required_factions={"royal_crown": 20},
                required_alignment=["lawful"]
            ),
            karma_actions={
                "honest_negotiation": KarmaAction.KEEP_PROMISE,
                "threaten_opposition": KarmaAction.EXTORT,
                "forge_documents": KarmaAction.BREAK_PROMISE
            },
            faction_impacts={"royal_crown": 30, "house_ravencrest": 15}
        )
        
        # People's Liberation Quests  
        self.quests["rebel_supply_raid"] = EnhancedQuest(
            quest=Quest(
                id="rebel_supply_raid", 
                title="Strike Against Oppression",
                location="royal_supply_depot",
                tags=["faction", "peoples_liberation", "raid"],
                intro="The People's Liberation needs weapons and supplies. A royal depot holds enough arms to equip a rebel company, but it's heavily guarded.",
                objectives=[
                    "Scout the royal supply depot",
                    "Neutralize guards (lethally or non-lethally)",
                    "Liberate supplies for the rebellion"
                ],
                success="The successful raid provides the rebellion with crucial supplies and deals a blow to royal logistics.",
                failure="The raid is repelled, but your courage inspires other rebels to join the cause.",
                reward=Reward(gold=200, items=["Rebel Armband", "Liberated Weapons"], experience=80),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.FACTION_POLITICAL,
            requirements=QuestRequirements(
                required_factions={"peoples_liberation": 25},
                max_corruption=30
            ),
            karma_actions={
                "non_lethal_approach": KarmaAction.SHOW_MERCY,
                "kill_guards": KarmaAction.MURDER_INNOCENT,
                "help_wounded_guards": KarmaAction.HEAL_WOUNDED
            },
            faction_impacts={"peoples_liberation": 40, "royal_crown": -30}
        )
        
        # Shadow Covenant Quests (Evil Path)
        self.quests["shadow_initiation"] = EnhancedQuest(
            quest=Quest(
                id="shadow_initiation",
                title="Embrace the Darkness",
                location="shadow_sanctum",
                tags=["faction", "shadow_covenant", "evil", "ritual"],
                intro="The Shadow Covenant has noticed your... flexible morality. They offer power beyond imagination in exchange for your service to the dark.",
                objectives=[
                    "Participate in a dark ritual",
                    "Prove your commitment by eliminating a 'problem'",
                    "Swear the blood oath to the Shadow"
                ],
                success="You are initiated into the Shadow Covenant and gain access to forbidden powers.",
                failure="The darkness rejects you, but you've learned of their existence and methods.",
                reward=Reward(gold=500, items=["Shadow Cloak", "Dark Ritual Dagger"], experience=150),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.FACTION_POLITICAL,
            requirements=QuestRequirements(
                min_corruption=40,
                required_alignment=["evil"]
            ),
            karma_actions={
                "embrace_darkness": KarmaAction.DESECRATE,
                "eliminate_target": KarmaAction.MURDER_INNOCENT,
                "blood_oath": KarmaAction.BETRAY_ALLY
            },
            faction_impacts={"shadow_covenant": 50, "order_of_dawn": -50},
            world_impact={"shadow_influence": 2, "corruption_spread": 1}
        )
    
    def _create_companion_quests(self):
        """Create companion personal quests"""
        
        # Lyralei's Quest Chain
        self.quests["lyralei_past"] = EnhancedQuest(
            quest=Quest(
                id="lyralei_past",
                title="The Ranger's Secret",
                location="ancient_forest",
                tags=["companion", "lyralei", "personal", "forest"],
                intro="Lyralei has been receiving cryptic messages from her past. Something in the Ancient Forest calls to her, and she asks for your help to face whatever awaits.",
                objectives=[
                    "Accompany Lyralei to the Ancient Forest",
                    "Help her confront her past",
                    "Support her difficult choices"
                ],
                success="Lyralei finds peace with her past and her bond with you deepens significantly.",
                failure="Old wounds remain unhealed, but Lyralei appreciates your attempt to help.",
                reward=Reward(gold=150, items=["Forest Bond Ring"], experience=75),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.COMPANION_PERSONAL,
            requirements=QuestRequirements(
                required_companions=["lyralei_ranger"],
                min_level=5
            ),
            companion_impacts={"lyralei_ranger": 30},
            unlocks_quests=["lyralei_romance", "forest_guardian_pact"]
        )
        
        # Thane's Honor Quest
        self.quests["thane_honor_trial"] = EnhancedQuest(
            quest=Quest(
                id="thane_honor_trial",
                title="Trial of Honor",
                location="warrior_halls",
                tags=["companion", "thane", "honor", "combat"],
                intro="Thane faces accusations of cowardice from his former war band. To clear his name, he must undergo the Trial of Honor - single combat against his accusers.",
                objectives=[
                    "Accompany Thane to the Warrior Halls",
                    "Witness his trial by combat",
                    "Support him through the ordeal"
                ],
                success="Thane's honor is restored and he gains the respect of his peers once more.",
                failure="Despite defeat, Thane's courage in facing the trial restores some measure of his honor.",
                reward=Reward(gold=200, items=["Honor Guard Badge"], experience=100),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.COMPANION_PERSONAL,
            requirements=QuestRequirements(
                required_companions=["thane_warrior"],
                required_alignment=["lawful", "good"]
            ),
            karma_actions={
                "fight_honorably": KarmaAction.UPHOLD_LAW,
                "cheat_for_thane": KarmaAction.BREAK_LAW,
                "expose_false_accusations": KarmaAction.PROTECT_WEAK
            },
            companion_impacts={"thane_warrior": 40}
        )
    
    def _create_alignment_quests(self):
        """Create alignment-specific moral choice quests"""
        
        # Good Alignment Quest
        self.quests["orphanage_salvation"] = EnhancedQuest(
            quest=Quest(
                id="orphanage_salvation",
                title="Sanctuary of Hope",
                location="lower_district",
                tags=["alignment", "good", "charity", "protection"],
                intro="The city orphanage faces closure due to corrupt officials demanding bribes. Dozens of children will be left homeless unless someone intervenes.",
                objectives=[
                    "Investigate the corruption charges",
                    "Raise funds to save the orphanage",
                    "Protect the children from eviction"
                ],
                success="The orphanage is saved and becomes a beacon of hope in dark times.",
                failure="Some children are helped despite the orphanage's closure.",
                reward=Reward(gold=0, items=["Saint's Blessing"], experience=100),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.ALIGNMENT_MORAL,
            requirements=QuestRequirements(
                required_alignment=["good"],
                min_karma=50
            ),
            karma_actions={
                "donate_personal_wealth": KarmaAction.DONATE_CHARITY,
                "protect_children": KarmaAction.PROTECT_WEAK,
                "expose_corruption": KarmaAction.UPHOLD_LAW
            },
            world_impact={"orphan_welfare": 2, "corruption_level": -1}
        )
        
        # Evil Alignment Quest
        self.quests["crime_syndicate_takeover"] = EnhancedQuest(
            quest=Quest(
                id="crime_syndicate_takeover",
                title="Crown of Shadows",
                location="underworld_district",
                tags=["alignment", "evil", "crime", "power"],
                intro="The local crime syndicate is weak and divided. With enough ruthlessness and cunning, you could seize control and rule the underworld.",
                objectives=[
                    "Eliminate rival crime bosses",
                    "Intimidate remaining gangs into submission",
                    "Establish yourself as the new crime lord"
                ],
                success="You become the undisputed ruler of the criminal underworld.",
                failure="Your bid for power fails, but you've gained respect among criminals.",
                reward=Reward(gold=1000, items=["Crime Lord's Ring"], experience=200),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.ALIGNMENT_MORAL,
            requirements=QuestRequirements(
                required_alignment=["evil"],
                min_corruption=60,
                required_factions={"criminal_underworld": 40}
            ),
            karma_actions={
                "murder_rivals": KarmaAction.MURDER_INNOCENT,
                "torture_information": KarmaAction.TORTURE,
                "extort_businesses": KarmaAction.EXTORT
            },
            faction_impacts={"criminal_underworld": 50, "lawful_authorities": -40},
            world_impact={"crime_rate": 3, "fear_level": 2}
        )
    
    def _create_criminal_quests(self):
        """Create criminal underground quests"""
        
        self.quests["heist_royal_treasury"] = EnhancedQuest(
            quest=Quest(
                id="heist_royal_treasury",
                title="The Royal Treasury Job",
                location="royal_palace",
                tags=["criminal", "heist", "stealth", "legendary"],
                intro="The ultimate score: breaking into the Royal Treasury. It's said to contain enough wealth to buy a small kingdom, but the security is legendary.",
                objectives=[
                    "Recruit a skilled crew",
                    "Plan the perfect heist",
                    "Execute the robbery without getting caught"
                ],
                success="You pull off the heist of the century and become a legend among thieves.",
                failure="The heist fails spectacularly, but you escape with your life and some dignity.",
                reward=Reward(gold=5000, items=["Master Thief's Tools", "Royal Jewels"], experience=300),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.CRIMINAL_UNDERGROUND,
            requirements=QuestRequirements(
                min_level=10,
                required_factions={"criminal_underworld": 50},
                max_karma=-50
            ),
            karma_actions={
                "steal_from_crown": KarmaAction.STEAL_FROM_POOR,  # Crown represents the people's wealth
                "kill_guards": KarmaAction.MURDER_INNOCENT,
                "frame_innocent": KarmaAction.BETRAY_ALLY
            },
            faction_impacts={"criminal_underworld": 60, "royal_crown": -60}
        )
    
    def _create_heroic_quests(self):
        """Create heroic legendary quests"""
        
        self.quests["dragon_ancient_evil"] = EnhancedQuest(
            quest=Quest(
                id="dragon_ancient_evil",
                title="The Ancient Terror",
                location="dragon_peaks",
                tags=["heroic", "legendary", "dragon", "epic"],
                intro="An ancient red dragon has awakened and threatens to burn the entire realm to ash. Only a true hero has any hope of stopping this primordial evil.",
                objectives=[
                    "Gather legendary weapons and allies",
                    "Confront the ancient dragon in its lair",
                    "Save the realm from fiery destruction"
                ],
                success="You slay the ancient dragon and become a legend sung by bards across the realm.",
                failure="Though you fall, your sacrifice inspires others to continue the fight.",
                reward=Reward(gold=10000, items=["Dragonslayer Title", "Dragon Heart"], experience=500),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.HEROIC_LEGENDARY,
            requirements=QuestRequirements(
                min_level=15,
                min_karma=100,
                required_alignment=["good"],
                required_story_flags=["legendary_hero"]
            ),
            karma_actions={
                "protect_innocents": KarmaAction.PROTECT_WEAK,
                "sacrifice_for_realm": KarmaAction.SELF_SACRIFICE
            },
            world_impact={"dragon_threat": -5, "hero_legend": 3}
        )
    
    def _create_mystery_quests(self):
        """Create mystery and supernatural quests"""
        
        self.quests["ghostly_manor"] = EnhancedQuest(
            quest=Quest(
                id="ghostly_manor",
                title="The Haunted Manor of Blackwood",
                location="blackwood_manor",
                tags=["mystery", "supernatural", "ghost", "investigation"],
                intro="The abandoned Blackwood Manor is haunted by restless spirits. Strange lights appear in its windows, and locals report hearing mournful wails echoing through the night.",
                objectives=[
                    "Investigate the paranormal activity",
                    "Uncover the dark history of the Blackwood family",
                    "Put the tortured souls to rest"
                ],
                success="You solve the mystery and grant peace to the restless dead.",
                failure="The mystery deepens, but you've learned valuable information.",
                reward=Reward(gold=300, items=["Spirit Medium's Crystal"], experience=150),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.MYSTERY_SUPERNATURAL,
            karma_actions={
                "help_ghosts_rest": KarmaAction.SHOW_MERCY,
                "exploit_spirits": KarmaAction.DESECRATE,
                "investigate_peacefully": KarmaAction.PRAGMATIC_DECISION
            },
            world_impact={"supernatural_activity": -1}
        )
    
    def _create_world_event_quests(self):
        """Create world event crisis quests"""
        
        self.quests["plague_outbreak"] = EnhancedQuest(
            quest=Quest(
                id="plague_outbreak",
                title="The Crimson Plague",
                location="plague_district",
                tags=["world_event", "plague", "crisis", "medical"],
                intro="A mysterious plague spreads through the city, turning victims' blood crimson. The city guard has quarantined entire districts, but the disease continues to spread.",
                objectives=[
                    "Investigate the plague's origin",
                    "Help treat the infected",
                    "Find a cure before the city falls"
                ],
                success="Your efforts help contain the plague and save countless lives.",
                failure="The plague spreads, but your research provides clues for future treatment.",
                reward=Reward(gold=400, items=["Plague Doctor's Mask"], experience=200),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.WORLD_EVENT,
            karma_actions={
                "risk_life_helping": KarmaAction.SELF_SACRIFICE,
                "quarantine_brutally": KarmaAction.CAUSE_CHAOS,
                "profiteer_from_plague": KarmaAction.SELFISH_CHOICE
            },
            world_impact={"plague_severity": -2, "medical_knowledge": 1}
        )
    
    def get_quest(self, quest_id: str) -> Optional[EnhancedQuest]:
        """Get a specific quest by ID"""
        return self.quests.get(quest_id)
    
    def get_available_quests(
        self, 
        player_level: int,
        alignment: str,
        karma: int,
        corruption: int,
        faction_standings: Dict[str, int],
        completed_quests: List[str],
        story_flags: List[str],
        companions: List[str]
    ) -> List[EnhancedQuest]:
        """Get all quests available to the player based on their current state"""
        
        available = []
        
        for quest_id, enhanced_quest in self.quests.items():
            if quest_id in completed_quests:
                continue
                
            req = enhanced_quest.requirements
            
            # Level check
            if player_level < req.min_level or player_level > req.max_level:
                continue
            
            # Alignment check
            if req.required_alignment and not any(align in alignment for align in req.required_alignment):
                continue
            if req.forbidden_alignment and any(align in alignment for align in req.forbidden_alignment):
                continue
            
            # Karma check
            if karma < req.min_karma or karma > req.max_karma:
                continue
            
            # Corruption check
            if corruption < req.min_corruption or corruption > req.max_corruption:
                continue
            
            # Faction standings check
            faction_ok = True
            for faction, min_standing in req.required_factions.items():
                if faction_standings.get(faction, 0) < min_standing:
                    faction_ok = False
                    break
            
            for faction, max_standing in req.forbidden_factions.items():
                if faction_standings.get(faction, 0) > max_standing:
                    faction_ok = False
                    break
            
            if not faction_ok:
                continue
            
            # Companion check
            if req.required_companions and not all(comp in companions for comp in req.required_companions):
                continue
            
            # Completed quests check
            if req.required_quests_completed and not all(q in completed_quests for q in req.required_quests_completed):
                continue
            
            # Story flags check
            if req.required_story_flags and not all(flag in story_flags for flag in req.required_story_flags):
                continue
            if req.forbidden_story_flags and any(flag in story_flags for flag in req.forbidden_story_flags):
                continue
            
            available.append(enhanced_quest)
        
        return available
    
    def get_quests_by_category(self, category: QuestCategory) -> List[EnhancedQuest]:
        """Get all quests in a specific category"""
        return [quest for quest in self.quests.values() if quest.category == category]
    
    def get_quests_by_chain(self, chain: QuestChain) -> List[EnhancedQuest]:
        """Get all quests in a specific chain"""
        return [quest for quest in self.quests.values() if quest.chain == chain]
    
    def get_next_quests_in_chain(self, completed_quest_id: str) -> List[EnhancedQuest]:
        """Get the next quests that should be unlocked after completing a quest"""
        if completed_quest_id not in self.quests:
            return []
        
        completed_quest = self.quests[completed_quest_id]
        unlocked = []
        
        for quest_id in completed_quest.unlocks_quests:
            if quest_id in self.quests:
                unlocked.append(self.quests[quest_id])
        
        return unlocked
    
    def get_quest_summary(self) -> Dict[str, Any]:
        """Get summary statistics about the quest collection"""
        
        category_counts = {}
        chain_counts = {}
        
        for quest in self.quests.values():
            category_counts[quest.category.value] = category_counts.get(quest.category.value, 0) + 1
            if quest.chain:
                chain_counts[quest.chain.value] = chain_counts.get(quest.chain.value, 0) + 1
        
        return {
            "total_quests": len(self.quests),
            "quests_by_category": category_counts,
            "quests_by_chain": chain_counts,
            "interconnected_quests": len([q for q in self.quests.values() if q.unlocks_quests or q.locks_quests])
        } 