"""
Extended Quest Collection - Part 2
Additional 30+ quests to complete our comprehensive quest system
"""

from backend.engine.quest_collection import QuestCollection, EnhancedQuest, QuestCategory, QuestChain, QuestRequirements
from backend.engine.alignment_karma import KarmaAction
from backend.models.dataclasses import Quest, QuestStatus, RiskLevel, Reward, ConsequenceThread
from typing import Dict, Any, List


class ExtendedQuestCollection(QuestCollection):
    """Extended quest collection with 50+ total quests"""
    
    def _initialize_quest_collection(self):
        """Initialize all quests including extended collection"""
        super()._initialize_quest_collection()
        
        # Add extended quest categories
        self._create_additional_faction_quests()
        self._create_merchant_trade_quests()
        self._create_exploration_quests()
        self._create_romantic_quests()
        self._create_epic_quest_chains()
        self._create_seasonal_event_quests()
        self._create_redemption_quests()
    
    def _create_additional_faction_quests(self):
        """Create additional faction quests"""
        
        # Order of Dawn Quests
        self.quests["dawn_temple_purification"] = EnhancedQuest(
            quest=Quest(
                id="dawn_temple_purification",
                title="Cleansing the Corrupted Temple",
                location="temple_of_dawn",
                tags=["faction", "order_of_dawn", "holy", "purification"],
                intro="The Temple of Dawn has been desecrated by Shadow Covenant cultists. The holy priests need a champion to cleanse the corruption and restore the sacred ground.",
                objectives=[
                    "Enter the corrupted temple",
                    "Banish the shadow entities",
                    "Restore the holy altar"
                ],
                success="The temple is purified and becomes a beacon of hope against the darkness.",
                failure="Though not fully cleansed, you've weakened the corruption significantly.",
                reward=Reward(gold=400, items=["Blessed Weapon", "Dawn Priest Robes"], experience=150),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.FACTION_POLITICAL,
            requirements=QuestRequirements(
                required_factions={"order_of_dawn": 30},
                required_alignment=["good"],
                max_corruption=20
            ),
            karma_actions={
                "purify_altar": KarmaAction.HEAL_WOUNDED,
                "show_mercy_to_cultists": KarmaAction.SHOW_MERCY,
                "destroy_corrupted_artifacts": KarmaAction.UPHOLD_LAW
            },
            faction_impacts={"order_of_dawn": 40, "shadow_covenant": -30}
        )
        
        # Merchant Guild Quests
        self.quests["trade_route_protection"] = EnhancedQuest(
            quest=Quest(
                id="trade_route_protection",
                title="Guardian of Commerce",
                location="trade_roads",
                tags=["faction", "merchant_guilds", "protection", "economic"],
                intro="Bandit attacks threaten the vital trade routes between cities. The Merchant Guilds offer lucrative contracts for skilled protection.",
                objectives=[
                    "Patrol the main trade routes",
                    "Eliminate bandit threats",
                    "Escort high-value caravans"
                ],
                success="Trade flourishes under your protection, strengthening the regional economy.",
                failure="Some caravans are lost, but your efforts reduce overall bandit activity.",
                reward=Reward(gold=350, items=["Merchant's Signet", "Trade Route Map"], experience=120),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.FACTION_POLITICAL,
            requirements=QuestRequirements(
                required_factions={"merchant_guilds": 25}
            ),
            karma_actions={
                "protect_merchants": KarmaAction.PROTECT_WEAK,
                "eliminate_bandits": KarmaAction.UPHOLD_LAW,
                "demand_extra_payment": KarmaAction.EXTORT
            },
            faction_impacts={"merchant_guilds": 35, "criminal_underworld": -25}
        )
        
        # House Ravencrest Intrigue
        self.quests["ravencrest_succession"] = EnhancedQuest(
            quest=Quest(
                id="ravencrest_succession",
                title="The Ravencrest Inheritance",
                location="ravencrest_manor",
                tags=["faction", "house_ravencrest", "intrigue", "succession"],
                intro="Lord Ravencrest has died mysteriously, and his three children compete for inheritance. Each offers you rewards to support their claim to power.",
                objectives=[
                    "Investigate Lord Ravencrest's death",
                    "Choose which heir to support",
                    "Secure their claim to leadership"
                ],
                success="Your chosen heir takes control of House Ravencrest and remembers your loyalty.",
                failure="The succession crisis continues, but you've gained insight into noble politics.",
                reward=Reward(gold=600, items=["Noble House Favor"], experience=180),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.FACTION_POLITICAL,
            requirements=QuestRequirements(
                required_factions={"house_ravencrest": 20},
                min_level=8
            ),
            karma_actions={
                "support_rightful_heir": KarmaAction.UPHOLD_LAW,
                "support_corrupt_heir": KarmaAction.SELFISH_CHOICE,
                "forge_inheritance_documents": KarmaAction.BREAK_PROMISE,
                "assassinate_rival_heir": KarmaAction.MURDER_INNOCENT
            },
            faction_impacts={"house_ravencrest": 50},
            unlocks_quests=["noble_conspiracy_revealed"]
        )
    
    def _create_merchant_trade_quests(self):
        """Create merchant and trade-focused quests"""
        
        self.quests["exotic_goods_expedition"] = EnhancedQuest(
            quest=Quest(
                id="exotic_goods_expedition",
                title="Journey to the Spice Islands",
                location="distant_islands",
                tags=["merchant", "exploration", "trade", "exotic"],
                intro="A wealthy merchant seeks an adventurer to lead an expedition to the legendary Spice Islands, where rare goods can make fortunes.",
                objectives=[
                    "Organize and supply the expedition",
                    "Navigate dangerous waters to reach the islands",
                    "Negotiate trade deals with island natives"
                ],
                success="You return with exotic goods worth a fortune and establish new trade relationships.",
                failure="The expedition faces setbacks, but you've opened new possibilities for future trade.",
                reward=Reward(gold=800, items=["Exotic Spices", "Navigator's Compass"], experience=200),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.MERCHANT_TRADE,
            requirements=QuestRequirements(
                min_level=6,
                required_factions={"merchant_guilds": 15}
            ),
            karma_actions={
                "fair_trade_with_natives": KarmaAction.KEEP_PROMISE,
                "exploit_native_ignorance": KarmaAction.EXTORT,
                "share_profits_with_crew": KarmaAction.HELP_POOR
            },
            faction_impacts={"merchant_guilds": 30},
            world_impact={"trade_prosperity": 2, "cultural_exchange": 1}
        )
        
        self.quests["smuggling_operation"] = EnhancedQuest(
            quest=Quest(
                id="smuggling_operation", 
                title="Contraband and Consequences",
                location="port_district",
                tags=["merchant", "criminal", "smuggling", "risk"],
                intro="A desperate merchant offers you a fortune to smuggle illegal goods past the royal customs. The risk is enormous, but so is the reward.",
                objectives=[
                    "Acquire the contraband goods",
                    "Evade customs inspections",
                    "Deliver goods to the black market buyer"
                ],
                success="The smuggling operation succeeds, netting you substantial profits and criminal contacts.",
                failure="You're caught by authorities, but manage to avoid serious consequences.",
                reward=Reward(gold=1200, items=["Smuggler's Cache Map"], experience=150),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.MERCHANT_TRADE,
            requirements=QuestRequirements(
                min_corruption=20,
                required_factions={"criminal_underworld": 15}
            ),
            karma_actions={
                "smuggle_illegal_goods": KarmaAction.BREAK_LAW,
                "bribe_customs_officers": KarmaAction.EXTORT,
                "betray_merchant_to_authorities": KarmaAction.BETRAY_ALLY
            },
            faction_impacts={"criminal_underworld": 25, "lawful_authorities": -20}
        )
    
    def _create_exploration_quests(self):
        """Create exploration and discovery quests"""
        
        self.quests["lost_city_discovery"] = EnhancedQuest(
            quest=Quest(
                id="lost_city_discovery",
                title="The Lost City of Aetherion",
                location="uncharted_wilderness",
                tags=["exploration", "discovery", "ancient", "legendary"],
                intro="Ancient maps speak of Aetherion, a lost city of incredible wealth and magical knowledge. Many have searched; none have returned.",
                objectives=[
                    "Decipher the ancient maps",
                    "Navigate the treacherous wilderness",
                    "Discover the secrets of Aetherion"
                ],
                success="You discover the lost city and uncover its incredible treasures and knowledge.",
                failure="The city remains lost, but your exploration reveals valuable clues for future expeditions.",
                reward=Reward(gold=2000, items=["Ancient Artifact", "City Map"], experience=300),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.EXPLORATION,
            requirements=QuestRequirements(
                min_level=12,
                required_story_flags=["master_explorer"]
            ),
            karma_actions={
                "preserve_ancient_knowledge": KarmaAction.KEEP_PROMISE,
                "loot_everything": KarmaAction.SELFISH_CHOICE,
                "share_discovery_with_scholars": KarmaAction.HELP_POOR
            },
            world_impact={"archaeological_knowledge": 3, "ancient_magic_understanding": 2}
        )
        
        self.quests["monster_hunter_trial"] = EnhancedQuest(
            quest=Quest(
                id="monster_hunter_trial",
                title="Trial of the Monster Hunter",
                location="monster_territories",
                tags=["exploration", "combat", "monsters", "trial"],
                intro="The Monster Hunter's Guild tests potential members by hunting three legendary beasts. Only the bravest and most skilled survive this trial.",
                objectives=[
                    "Hunt the Shadowmane Wolf",
                    "Defeat the Crystal Basilisk",
                    "Slay the Terror Bird of the peaks"
                ],
                success="You become a certified Monster Hunter with access to exclusive contracts and equipment.",
                failure="Though you don't complete all trials, your attempts earn respect among hunters.",
                reward=Reward(gold=500, items=["Monster Hunter License", "Beast Tracker Tools"], experience=250),
                risk=RiskLevel.COMBAT
            ),
            category=QuestCategory.EXPLORATION,
            requirements=QuestRequirements(
                min_level=8,
                max_corruption=40
            ),
            karma_actions={
                "hunt_responsibly": KarmaAction.PROTECT_WEAK,
                "torture_beasts": KarmaAction.TORTURE,
                "protect_monster_habitats": KarmaAction.PRAGMATIC_DECISION
            },
            unlocks_quests=["legendary_beast_hunt", "monster_conservation"]
        )
    
    def _create_romantic_quests(self):
        """Create romance and relationship quests"""
        
        self.quests["lyralei_romance"] = EnhancedQuest(
            quest=Quest(
                id="lyralei_romance",
                title="Heart of the Forest",
                location="moonlit_grove",
                tags=["romance", "lyralei", "companion", "personal"],
                intro="Your relationship with Lyralei has deepened beyond friendship. She invites you to a sacred grove under the full moon to share something important.",
                objectives=[
                    "Meet Lyralei at the moonlit grove",
                    "Share your feelings honestly",
                    "Make a commitment to your relationship"
                ],
                success="You and Lyralei become romantic partners, deepening your bond beyond mere companionship.",
                failure="Your relationship remains strong as friends, with mutual respect and understanding.",
                reward=Reward(gold=0, items=["Heart Bond Token"], experience=75),
                risk=RiskLevel.CALM
            ),
            category=QuestCategory.COMPANION_PERSONAL,
            requirements=QuestRequirements(
                required_companions=["lyralei_ranger"],
                required_quests_completed=["lyralei_past"],
                min_level=10
            ),
            karma_actions={
                "express_love_honestly": KarmaAction.KEEP_PROMISE,
                "manipulate_emotions": KarmaAction.BREAK_PROMISE
            },
            companion_impacts={"lyralei_ranger": 50}
        )
        
        self.quests["tragic_love_triangle"] = EnhancedQuest(
            quest=Quest(
                id="tragic_love_triangle",
                title="Two Hearts, One Choice",
                location="various",
                tags=["romance", "tragedy", "choice", "emotional"],
                intro="You find yourself caught between two people who both love you deeply. Your choice will break one heart while fulfilling another.",
                objectives=[
                    "Acknowledge the situation honestly",
                    "Consider both relationships carefully",
                    "Make a choice that you can live with"
                ],
                success="You handle the situation with honesty and compassion, though not everyone's heart remains unbroken.",
                failure="The situation becomes complicated and painful for everyone involved.",
                reward=Reward(gold=0, items=["Wisdom of the Heart"], experience=100),
                risk=RiskLevel.CALM
            ),
            category=QuestCategory.COMPANION_PERSONAL,
            requirements=QuestRequirements(
                min_level=8,
                required_companions=["lyralei_ranger", "thane_warrior"]  # Or other combinations
            ),
            karma_actions={
                "choose_honestly": KarmaAction.KEEP_PROMISE,
                "deceive_both": KarmaAction.BREAK_PROMISE,
                "sacrifice_own_happiness": KarmaAction.SELF_SACRIFICE
            }
        )
    
    def _create_epic_quest_chains(self):
        """Create epic multi-part quest chains"""
        
        # The Corruption War Chain
        self.quests["corruption_war_begins"] = EnhancedQuest(
            quest=Quest(
                id="corruption_war_begins",
                title="The First Sign",
                location="various",
                tags=["epic", "corruption", "war", "main_story"],
                intro="Reality itself begins to fray as corruption spreads through the realm. This is more than political strife - this is a war for the very soul of the world.",
                objectives=[
                    "Investigate reality distortions",
                    "Rally allies for the coming conflict",
                    "Prepare for war against corruption itself"
                ],
                success="You've identified the true threat and begun building a coalition to fight it.",
                failure="The corruption spreads further, but awareness of the threat grows.",
                reward=Reward(gold=300, items=["Reality Anchor"], experience=150),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.MAIN_STORY,
            chain=QuestChain.CORRUPTION_PATH,
            requirements=QuestRequirements(
                min_level=12,
                required_quests_completed=["shadow_conspiracy_begins"]
            ),
            unlocks_quests=["gather_corruption_resistance", "find_pure_artifacts"],
            world_impact={"corruption_awareness": 2, "reality_stability": -1}
        )
        
        # The Unity Path Chain
        self.quests["unite_the_factions"] = EnhancedQuest(
            quest=Quest(
                id="unite_the_factions",
                title="Forging Unlikely Alliances",
                location="neutral_territory",
                tags=["epic", "diplomacy", "unity", "faction"],
                intro="With corruption threatening everything, ancient enemies must become allies. Can you unite the fractured factions against a common threat?",
                objectives=[
                    "Arrange a peace summit",
                    "Mediate between hostile factions",
                    "Create a unified resistance"
                ],
                success="The factions put aside their differences to face the greater threat.",
                failure="Some alliances form, but unity remains elusive.",
                reward=Reward(gold=500, items=["Peacemaker's Staff"], experience=200),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.FACTION_POLITICAL,
            chain=QuestChain.WORLD_CRISIS,
            requirements=QuestRequirements(
                min_level=15,
                required_alignment=["good", "neutral"],
                required_factions={"royal_crown": 20, "peoples_liberation": 20}
            ),
            karma_actions={
                "broker_honest_peace": KarmaAction.KEEP_PROMISE,
                "unite_against_common_enemy": KarmaAction.PROTECT_WEAK,
                "manipulate_factions": KarmaAction.BREAK_PROMISE
            },
            unlocks_quests=["final_battle_preparation"]
        )
    
    def _create_seasonal_event_quests(self):
        """Create seasonal and time-limited event quests"""
        
        self.quests["harvest_festival_crisis"] = EnhancedQuest(
            quest=Quest(
                id="harvest_festival_crisis",
                title="The Poisoned Harvest",
                location="farming_district",
                tags=["seasonal", "festival", "crisis", "community"],
                intro="The annual Harvest Festival is threatened when the crops are discovered to be poisoned. Without intervention, the celebration will become a tragedy.",
                objectives=[
                    "Investigate the source of the poison",
                    "Find an antidote or cleansing method",
                    "Save the Harvest Festival"
                ],
                success="The festival is saved and becomes a celebration of your heroism.",
                failure="The festival is cancelled, but your efforts prevent a larger catastrophe.",
                reward=Reward(gold=200, items=["Festival Crown"], experience=100),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.WORLD_EVENT,
            karma_actions={
                "save_the_harvest": KarmaAction.PROTECT_WEAK,
                "expose_the_poisoner": KarmaAction.UPHOLD_LAW,
                "profit_from_crisis": KarmaAction.SELFISH_CHOICE
            },
            world_impact={"community_happiness": 2, "food_security": 1}
        )
        
        self.quests["winter_solstice_darkness"] = EnhancedQuest(
            quest=Quest(
                id="winter_solstice_darkness",
                title="When the Sun Won't Rise",
                location="solar_temple",
                tags=["seasonal", "supernatural", "darkness", "ritual"],
                intro="The winter solstice has passed, but the sun hasn't returned. Eternal darkness threatens to grip the land unless the ancient solar rituals are restored.",
                objectives=[
                    "Discover why the sun won't rise",
                    "Gather components for the solar ritual",
                    "Perform the ritual to restore daylight"
                ],
                success="Your efforts restore the natural cycle and bring back the sun.",
                failure="Darkness persists, but your ritual weakens whatever force blocks the sun.",
                reward=Reward(gold=400, items=["Solar Blessing"], experience=180),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.WORLD_EVENT,
            karma_actions={
                "restore_natural_order": KarmaAction.HEAL_WOUNDED,
                "embrace_eternal_darkness": KarmaAction.DESECRATE
            },
            world_impact={"natural_balance": 2, "supernatural_activity": -1}
        )
    
    def _create_redemption_quests(self):
        """Create redemption arc quests for evil characters"""
        
        self.quests["path_of_redemption"] = EnhancedQuest(
            quest=Quest(
                id="path_of_redemption",
                title="Seeking Forgiveness",
                location="temple_of_dawn",
                tags=["redemption", "moral", "transformation", "atonement"],
                intro="Your dark past weighs heavily on your soul. The priests of Dawn offer a chance at redemption, but the path to forgiveness is neither easy nor certain.",
                objectives=[
                    "Confess your crimes to the High Priest",
                    "Perform acts of penance and service",
                    "Prove your commitment to change"
                ],
                success="You begin walking the difficult path of redemption, earning a chance to make amends.",
                failure="Redemption remains out of reach, but you've taken the first steps toward change.",
                reward=Reward(gold=0, items=["Pendant of Atonement"], experience=100),
                risk=RiskLevel.CALM
            ),
            category=QuestCategory.ALIGNMENT_MORAL,
            chain=QuestChain.REDEMPTION_ARC,
            requirements=QuestRequirements(
                min_corruption=60,
                max_karma=-100,
                required_alignment=["evil"]
            ),
            karma_actions={
                "confess_crimes": KarmaAction.KEEP_PROMISE,
                "help_those_you_wronged": KarmaAction.HEAL_WOUNDED,
                "sacrifice_for_others": KarmaAction.SELF_SACRIFICE
            },
            unlocks_quests=["atonement_trials", "redemption_test"],
            world_impact={"redemption_possibility": 1}
        )
        
        self.quests["atonement_trials"] = EnhancedQuest(
            quest=Quest(
                id="atonement_trials",
                title="Trials of Atonement",
                location="various",
                tags=["redemption", "trials", "challenge", "growth"],
                intro="To prove your redemption is genuine, you must face three trials that test your commitment to good, your willingness to sacrifice, and your ability to resist temptation.",
                objectives=[
                    "Pass the Trial of Compassion",
                    "Endure the Trial of Sacrifice", 
                    "Overcome the Trial of Temptation"
                ],
                success="You pass the trials and prove your redemption is real, not merely convenient.",
                failure="Though you fail some trials, your effort demonstrates genuine desire to change.",
                reward=Reward(gold=100, items=["Redeemer's Mark"], experience=200),
                risk=RiskLevel.MYSTERY
            ),
            category=QuestCategory.ALIGNMENT_MORAL,
            chain=QuestChain.REDEMPTION_ARC,
            requirements=QuestRequirements(
                required_quests_completed=["path_of_redemption"],
                min_corruption=40
            ),
            karma_actions={
                "show_true_compassion": KarmaAction.PROTECT_WEAK,
                "sacrifice_for_strangers": KarmaAction.SELF_SACRIFICE,
                "resist_evil_temptation": KarmaAction.UPHOLD_LAW
            },
            unlocks_quests=["redeemed_hero_path"]
        )
    
    def get_quest_chains_summary(self) -> Dict[str, Any]:
        """Get detailed summary of all quest chains"""
        
        chains = {}
        for quest_id, quest in self.quests.items():
            if quest.chain:
                chain_name = quest.chain.value
                if chain_name not in chains:
                    chains[chain_name] = []
                chains[chain_name].append({
                    "id": quest_id,
                    "title": quest.quest.title,
                    "category": quest.category.value,
                    "unlocks": quest.unlocks_quests
                })
        
        return chains
    
    def get_interconnection_map(self) -> Dict[str, List[str]]:
        """Get map of quest interconnections"""
        
        interconnections = {}
        for quest_id, quest in self.quests.items():
            if quest.unlocks_quests:
                interconnections[quest_id] = quest.unlocks_quests
        
        return interconnections