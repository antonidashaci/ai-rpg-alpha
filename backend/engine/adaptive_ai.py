"""
AI-RPG-Alpha: Advanced Memory & Learning AI

Sophisticated AI system with persistent NPC memory, adaptive storytelling,
player preference learning, and emergent relationship dynamics.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
from datetime import datetime, timedelta
import json


class MemoryType(Enum):
    """Types of AI memories"""
    INTERACTION = "interaction"
    OBSERVATION = "observation"
    EMOTIONAL = "emotional"
    FACTUAL = "factual"
    BEHAVIORAL = "behavioral"
    RELATIONSHIP = "relationship"


class LearningCategory(Enum):
    """Categories of player behavior learning"""
    MORAL_CHOICES = "moral_choices"
    COMBAT_STYLE = "combat_style"
    DIALOGUE_PREFERENCES = "dialogue_preferences"
    QUEST_APPROACH = "quest_approach"
    RELATIONSHIP_STYLE = "relationship_style"
    EXPLORATION_PATTERNS = "exploration_patterns"


@dataclass
class AIMemory:
    """Individual AI memory entry"""
    id: str
    memory_type: MemoryType
    content: str
    importance: int  # 1-10
    emotional_weight: float = 0.0  # -1.0 to 1.0
    
    # Context
    location: str = ""
    participants: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Memory properties
    clarity: float = 1.0  # How clear/accurate the memory is
    accessibility: float = 1.0  # How easily recalled
    last_accessed: datetime = field(default_factory=datetime.now)
    
    # Connections to other memories
    related_memories: List[str] = field(default_factory=list)
    contradicts_memories: List[str] = field(default_factory=list)


@dataclass
class PlayerProfile:
    """AI's understanding of player behavior and preferences"""
    player_id: str
    
    # Behavioral patterns
    moral_alignment: Dict[str, float] = field(default_factory=dict)  # good/evil/lawful/chaotic
    personality_traits: Dict[str, float] = field(default_factory=dict)
    decision_patterns: Dict[str, int] = field(default_factory=dict)
    
    # Preferences
    preferred_dialogue_style: str = "balanced"  # direct, diplomatic, humorous, etc.
    preferred_quest_types: List[str] = field(default_factory=list)
    relationship_approach: str = "friendly"  # friendly, professional, romantic, etc.
    
    # Playstyle analysis
    combat_preferences: Dict[str, float] = field(default_factory=dict)
    exploration_style: str = "thorough"  # thorough, efficient, chaotic
    risk_tolerance: float = 0.5  # 0.0 to 1.0
    
    # Learning history
    learning_confidence: Dict[LearningCategory, float] = field(default_factory=dict)
    behavior_samples: Dict[str, List[Dict]] = field(default_factory=dict)
    
    # Adaptation tracking
    successful_predictions: int = 0
    total_predictions: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class NPCMemoryBank:
    """Memory bank for individual NPCs"""
    npc_id: str
    npc_name: str
    
    # Memory storage
    memories: Dict[str, AIMemory] = field(default_factory=dict)
    memory_capacity: int = 1000
    
    # Memory organization
    important_memories: List[str] = field(default_factory=list)
    recent_memories: List[str] = field(default_factory=list)
    emotional_memories: List[str] = field(default_factory=list)
    
    # Player-specific memories
    player_memories: Dict[str, List[str]] = field(default_factory=dict)
    
    # Memory processing
    last_consolidation: datetime = field(default_factory=datetime.now)
    forgotten_memories: int = 0


@dataclass
class StorytellingPreferences:
    """AI's learned preferences about storytelling for this player"""
    preferred_narrative_pace: str = "moderate"  # slow, moderate, fast
    preferred_complexity: str = "medium"  # simple, medium, complex
    preferred_themes: List[str] = field(default_factory=list)
    
    # Content preferences
    violence_tolerance: float = 0.5
    romance_interest: float = 0.5
    political_intrigue_interest: float = 0.5
    mystery_interest: float = 0.5
    
    # Narrative structure preferences
    prefers_linear_stories: bool = False
    enjoys_plot_twists: bool = True
    likes_character_development: bool = True
    
    # Dialogue preferences
    humor_appreciation: float = 0.5
    prefers_brief_conversations: bool = False
    enjoys_philosophical_discussions: bool = False


