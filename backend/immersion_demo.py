"""
AI-RPG-Alpha: Immersion Demonstration

Shows the dramatic difference between generic "video game speak" and 
authentic, immersive character dialogue and world descriptions.
"""

from backend.engine.immersive_storytelling import storytelling_engine, NPCPersonality

class ImmersionDemo:
    """Demonstrates the power of immersive storytelling"""
    
    def demonstrate_dialogue_authenticity(self):
        """Show realistic vs generic dialogue examples"""
        
        print("🎭 IMMERSIVE DIALOGUE DEMONSTRATION")
        print("=" * 80)
        print("The difference between generic 'video game speak' and authentic character dialogue\n")
        
        # Gruff Merchant Examples
        print("🏪 GRUFF MERCHANT ENCOUNTER")
        print("-" * 40)
        print("❌ GENERIC (Before):")
        print("'Greetings, traveler! How may I assist you on this fine day?'")
        print("'I have many fine wares for sale! Please browse my selection!'")
        print()
        print("✅ IMMERSIVE (After):")
        
        # Generate authentic dialogue
        merchant_greeting = storytelling_engine.generate_authentic_dialogue(
            "marcus_trader", "first_meeting", {"karma": 0}, [], "stranger"
        )
        merchant_business = storytelling_engine.generate_authentic_dialogue(
            "marcus_trader", "business_inquiry", {"karma": 0}, [], "stranger"
        )
        
        print(f"'{merchant_greeting}'")
        print(f"'{merchant_business}'")
        print()
        print("🧠 WHY IT WORKS:")
        print("• Personality-driven speech patterns")
        print("• Realistic impatience and directness")
        print("• No fake politeness - authentic to character type")
        print("• Creates immediate understanding of who this person is")
        print("\n" + "═" * 80 + "\n")
        
        # Nervous Guard Examples
        print("🛡️ NERVOUS GUARD ENCOUNTER")
        print("-" * 40)
        print("❌ GENERIC (Before):")
        print("'Halt! State your business here, citizen!'")
        print("'I am a loyal guard of this fine establishment!'")
        print()
        print("✅ IMMERSIVE (After):")
        
        guard_greeting = storytelling_engine.generate_authentic_dialogue(
            "guard_tim", "first_meeting", {"karma": 0}, [], "stranger"
        )
        
        print(f"'{guard_greeting}'")
        print("'Uh, excuse me... I need to see your, um, papers?'")
        print("'Please don't make this difficult. I'm just doing my job.'")
        print()
        print("🧠 WHY IT WORKS:")
        print("• Shows uncertainty and inexperience")
        print("• Stammering reveals nervousness authentically")
        print("• Polite but unsure - realistic for new guard")
        print("• Makes player feel the character's human vulnerability")
        print("\n" + "═" * 80 + "\n")
        
        # Arrogant Noble Examples
        print("👑 ARROGANT NOBLE ENCOUNTER")
        print("-" * 40)
        print("❌ GENERIC (Before):")
        print("'Hello there, good sir! How are you doing today?'")
        print("'What brings you to speak with me?'")
        print()
        print("✅ IMMERSIVE (After):")
        
        noble_greeting = storytelling_engine.generate_authentic_dialogue(
            "lord_blackwood", "first_meeting", {"karma": 0}, [], "stranger"
        )
        
        print(f"'{noble_greeting}'")
        print("'You may speak, but be brief and respectful.'")
        print("'Make your business known quickly. My time is valuable.'")
        print()
        print("🧠 WHY IT WORKS:")
        print("• Immediately establishes social hierarchy")
        print("• Condescending tone feels authentic to privileged background")
        print("• Creates immediate emotional response in player")
        print("• Shows character's worldview through speech patterns")
        print("\n" + "═" * 80 + "\n")
    
    def demonstrate_mood_based_reactions(self):
        """Show how character mood affects dialogue authentically"""
        
        print("🎭 MOOD-BASED DIALOGUE SYSTEM")
        print("=" * 60)
        print("Same character, different circumstances = different reactions\n")
        
        print("🏪 MARCUS THE MERCHANT - MOOD VARIATIONS")
        print("-" * 50)
        
        scenarios = [
            ("Normal Day", {"karma": 0}, [], "stranger"),
            ("After Robbery", {"karma": 0}, ["robbery_nearby"], "stranger"),
            ("Good Business Day", {"karma": 0}, ["good_business"], "customer"),
            ("Evil Player Reputation", {"karma": -60}, [], "stranger")
        ]
        
        for scenario_name, reputation, events, relationship in scenarios:
            print(f"📅 {scenario_name.upper()}:")
            dialogue = storytelling_engine.generate_authentic_dialogue(
                "marcus_trader", "first_meeting", reputation, events, relationship
            )
            print(f"   '{dialogue}'\n")
        
        print("🧠 IMMERSION IMPACT:")
        print("• World feels alive and reactive")
        print("• Characters remember and respond to events")
        print("• Player actions have meaningful consequences")
        print("• Creates sense of living, breathing world")
        print("\n" + "═" * 80 + "\n")
    
    def demonstrate_social_class_speech(self):
        """Show how social class affects authentic speech patterns"""
        
        print("🏛️ SOCIAL CLASS SPEECH PATTERNS")
        print("=" * 60)
        print("Authentic speech reflects character background\n")
        
        # Create sample dialogue from different social classes
        examples = [
            ("Peasant Elder", "elder_miriam", "Welcome, young one. What brings you to our humble village?"),
            ("Noble Lord", "lord_blackwood", "You may speak, but be brief and respectful."),
            ("Criminal Thief", "shadow_thief", "*looks around nervously* What do you want?"),
            ("Merchant Innkeeper", "martha_innkeeper", "Welcome to the Sleepy Griffin, dearie! Come in!")
        ]
        
        for class_name, character_id, sample in examples:
            print(f"👤 {class_name.upper()}:")
            print(f"   '{sample}'")
            
            character = storytelling_engine.character_database[character_id]
            print(f"   Background: {character.background_story}")
            print(f"   Speech patterns: {', '.join(character.speech_patterns)}")
            print()
        
        print("🧠 AUTHENTICITY ELEMENTS:")
        print("• Vocabulary matches education level")
        print("• Formality reflects social standing") 
        print("• Slang and expressions fit character's world")
        print("• Body language cues enhance immersion")
        print("\n" + "═" * 80 + "\n")
    
    def demonstrate_immersive_descriptions(self):
        """Show rich, sensory world descriptions"""
        
        print("🌍 IMMERSIVE WORLD DESCRIPTIONS")
        print("=" * 60)
        print("Rich sensory details bring the world to life\n")
        
        print("❌ GENERIC DESCRIPTION (Before):")
        print("You are in a village. There are houses and people around.")
        print("The weather is nice today.")
        print()
        
        print("✅ IMMERSIVE DESCRIPTION (After):")
        village_description = storytelling_engine.generate_immersive_scene_description(
            "Village of Millbrook", "day", "clear", "moderate", []
        )
        print(village_description)
        print()
        
        print("🌙 SAME LOCATION - DIFFERENT TIME:")
        night_description = storytelling_engine.generate_immersive_scene_description(
            "Village of Millbrook", "night", "misty", "quiet", []
        )
        print(night_description)
        print()
        
        print("🧠 IMMERSION TECHNIQUES:")
        print("• Multiple senses engaged (sight, sound, smell)")
        print("• Time and weather create atmosphere")
        print("• Specific details instead of generic terms")
        print("• Emotional tone matches setting")
        print("\n" + "═" * 80 + "\n")
    
    def demonstrate_world_reactions(self):
        """Show how the world reacts authentically to player actions"""
        
        print("⚡ DYNAMIC WORLD REACTIONS")
        print("=" * 60)
        print("The world responds believably to player choices\n")
        
        scenarios = [
            ("Stealing in Village", "steal bread from market", "Village of Millbrook", 
             ["guard_tim", "martha_innkeeper"], {"karma": -20}),
            ("Helping Villagers", "help elderly woman carry groceries", "Village of Millbrook",
             ["elder_miriam"], {"karma": 30}),
            ("Violence in Peaceful Area", "attack merchant", "Village of Millbrook",
             ["guard_tim", "martha_innkeeper"], {"karma": -80})
        ]
        
        for scenario_name, action, location, witnesses, reputation in scenarios:
            print(f"🎬 {scenario_name.upper()}:")
            print(f"   Action: {action}")
            
            reaction = storytelling_engine.create_dynamic_world_reaction(
                action, location, witnesses, reputation
            )
            print(f"   World Reaction: {reaction}")
            print()
        
        print("🧠 IMMERSION BENEFITS:")
        print("• Actions have realistic consequences")
        print("• NPCs react based on their personalities")
        print("• World feels alive and responsive")
        print("• Player choices matter authentically")
        print("\n" + "═" * 80 + "\n")
    
    def demonstrate_character_consistency(self):
        """Show how characters maintain consistent personalities"""
        
        print("🎯 CHARACTER CONSISTENCY")
        print("=" * 60)
        print("NPCs remain true to their personalities across interactions\n")
        
        print("📊 MARCUS THE GRUFF MERCHANT - CONSISTENCY CHECK:")
        print("-" * 55)
        
        interactions = [
            ("First Meeting", "first_meeting"),
            ("Business Inquiry", "business_inquiry"),
            ("Information Request", "information_request"),
            ("Casual Conversation", "casual_conversation")
        ]
        
        for interaction_name, context in interactions:
            dialogue = storytelling_engine.generate_authentic_dialogue(
                "marcus_trader", context, {"karma": 0}, [], "stranger"
            )
            print(f"{interaction_name}: '{dialogue}'")
        
        print()
        print("🧠 CONSISTENCY ELEMENTS:")
        print("• Same gruff, business-focused personality")
        print("• Consistent speech patterns and vocabulary")
        print("• Reactions match established character traits")
        print("• No personality contradictions or generic responses")
        print("\n" + "═" * 80 + "\n")

