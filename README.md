# 🎮 AI-RPG-Alpha

**Professional AI-Powered RPG Engine with BG3-Style Combat, Long-Form Quests, and Cosmic Horror Mechanics**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🌟 Öne Çıkan Özellikler

### ⚔️ BG3-Style Tactical Combat
- **Environmental Interactions:** Çevreyi kullan, köprüleri yık, yüksek yerlerden avantaj kazan
- **Multiple Solutions:** Her karşılaşma için 5+ farklı çözüm yolu
- **Failure-as-Content:** Yenilgi = yeni hikaye yolları
- **Resource Management:** Stamina ve Action Points sistemi
- **Smart Enemy AI:** Zekaya göre adapte olan düşman yapay zekası

### 📜 Long-Form Quest System
- **30-40 Turn Quests:** Bethesda-kalitesinde uzun-format görevler
- **Multi-Act Structure:** Setup → Pursuit → Climax → Aftermath
- **Meaningful Choices:** Her 3-5 turda anlamlı seçim
- **Dynamic Endings:** Seçimlerinize göre değişen sonlar
- **Quest Milestones:** Önemli anlar ve dönüm noktaları

### 🪄 Complete Magic System
- **6 Magic Schools:** Destruction, Restoration, Alteration, Conjuration, Illusion, Enchantment
- **20+ Spells:** From Fire Bolt to Invisibility
- **Mana Management:** Strategic spell casting with costs and regeneration
- **Spell Schools:** Specialize in different magical disciplines
- **Magical Artifacts:** Enchanted items that enhance spellcasting

### 🏰 NPC Dialogue & Political Intrigue
- **Dynamic NPCs:** 5+ unique characters with branching dialogue trees
- **Kingdom Politics:** 3 kingdoms (Ironhold, Stormwatch, Frostmere) with dynamic relationships
- **Reputation System:** Build alliances and rivalries across kingdoms
- **Political Events:** Diplomatic choices affect entire realms
- **Faction Management:** Noble houses and political intrigue

### 🎭 Immersive Fantasy World
- **Rich Lore:** Deep world-building with ancient prophecies and dragon history
- **Multiple Factions:** Political maneuvering and alliance building
- **Living World:** NPCs react to player reputation and choices
- **Consequence System:** Every decision ripples across the realm

### 🌍 The Northern Realms - Complete Epic Fantasy

**Single-Scenario Excellence:** Focus entirely on one rich, detailed fantasy world:

- **🐉 Dragon Prophecy:** 40-turn epic quest with ancient prophecies
- **🏰 Kingdom Politics:** Three kingdoms (Ironhold, Stormwatch, Frostmere) with dynamic alliances
- **🪄 Complete Magic:** 6 schools, 20+ spells, mana management, magical artifacts
- **⚔️ Tactical Combat:** BG3-style encounters with environmental interactions
- **👥 Living NPCs:** 5+ characters with branching dialogue and reputation systems
- **🏛️ Political Intrigue:** Diplomatic choices affect entire realms
- **📚 Rich Lore:** Deep world-building with history, factions, and consequences

---

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.11+
- pip (Python package manager)

### Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/antonidashaci/ai-rpg-alpha.git
cd ai-rpg-alpha

# Backend bağımlılıklarını yükleyin
cd backend
pip install -r requirements.txt

# Backend'i başlatın
python main_enhanced.py
```

Backend şu adreste çalışacak: **http://localhost:8000**

### Frontend

```bash
# Yeni terminal açın
cd frontend

# HTTP server başlatın (Python ile)
python -m http.server 3000