class AdaptiveAIEngine:
    """Advanced AI system with memory and learning capabilities"""
    
    def __init__(self):
        self.npc_memories: Dict[str, NPCMemoryBank] = {}
        self.player_profiles: Dict[str, PlayerProfile] = {}
        self.global_knowledge: Dict[str, Any] = {}
        self.storytelling_ai = StorytellingAI()
        
        # Learning systems
        self.behavior_analyzer = PlayerBehaviorAnalyzer()
        self.preference_learner = PreferenceLearner()
        self.memory_manager = MemoryManager()
    
    def initialize_npc_memory(self, npc_id: str, npc_name: str, base_knowledge: List[str] = None):
        """Initialize memory bank for an NPC"""
        
        memory_bank = NPCMemoryBank(npc_id=npc_id, npc_name=npc_name)
        
        # Add base knowledge as factual memories
        if base_knowledge:
            for i, knowledge in enumerate(base_knowledge):
                memory_id = f"{npc_id}_base_{i}"
                memory = AIMemory(
                    id=memory_id,
                    memory_type=MemoryType.FACTUAL,
                    content=knowledge,
                    importance=5,
                    clarity=1.0,
                    accessibility=1.0
                )
                memory_bank.memories[memory_id] = memory
                memory_bank.important_memories.append(memory_id)
        
        self.npc_memories[npc_id] = memory_bank
    
    def record_interaction(
        self,
        npc_id: str,
        player_id: str,
        interaction_type: str,
        content: str,
        context: Dict[str, Any] = None
    ):
        """Record an interaction in NPC memory"""
        
        if npc_id not in self.npc_memories:
            self.initialize_npc_memory(npc_id, context.get("npc_name", "Unknown"))
        
        memory_bank = self.npc_memories[npc_id]
        
        # Create interaction memory
        memory_id = f"{npc_id}_interaction_{datetime.now().timestamp()}"
        
        # Determine importance based on interaction type
        importance_map = {
            "first_meeting": 8,
            "deep_conversation": 7,
            "gift_received": 6,
            "helped_in_combat": 9,
            "betrayed": 10,
            "romantic_moment": 8,
            "casual_chat": 3,
            "quest_given": 6,
            "quest_completed": 7
        }
        
        importance = importance_map.get(interaction_type, 5)
        
        # Determine emotional weight
        emotional_weight = self._calculate_emotional_weight(interaction_type, content, context)
        
        memory = AIMemory(
            id=memory_id,
            memory_type=MemoryType.INTERACTION,
            content=f"{interaction_type}: {content}",
            importance=importance,
            emotional_weight=emotional_weight,
            location=context.get("location", "unknown"),
            participants=[player_id]
        )
        
        # Store memory
        memory_bank.memories[memory_id] = memory
        memory_bank.recent_memories.append(memory_id)
        
        # Add to player-specific memories
        if player_id not in memory_bank.player_memories:
            memory_bank.player_memories[player_id] = []
        memory_bank.player_memories[player_id].append(memory_id)
        
        # Update emotional memories if significant
        if abs(emotional_weight) > 0.5:
            memory_bank.emotional_memories.append(memory_id)
        
        # Update important memories if high importance
        if importance >= 7:
            memory_bank.important_memories.append(memory_id)
        
        # Consolidate memories if needed
        if len(memory_bank.memories) > memory_bank.memory_capacity:
            self._consolidate_memories(memory_bank)
        
        # Learn from this interaction
        self._learn_from_interaction(player_id, interaction_type, content, context)
    
    def _calculate_emotional_weight(self, interaction_type: str, content: str, context: Dict[str, Any]) -> float:
        """Calculate emotional weight of an interaction"""
        
        base_emotions = {
            "helped_in_combat": 0.8,
            "betrayed": -0.9,
            "gift_received": 0.6,
            "insulted": -0.7,
            "romantic_moment": 0.9,
            "deep_conversation": 0.5,
            "first_meeting": 0.3,
            "quest_completed": 0.4,
            "quest_failed": -0.3
        }
        
        base_weight = base_emotions.get(interaction_type, 0.0)
        
        # Modify based on content sentiment
        positive_words = ["help", "love", "friend", "trust", "honor", "kind", "good"]
        negative_words = ["hate", "enemy", "betray", "evil", "cruel", "bad", "hurt"]
        
        content_lower = content.lower()
        for word in positive_words:
            if word in content_lower:
                base_weight += 0.1
        
        for word in negative_words:
            if word in content_lower:
                base_weight -= 0.1
        
        return max(-1.0, min(1.0, base_weight))
    
    def _consolidate_memories(self, memory_bank: NPCMemoryBank):
        """Consolidate old memories to make room for new ones"""
        
        # Sort memories by importance and recency
        memory_scores = []
        current_time = datetime.now()
        
        for memory_id, memory in memory_bank.memories.items():
            # Calculate retention score
            importance_score = memory.importance / 10.0
            recency_score = 1.0 / max(1, (current_time - memory.timestamp).days + 1)
            access_score = 1.0 / max(1, (current_time - memory.last_accessed).days + 1)
            emotional_score = abs(memory.emotional_weight)
            
            total_score = importance_score + recency_score + access_score + emotional_score
            memory_scores.append((memory_id, total_score))
        
        # Sort by score (lowest first - these will be forgotten)
        memory_scores.sort(key=lambda x: x[1])
        
        # Remove 20% of lowest-scoring memories
        memories_to_remove = int(len(memory_scores) * 0.2)
        
        for i in range(memories_to_remove):
            memory_id, _ = memory_scores[i]
            
            # Don't remove highly important memories
            if memory_bank.memories[memory_id].importance >= 8:
                continue
            
            # Remove from all lists
            memory_bank.memories.pop(memory_id, None)
            
            if memory_id in memory_bank.recent_memories:
                memory_bank.recent_memories.remove(memory_id)
            if memory_id in memory_bank.important_memories:
                memory_bank.important_memories.remove(memory_id)
            if memory_id in memory_bank.emotional_memories:
                memory_bank.emotional_memories.remove(memory_id)
            
            # Remove from player memories
            for player_memories in memory_bank.player_memories.values():
                if memory_id in player_memories:
                    player_memories.remove(memory_id)
            
            memory_bank.forgotten_memories += 1
        
        memory_bank.last_consolidation = current_time
    
    def get_npc_memory_context(self, npc_id: str, player_id: str, context_type: str = "general") -> Dict[str, Any]:
        """Get relevant memory context for NPC interaction"""
        
        if npc_id not in self.npc_memories:
            return {"memories": [], "relationship_summary": "Unknown person"}
        
        memory_bank = self.npc_memories[npc_id]
        
        # Get player-specific memories
        player_memories = memory_bank.player_memories.get(player_id, [])
        
        relevant_memories = []
        relationship_data = {
            "interaction_count": len(player_memories),
            "positive_interactions": 0,
            "negative_interactions": 0,
            "significant_moments": [],
            "last_interaction": None
        }
        
        # Analyze player memories
        for memory_id in player_memories[-10:]:  # Last 10 interactions
            if memory_id in memory_bank.memories:
                memory = memory_bank.memories[memory_id]
                
                # Update access time
                memory.last_accessed = datetime.now()
                
                relevant_memories.append({
                    "content": memory.content,
                    "importance": memory.importance,
                    "emotional_weight": memory.emotional_weight,
                    "timestamp": memory.timestamp.isoformat(),
                    "location": memory.location
                })
                
                # Update relationship data
                if memory.emotional_weight > 0.3:
                    relationship_data["positive_interactions"] += 1
                elif memory.emotional_weight < -0.3:
                    relationship_data["negative_interactions"] += 1
                
                if memory.importance >= 7:
                    relationship_data["significant_moments"].append(memory.content)
                
                if not relationship_data["last_interaction"] or memory.timestamp > datetime.fromisoformat(relationship_data["last_interaction"]):
                    relationship_data["last_interaction"] = memory.timestamp.isoformat()
        
        # Generate relationship summary
        if relationship_data["interaction_count"] == 0:
            relationship_summary = "I don't recall meeting this person before."
        elif relationship_data["positive_interactions"] > relationship_data["negative_interactions"] * 2:
            relationship_summary = "I have positive feelings about this person."
        elif relationship_data["negative_interactions"] > relationship_data["positive_interactions"] * 2:
            relationship_summary = "I have concerns about this person."
        else:
            relationship_summary = "I have mixed feelings about this person."
        
        return {
            "memories": relevant_memories,
            "relationship_summary": relationship_summary,
            "relationship_data": relationship_data,
            "context_type": context_type
        }
    
    def _learn_from_interaction(self, player_id: str, interaction_type: str, content: str, context: Dict[str, Any]):
        """Learn about player behavior from interaction"""
        
        if player_id not in self.player_profiles:
            self.player_profiles[player_id] = PlayerProfile(player_id=player_id)
        
        profile = self.player_profiles[player_id]
        
        # Analyze moral choices
        if interaction_type in ["moral_choice", "dialogue_choice", "quest_decision"]:
            self.behavior_analyzer.analyze_moral_choice(profile, content, context)
        
        # Analyze dialogue preferences
        if interaction_type in ["dialogue_choice", "conversation"]:
            self.behavior_analyzer.analyze_dialogue_preference(profile, content, context)
        
        # Analyze relationship approach
        if interaction_type in ["romantic_moment", "friendship_building", "gift_giving"]:
            self.behavior_analyzer.analyze_relationship_approach(profile, interaction_type, content)
        
        # Update last updated timestamp
        profile.last_updated = datetime.now()
    
    def generate_adaptive_dialogue(
        self,
        npc_id: str,
        player_id: str,
        dialogue_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate dialogue adapted to player preferences and NPC memory"""
        
        # Get NPC memory context
        memory_context = self.get_npc_memory_context(npc_id, player_id)
        
        # Get player profile
        player_profile = self.player_profiles.get(player_id, PlayerProfile(player_id=player_id))
        
        # Generate adaptive response
        return self.storytelling_ai.generate_adaptive_dialogue(
            npc_id, player_profile, memory_context, dialogue_context
        )
    
    def predict_player_choice(
        self,
        player_id: str,
        choice_context: Dict[str, Any],
        available_choices: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Predict which choice the player is likely to make"""
        
        if player_id not in self.player_profiles:
            return {"prediction": None, "confidence": 0.0}
        
        profile = self.player_profiles[player_id]
        
        # Analyze each choice
        choice_scores = []
        
        for choice in available_choices:
            score = self.behavior_analyzer.score_choice_likelihood(
                profile, choice, choice_context
            )
            choice_scores.append((choice, score))
        
        # Sort by score
        choice_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Update prediction tracking
        profile.total_predictions += 1
        
        if choice_scores:
            best_choice, best_score = choice_scores[0]
            confidence = best_score / sum(score for _, score in choice_scores) if len(choice_scores) > 1 else 1.0
            
            return {
                "prediction": best_choice,
                "confidence": confidence,
                "all_scores": [(choice["id"], score) for choice, score in choice_scores]
            }
        
        return {"prediction": None, "confidence": 0.0}
    
    def adapt_story_content(
        self,
        player_id: str,
        story_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Adapt story content based on learned player preferences"""
        
        if player_id not in self.player_profiles:
            return story_context  # No adaptation possible
        
        profile = self.player_profiles[player_id]
        
        # Get storytelling preferences
        storytelling_prefs = self.preference_learner.get_storytelling_preferences(profile)
        
        # Adapt content
        adapted_content = self.storytelling_ai.adapt_story_content(
            story_context, storytelling_prefs, profile
        )
        
        return adapted_content
    
    def get_ai_status(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive AI system status"""
        
        npc_memory_summary = {}
        for npc_id, memory_bank in self.npc_memories.items():
            player_memory_count = len(memory_bank.player_memories.get(player_id, []))
            npc_memory_summary[npc_id] = {
                "npc_name": memory_bank.npc_name,
                "total_memories": len(memory_bank.memories),
                "player_memories": player_memory_count,
                "forgotten_memories": memory_bank.forgotten_memories,
                "last_interaction": memory_bank.player_memories.get(player_id, [])[-1:] if player_memory_count > 0 else None
            }
        
        player_profile_summary = None
        if player_id in self.player_profiles:
            profile = self.player_profiles[player_id]
            player_profile_summary = {
                "moral_alignment": profile.moral_alignment,
                "personality_traits": profile.personality_traits,
                "preferred_dialogue_style": profile.preferred_dialogue_style,
                "relationship_approach": profile.relationship_approach,
                "successful_predictions": profile.successful_predictions,
                "total_predictions": profile.total_predictions,
                "prediction_accuracy": profile.successful_predictions / max(1, profile.total_predictions)
            }
        
        return {
            "npc_memories": npc_memory_summary,
            "player_profile": player_profile_summary,
            "learning_active": len(self.player_profiles) > 0,
            "total_npcs_with_memory": len(self.npc_memories)
        }


class PlayerBehaviorAnalyzer:
    """Analyzes player behavior patterns"""
    
    def analyze_moral_choice(self, profile: PlayerProfile, content: str, context: Dict[str, Any]):
        """Analyze a moral choice made by the player"""
        
        # Extract moral dimensions from choice
        moral_keywords = {
            "good": ["help", "save", "protect", "heal", "kind", "mercy"],
            "evil": ["harm", "kill", "destroy", "cruel", "selfish"],
            "lawful": ["law", "order", "duty", "rules", "honor"],
            "chaotic": ["freedom", "rebel", "break", "chaos", "independent"]
        }
        
        content_lower = content.lower()
        
        for alignment, keywords in moral_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    current_value = profile.moral_alignment.get(alignment, 0.0)
                    profile.moral_alignment[alignment] = current_value + 0.1
        
        # Normalize values
        total = sum(abs(v) for v in profile.moral_alignment.values())
        if total > 0:
            for key in profile.moral_alignment:
                profile.moral_alignment[key] /= total
    
    def analyze_dialogue_preference(self, profile: PlayerProfile, content: str, context: Dict[str, Any]):
        """Analyze dialogue style preferences"""
        
        dialogue_styles = {
            "direct": ["yes", "no", "straight", "simple"],
            "diplomatic": ["perhaps", "consider", "understand", "respect"],
            "humorous": ["joke", "funny", "laugh", "wit"],
            "aggressive": ["fight", "force", "demand", "threat"]
        }
        
        content_lower = content.lower()
        
        for style, keywords in dialogue_styles.items():
            for keyword in keywords:
                if keyword in content_lower:
                    if "dialogue_style_frequency" not in profile.decision_patterns:
                        profile.decision_patterns["dialogue_style_frequency"] = {}
                    
                    current_count = profile.decision_patterns["dialogue_style_frequency"].get(style, 0)
                    profile.decision_patterns["dialogue_style_frequency"][style] = current_count + 1
                    
                    # Update preferred style
                    most_used_style = max(
                        profile.decision_patterns["dialogue_style_frequency"].items(),
                        key=lambda x: x[1]
                    )[0]
                    profile.preferred_dialogue_style = most_used_style
                    break
    
    def analyze_relationship_approach(self, profile: PlayerProfile, interaction_type: str, content: str):
        """Analyze relationship building approach"""
        
        relationship_indicators = {
            "romantic": ["love", "romance", "date", "kiss"],
            "friendly": ["friend", "buddy", "companion", "ally"],
            "professional": ["business", "work", "duty", "task"],
            "distant": ["alone", "private", "independent", "solo"]
        }
        
        content_lower = content.lower()
        
        for approach, keywords in relationship_indicators.items():
            for keyword in keywords:
                if keyword in content_lower:
                    profile.relationship_approach = approach
                    return
    
    def score_choice_likelihood(
        self,
        profile: PlayerProfile,
        choice: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """Score how likely the player is to make this choice"""
        
        base_score = 1.0
        
        # Check moral alignment compatibility
        choice_content = choice.get("text", "").lower()
        
        for alignment, weight in profile.moral_alignment.items():
            alignment_keywords = {
                "good": ["help", "save", "protect", "kind"],
                "evil": ["harm", "destroy", "selfish"],
                "lawful": ["law", "duty", "order"],
                "chaotic": ["freedom", "rebel", "break"]
            }
            
            if alignment in alignment_keywords:
                for keyword in alignment_keywords[alignment]:
                    if keyword in choice_content:
                        base_score += weight * 2.0
        
        # Check dialogue style compatibility
        if profile.preferred_dialogue_style == "direct" and len(choice_content) < 50:
            base_score += 1.0
        elif profile.preferred_dialogue_style == "diplomatic" and "consider" in choice_content:
            base_score += 1.0
        elif profile.preferred_dialogue_style == "humorous" and any(word in choice_content for word in ["joke", "funny", "wit"]):
            base_score += 1.0
        
        return max(0.1, base_score)


class PreferenceLearner:
    """Learns and adapts to player preferences"""
    
    def get_storytelling_preferences(self, profile: PlayerProfile) -> StorytellingPreferences:
        """Get storytelling preferences based on player profile"""
        
        prefs = StorytellingPreferences()
        
        # Determine narrative pace based on exploration style
        if hasattr(profile, 'exploration_style'):
            if profile.exploration_style == "thorough":
                prefs.preferred_narrative_pace = "slow"
            elif profile.exploration_style == "efficient":
                prefs.preferred_narrative_pace = "fast"
        
        # Determine complexity based on dialogue preferences
        if profile.preferred_dialogue_style == "diplomatic":
            prefs.preferred_complexity = "complex"
        elif profile.preferred_dialogue_style == "direct":
            prefs.preferred_complexity = "simple"
        
        # Set content preferences based on moral alignment
        if profile.moral_alignment.get("good", 0) > 0.5:
            prefs.violence_tolerance = 0.3
        if "romantic" in profile.relationship_approach:
            prefs.romance_interest = 0.8
        
        return prefs


class StorytellingAI:
    """AI system for adaptive storytelling"""
    
    def generate_adaptive_dialogue(
        self,
        npc_id: str,
        player_profile: PlayerProfile,
        memory_context: Dict[str, Any],
        dialogue_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate dialogue adapted to player and NPC context"""
        
        # Base dialogue options
        base_options = dialogue_context.get("options", [])
        
        # Adapt based on player preferences
        adapted_options = []
        
        for option in base_options:
            adapted_option = option.copy()
            
            # Adjust tone based on preferred dialogue style
            if player_profile.preferred_dialogue_style == "direct":
                adapted_option["text"] = self._make_more_direct(option["text"])
            elif player_profile.preferred_dialogue_style == "diplomatic":
                adapted_option["text"] = self._make_more_diplomatic(option["text"])
            elif player_profile.preferred_dialogue_style == "humorous":
                adapted_option["text"] = self._add_humor(option["text"])
            
            adapted_options.append(adapted_option)
        
        # Generate NPC response based on memory
        npc_response = self._generate_memory_aware_response(
            memory_context, dialogue_context, player_profile
        )
        
        return {
            "npc_response": npc_response,
            "adapted_options": adapted_options,
            "adaptation_applied": True
        }
    
    def _make_more_direct(self, text: str) -> str:
        """Make dialogue more direct"""
        # Remove hedging words
        hedging_words = ["perhaps", "maybe", "possibly", "I think"]
        for word in hedging_words:
            text = text.replace(word, "")
        
        # Make statements more definitive
        text = text.replace("Could you", "You should")
        text = text.replace("Would you mind", "Please")
        
        return text.strip()
    
    def _make_more_diplomatic(self, text: str) -> str:
        """Make dialogue more diplomatic"""
        # Add diplomatic phrases
        if text.startswith("No"):
            text = "I respectfully disagree, but " + text[2:].lower()
        elif text.startswith("Yes"):
            text = "I believe you're right that " + text[3:].lower()
        
        return text
    
    def _add_humor(self, text: str) -> str:
        """Add light humor to dialogue"""
        humor_additions = [
            " (with a wry smile)",
            " - though don't tell anyone I said that!",
            " ...well, most of the time anyway.",
            " - at least that's the plan!"
        ]
        
        if random.random() < 0.3:  # 30% chance
            return text + random.choice(humor_additions)
        
        return text
    
    def _generate_memory_aware_response(
        self,
        memory_context: Dict[str, Any],
        dialogue_context: Dict[str, Any],
        player_profile: PlayerProfile
    ) -> str:
        """Generate NPC response that incorporates memory"""
        
        memories = memory_context.get("memories", [])
        relationship_summary = memory_context.get("relationship_summary", "")
        
        # Reference recent significant interactions
        significant_memories = [m for m in memories if m["importance"] >= 7]
        
        if significant_memories:
            recent_memory = significant_memories[-1]
            return f"I remember {recent_memory['content']}. {relationship_summary}"
        
        elif memories:
            return f"Good to see you again. {relationship_summary}"
        
        else:
            return "I don't believe we've met before. What brings you here?"
    
    def adapt_story_content(
        self,
        story_context: Dict[str, Any],
        preferences: StorytellingPreferences,
        player_profile: PlayerProfile
    ) -> Dict[str, Any]:
        """Adapt story content based on preferences"""
        
        adapted_context = story_context.copy()
        
        # Adjust pacing
        if preferences.preferred_narrative_pace == "fast":
            adapted_context["skip_minor_details"] = True
            adapted_context["accelerate_plot"] = True
        elif preferences.preferred_narrative_pace == "slow":
            adapted_context["add_atmospheric_details"] = True
            adapted_context["expand_character_moments"] = True
        
        # Adjust complexity
        if preferences.preferred_complexity == "simple":
            adapted_context["simplify_plot"] = True
            adapted_context["reduce_subplots"] = True
        elif preferences.preferred_complexity == "complex":
            adapted_context["add_subplots"] = True
            adapted_context["increase_moral_ambiguity"] = True
        
        # Content filtering
        if preferences.violence_tolerance < 0.3:
            adapted_context["reduce_violence"] = True
        if preferences.romance_interest > 0.7:
            adapted_context["add_romance_opportunities"] = True
        
        return adapted_context


class MemoryManager:
    """Manages AI memory consolidation and optimization"""
    
    def __init__(self):
        self.consolidation_rules = self._initialize_consolidation_rules()
    
    def _initialize_consolidation_rules(self) -> Dict[str, Any]:
        """Initialize memory consolidation rules"""
        
        return {
            "importance_threshold": 5,
            "recency_days": 30,
            "emotional_threshold": 0.5,
            "access_frequency_threshold": 3,
            "relationship_memory_priority": True
        } 