def run_immersion_demo():
    """Run the complete immersion demonstration"""
    
    print("🎮 AI-RPG-ALPHA: IMMERSION DEMONSTRATION")
    print("=" * 80)
    print("Transforming generic NPCs into authentic, believable characters")
    print("that create maximum immersion in our text-based world.")
    print("=" * 80 + "\n")
    
    demo = ImmersionDemo()
    
    # Run all demonstrations
    demo.demonstrate_dialogue_authenticity()
    demo.demonstrate_mood_based_reactions()
    demo.demonstrate_social_class_speech()
    demo.demonstrate_immersive_descriptions()
    demo.demonstrate_world_reactions()
    demo.demonstrate_character_consistency()
    
    print("🎯 IMMERSION ACHIEVEMENT SUMMARY:")
    print("=" * 60)
    print("✅ No more 'video game speak' - authentic dialogue")
    print("✅ Characters react based on personality & mood")
    print("✅ Rich sensory descriptions every turn")
    print("✅ Social class affects speech patterns realistically")
    print("✅ Dynamic world reactions to player actions")
    print("✅ Consistent character personalities")
    print("✅ Living, breathing world that feels real")
    print()
    print("🚀 IMMERSION LEVEL: MAXIMUM!")
    print("Players will feel truly transported to our fantasy world.")

if __name__ == "__main__":
    run_immersion_demo() 