# VEYA Node.js ile
npx http-server -p 3000
```

Frontend şu adreste: **http://localhost:3000**

### API Dokümantasyonu

FastAPI otomatik dokümantasyon: **http://localhost:8000/docs**

---

## 🎮 Nasıl Oynanır

1. **Scenario Seçin:** Cosmic Horror, Epic Fantasy veya Cyberpunk
2. **Karakterinizi Oluşturun:** İsim ve yetenekler
3. **Maceraya Başlayın:** 40-turn epic journey
4. **Seçimler Yapın:** Her seçimin sonuçları var
5. **Savaşın veya Konuşun:** Combat veya diplomasi
6. **Bilgi Edinin:** (Cosmic Horror) Güç için akıl sağlığınızı riske atın

---

## 📋 API Endpoints

### Game Management
- `POST /game/new` - Yeni oyun başlat (Northern Realms)
- `POST /game/turn` - Oyun turu işle
- `GET /game/state/{player_id}` - Oyun durumunu al
- `POST /game/save` - Oyunu kaydet
- `POST /game/load` - Oyunu yükle

### Combat System
- `POST /game/combat/action` - Combat aksiyonu işle
- 7 Fantasy encounters (dragon, orcs, undead, assassins, troll, frost giants)

### Magic System
- `GET /magic/spells` - Tüm büyüleri listele
- `GET /magic/schools` - Büyü okullarını listele
- `POST /magic/spells` - Büyü kullan
- 6 schools, 20+ spells, mana management

### NPC Dialogue & Politics
- `GET /npcs` - NPC'leri listele
- `POST /npcs/dialogue` - NPC ile konuşma
- `GET /kingdoms` - Krallık durumlarını al
- `POST /politics/ally` - Krallık ile ittifak kur
- 5 NPCs, 3 kingdoms, political intrigue

### Information
- `GET /health` - Sistem sağlık kontrolü
- `GET /politics/events` - Siyasi olayları al

---

## 🏗️ Teknik Mimari

### Backend Stack
```
FastAPI (Modern async web framework)
  ↓
Game Orchestrator (Master controller)
  ├── Quest Framework Engine (30-40 turn quests)
  ├── Tactical Combat Engine (BG3-style combat)
  ├── Sanity Engine (Cosmic horror mechanics)
  └── Game Database (SQLite persistence)
       ↓
AI Narrative Templates (Context-aware prompts)
```

### Modüler Yapı
- **`combat_system.py`** - BG3-inspired tactical combat
- **`quest_framework.py`** - Long-form quest management
- **`sanity_system.py`** - Cosmic horror sanity mechanics
- **`game_orchestrator.py`** - Central game controller
- **`game_database.py`** - Database operations
- **`narrative_templates.py`** - AI prompt templates
- **`main_enhanced.py`** - FastAPI server

---

## 💾 Database Schema

8 ana tablo:
- **players** - Karakter istatistikleri ve kaynaklar
- **quest_states** - Quest ilerlemesi ve seçimler
- **combat_encounters** - Combat geçmişi
- **sanity_events** - Sanity olayları (Cosmic Horror)
- **player_knowledge** - Yasak bilgi takibi
- **game_events** - Turn-by-turn event logging
- **inventory** - Envanter yönetimi
- **save_slots** - Kayıt slotları

---

## 🎨 Frontend Features

- **Quest Progress Tracker** - Act göstergesi ve ilerleme çubuğu
- **Combat Visualization** - Düşman kartları ve kaynak göstergeleri
- **Sanity Meter** - Akıl sağlığı ve corruption seviyesi
- **Enhanced Choice UI** - Modern ve responsive seçim düğmeleri
- **Loading States** - Smooth loading animations
- **Responsive Design** - Mobile ve desktop uyumlu

---

## 🔧 Geliştirme

### Proje Yapısı
```
ai-rpg-alpha/
├── backend/
│   ├── ai/                    # AI integration
│   │   └── narrative_templates.py
│   ├── dao/                   # Database operations
│   │   └── game_database.py
│   ├── engine/                # Game engines
│   │   ├── combat_system.py
│   │   ├── quest_framework.py
│   │   ├── sanity_system.py
│   │   └── game_orchestrator.py
│   ├── models/                # Data models
│   └── main_enhanced.py       # FastAPI server
├── frontend/
│   ├── enhanced_game.js       # Game logic
│   ├── enhanced_styles.css    # Enhanced styles
│   └── index.html             # Main page
└── docs/                      # Documentation
```

### Yeni Scenario Ekleme
```python
# backend/engine/quest_framework.py içinde
@staticmethod
def your_new_scenario_quest() -> LongFormQuest:
    quest = LongFormQuest(
        quest_id="new_scenario",
        title="Your Quest Title",
        scenario="your_scenario",
        total_turns=40,
        milestones=[...],  # Define milestones
        opening_narrative="...",
        possible_endings=[...]
    )
    return quest
