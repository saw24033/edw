# Documentation & Instructions

This folder contains setup documentation and the Custom GPT instructions file.

## 📄 Files in This Folder

### Instructions File
- **`custom_gpt_instructions_COMPACT.txt`** (7,112 characters)
  - Main instructions for Custom GPT
  - Goes in the **Instructions** field (NOT Knowledge)
  - Contains core behavior, workflow rules, and references to knowledge files
  - Updated with corridor detection and branch query logic

### Reference Documentation
- **`GPT_USAGE_GUIDE.md`**
  - Usage guide and examples
  - Not needed in Custom GPT Knowledge
  - Reference for understanding system behavior

---

## 🔧 How to Use

1. **Instructions:** Copy contents of `custom_gpt_instructions_COMPACT.txt` and paste into Custom GPT's Instructions field
2. **Knowledge:** Upload all 12 files from `../UPLOAD_TO_CUSTOM_GPT/` folder
3. **Test:** Verify with Morganstown Branch and R081 corridor queries

---

## 📊 Key Updates (Latest Session)

### ✅ Version 3.5.0 - Fixed Issues
1. **Morganstown Branch hallucination** - Now uses scr_lines.json for authoritative data
2. **R081 corridor detection** - Identifies Morganstown corridor (not Benton) via related route analysis

### 📝 Instruction Changes
- Added corridor detection logic for express routes
- Added mandatory scr_lines.json loading for branch queries
- Offloaded detailed examples to SYSTEM_INSTRUCTIONS_REFERENCE.md
- Character count: 7,112 (under 8,000 limit ✅)

---

## 🎯 Version History

| Version | Date | Feature |
|---------|------|---------|
| **3.5.0** | **2025-11-19** | **Branch/line data + corridor detection** ⭐⭐⭐ |
| 3.4.1 | 2025-11-19 | Integration fixes for Custom GPT ⭐ |
| 3.4.0 | 2025-11-18 | Terminal detection for intermediate stops ⭐⭐ |
| 3.3.0 | 2025-11-18 | Improved platform parsing |
| 3.1.0 | 2025-11-18 | Python import paths & coordinates ⭐ |

- **Platform Detection:** v3.4.1 (with terminal detection and fuzzy matching)
- **Corridor Detection:** Enhanced with express route identification
- **Branch Data:** Added scr_lines.json from SCR wiki (15 lines/branches)