```

### Yeni Combat Encounter Ekleme
```python
# backend/engine/combat_system.py içinde
@staticmethod
def your_encounter() -> Tuple[List[Enemy], List[EnvironmentalFeature], str]:
    enemies = [Enemy(...), Enemy(...)]
    environment = [EnvironmentalFeature(...)]
    context = "Your encounter description"
    return enemies, environment, context
```

---

## 📊 Kod İstatistikleri

**Phase 1 Implementation:**
- ~3,932 satır yeni kod
- 7 yeni backend modülü
- 2 enhanced frontend dosyası
- 8 veritabanı tablosu
- 10+ API endpoint

---

## 🎯 Roadmap

### ✅ Phase 1: Core Foundation (TAMAMLANDI)
- BG3-Style Combat System
- Long-Form Quest Framework
- Cosmic Horror Sanity Mechanics
- Enhanced Database & Save System
- AI Narrative Templates
- Enhanced Frontend UI

### 🔄 Phase 2: Scenario Content (DEVAM EDİYOR)
- [ ] Complete The Whispering Town quest content
- [ ] Complete The Northern Realms quest content
- [ ] Complete Neo-Tokyo 2087 quest content
- [ ] Cross-scenario butterfly effects
- [ ] Additional combat encounters

### 📝 Phase 3: Polish & Expansion
- [ ] AI integration (Gemini/OpenAI)
- [ ] Advanced quest editor
- [ ] Community content sharing
- [ ] Achievement system
- [ ] Statistics and analytics

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:
1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🌟 Özellikler Detayı

### Combat System Highlights
- **8 Action Types:** Attack, Defend, Environment, Negotiate, Flee, Stealth, Position, Cast Spell
- **4 Difficulty Levels:** Story, Balanced, Tactical, Honor
- **5 Terrain Types:** Open, Elevated, Cover, Hazardous, Destructible
- **Dynamic AI:** Intelligence-based enemy decisions
- **Morale System:** Enemies can flee when demoralized

### Quest System Highlights
- **4 Quest Acts:** Setup, Pursuit, Climax, Aftermath
- **4 Impact Levels:** Minor, Moderate, Major, Critical
- **Milestone Tracking:** Every 3-5 turns
- **Combat Integration:** Every 8-10 turns
- **Dynamic Endings:** Based on player choices

### Sanity System Highlights
- **5 Sanity Levels:** Each with unique effects
- **5 Forbidden Knowledge Items:** Power vs Sanity trade-off
- **6 Distortion Types:** Visual, Auditory, Temporal, Spatial, Identity, Text
- **Text Corruption:** Zalgo, word replacement, letter glitching
- **Hallucination System:** Context-aware hallucinations

---

## 📞 İletişim

- **Proje:** [github.com/antonidashaci/ai-rpg-alpha](https://github.com/antonidashaci/ai-rpg-alpha)
- **Issues:** [github.com/antonidashaci/ai-rpg-alpha/issues](https://github.com/antonidashaci/ai-rpg-alpha/issues)

---

## 🙏 Teşekkürler

Bu proje şu harika oyunlardan ilham aldı:
- **Baldur's Gate 3** - Tactical combat mechanics
- **Bethesda RPGs** - Long-form quest design
- **Lovecraft** - Cosmic horror elements
- **Disco Elysium** - Narrative depth
- **AI Dungeon** - AI-driven storytelling

---

**Made with ❤️ and 🤖 AI**

**Phase 1: COMPLETE** ✅  
**Ready for Phase 2: Scenario Content Development** 🚀
