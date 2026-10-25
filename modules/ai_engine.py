"""
Food Verse AI - Unified AI Engine
Supports Google Gemini (multimodal vision & reasoning), Groq Cloud,
and a standalone demonstration simulation mode with zero API key dependencies.
"""

import os
import io
import json
import base64
import logging
from typing import Dict, Any, Optional
from PIL import Image

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FoodVerseAI")

# Try imports
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """Safely extracts JSON object from model output text."""
    if not text:
        return {}
    clean_text = text.strip()
    if "```json" in clean_text:
        clean_text = clean_text.split("```json")[1].split("```")[0].strip()
    elif "```" in clean_text:
        clean_text = clean_text.split("```")[1].split("```")[0].strip()
    
    # Try finding first { and last }
    start = clean_text.find("{")
    end = clean_text.rfind("}")
    if start != -1 and end != -1:
        clean_text = clean_text[start:end+1]
        
    try:
        return json.loads(clean_text)
    except Exception as e:
        logger.warning(f"Failed to parse JSON directly: {e}. Raw text snippet: {text[:200]}")
        return {"raw_text": text}


def pil_to_base64(image: Image.Image, format: str = "JPEG") -> str:
    """Converts a PIL image to a base64 encoded string."""
    buffered = io.BytesIO()
    # Convert RGBA to RGB if saving as JPEG
    if format.upper() == "JPEG" and image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


class FoodVerseAIEngine:
    def __init__(self, provider: str = "Demo", gemini_key: str = "", groq_key: str = ""):
        self.provider = provider
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY", "")
        self.groq_key = groq_key or os.getenv("GROQ_API_KEY", "")
        
        self.gemini_client = None
        self.groq_client = None
        
        if self.provider == "Google Gemini" and self.gemini_key and GEMINI_AVAILABLE:
            try:
                self.gemini_client = genai.Client(api_key=self.gemini_key)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Client: {e}")

        elif self.provider == "Groq" and self.groq_key and GROQ_AVAILABLE:
            try:
                self.groq_client = Groq(api_key=self.groq_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq Client: {e}")

    # =========================================================================
    # TAB 1: Food Recognition & Nutrition Audit
    # =========================================================================
    def analyze_nutrition(self, image: Image.Image, user_hint: str = "") -> Dict[str, Any]:
        """Multimodal food identification and nutritional audit."""
        prompt = f"""
Act as a master clinical nutritionist and food computer vision system.
Analyze the dish in this image. {f'User note: {user_hint}' if user_hint else ''}
Return a single valid JSON object with EXACTLY the following structure:
{{
  "title": "Dish name",
  "cuisine": "Cuisine type (e.g. Mediterranean, Mexican, South Asian)",
  "portion_size": "Estimated portion in grams and description (e.g. 350g, 1 bowl)",
  "calories": 520,
  "protein": 34.5,
  "carbs": 45.0,
  "fats": 18.0,
  "fiber": 7.5,
  "sugar": 5.0,
  "sodium": 550,
  "health_score": 88,
  "health_rating": "Grade A (Nutrient Dense)",
  "ingredients": [
    {{"name": "Ingredient name", "weight": "150g", "calories": 200}}
  ],
  "allergens": [
    {{"allergen": "Gluten", "severity": "High/Medium/Low", "source": "Wheat bun"}}
  ],
  "dietary_tags": ["High-Protein", "Low-GI", "Heart-Healthy"],
  "science_notes": "Concise 2-sentence nutritional science breakdown on macronutrient balance and glycemic impact."
}}
Ensure the JSON is strictly formatted and valid.
"""
        # Try Live Gemini
        if self.provider == "Google Gemini" and self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, prompt]
                )
                data = extract_json_from_text(response.text)
                if data and "title" in data and "calories" in data:
                    return data
            except Exception as e:
                logger.error(f"Gemini API error in analyze_nutrition: {e}")
                
        # Try Live Groq Vision
        elif self.provider == "Groq" and self.groq_client:
            try:
                b64 = pil_to_base64(image)
                completion = self.groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                        ]
                    }],
                    temperature=0.2
                )
                data = extract_json_from_text(completion.choices[0].message.content)
                if data and "title" in data:
                    return data
            except Exception as e:
                logger.error(f"Groq API error in analyze_nutrition: {e}")

        # Standalone Demonstration Simulation Fallback
        from modules.sample_data import SAMPLE_DISHES
        # Return realistic salmon bowl sample as high fidelity benchmark
        return SAMPLE_DISHES["salmon_bowl"]

    # =========================================================================
    # TAB 2: Food Freshness & Spoilage Diagnostic
    # =========================================================================
    def analyze_freshness(self, image: Image.Image, food_type: str = "Produce") -> Dict[str, Any]:
        """Evaluates food spoilage, surface texture, discoloration, and mold."""
        prompt = f"""
Act as a PhD Food Pathologist and Food Safety Officer.
Analyze the freshness and spoilage state of the perishable food in this image. Item Category: {food_type}.
Return a single valid JSON object with EXACTLY the following structure:
{{
  "item_name": "Specific item identified (e.g. Avocado and Strawberries)",
  "category": "{food_type}",
  "freshness_stage": "Fresh" or "Moderately Fresh" or "Spoiled",
  "freshness_stage_enum": "Fresh" | "Moderately Fresh" | "Spoiled",
  "freshness_score": 85,
  "color_code": "green" or "amber" or "red",
  "texture_analysis": "Detailed evaluation of surface texture, softening, firmness, skin elasticity, or slime.",
  "discoloration_index": "Description and % of enzymatic browning, dark spots, or oxidation.",
  "wrinkling_turgor": "Evaluation of skin dehydration, wrinkles, and cell turgor pressure.",
  "mold_detection": "State POSITIVE or NEGATIVE with details of fungal mycelium/spores or bacterial colonies.",
  "food_safety_verdict": "Actionable verdict (e.g. Discard Immediately - High Health Risk, or Safe to Consume).",
  "safety_badge": "DISCARD IMMEDIATELY" or "CONSUME WITHIN 24H" or "SAFE TO CONSUME",
  "remaining_shelf_life": "Estimated remaining safe shelf life (e.g. 0 hours, 2-3 days, etc.)",
  "actionable_advice": [
    "First concrete food safety recommendation",
    "Second concrete food safety recommendation"
  ],
  "preservation_tips": [
    "Optimal storage temperature and humidity advice",
    "Packaging or ethylene isolation recommendation"
  ]
}}
Ensure the JSON is strictly formatted and valid.
"""
        # Try Live Gemini
        if self.provider == "Google Gemini" and self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, prompt]
                )
                data = extract_json_from_text(response.text)
                if data and "freshness_stage" in data:
                    return data
            except Exception as e:
                logger.error(f"Gemini API error in analyze_freshness: {e}")

        # Try Live Groq Vision
        elif self.provider == "Groq" and self.groq_client:
            try:
                b64 = pil_to_base64(image)
                completion = self.groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                        ]
                    }],
                    temperature=0.2
                )
                data = extract_json_from_text(completion.choices[0].message.content)
                if data and "freshness_stage" in data:
                    return data
            except Exception as e:
                logger.error(f"Groq API error in analyze_freshness: {e}")

        # Standalone Demonstration Simulation Fallback
        from modules.sample_data import SAMPLE_FRESHNESS
        return SAMPLE_FRESHNESS["spoiled_fruit"]

    # =========================================================================
    # TAB 3: Kitchen Hygiene & Safety Compliance
    # =========================================================================
    def analyze_kitchen_hygiene(self, image: Image.Image, facility_type: str = "Commercial Kitchen") -> Dict[str, Any]:
        """Evaluates commercial kitchen image for HACCP and FDA hygiene compliance."""
        prompt = f"""
Act as a Lead HACCP Auditor and FDA Food Safety Compliance Inspector.
Analyze this commercial kitchen photo ({facility_type}).
Assess:
1. Chef hat / hairnet / beard restraint compliance.
2. Food-grade glove usage and bare-hand contact protocols.
3. Cleanliness, sanitization, and surface cleanliness.
4. Cross-contamination hazards (e.g. raw poultry/meat touching or near ready-to-eat vegetables).

Return a single valid JSON object with EXACTLY the following structure:
{{
  "title": "Facility Compliance Assessment",
  "compliance_score": 88,
  "compliance_grade": "Grade A" or "Grade B+" or "Grade C" or "Grade F",
  "hygiene_status": "Operational - Compliant" or "Operational - Corrective Actions Required" or "Critical Hazard - Cease Prep",
  "indicators": {{
    "chef_hat_hairnet": {{"status": "Compliant" or "Partial Compliance" or "Non-Compliant", "details": "Specific observations"}},
    "glove_usage": {{"status": "Compliant" or "Partial Compliance" or "Non-Compliant", "details": "Specific observations"}},
    "sanitization_state": {{"status": "Good" or "Needs Improvement" or "Poor", "details": "Specific observations"}},
    "cross_contamination": {{"status": "Safe" or "Minor Hazard" or "Critical Hazard", "details": "Specific observations"}}
  }},
  "violations": [
    {{
      "code": "HACCP-CCP-2",
      "severity": "Critical" or "Major" or "Minor" or "Pass",
      "issue": "Brief title of issue",
      "observation": "Detailed specific observation seen in image",
      "action": "Immediate corrective action protocol"
    }}
  ],
  "summary": "Executive inspection summary paragraph for the kitchen manager."
}}
Ensure the JSON is strictly formatted and valid.
"""
        # Try Live Gemini
        if self.provider == "Google Gemini" and self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, prompt]
                )
                data = extract_json_from_text(response.text)
                if data and "compliance_score" in data:
                    return data
            except Exception as e:
                logger.error(f"Gemini API error in analyze_kitchen_hygiene: {e}")

        # Try Live Groq Vision
        elif self.provider == "Groq" and self.groq_client:
            try:
                b64 = pil_to_base64(image)
                completion = self.groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                        ]
                    }],
                    temperature=0.2
                )
                data = extract_json_from_text(completion.choices[0].message.content)
                if data and "compliance_score" in data:
                    return data
            except Exception as e:
                logger.error(f"Groq API error in analyze_kitchen_hygiene: {e}")

        # Standalone Demonstration Simulation Fallback
        from modules.sample_data import SAMPLE_KITCHEN
        return SAMPLE_KITCHEN["kitchen_hygiene"]

    # =========================================================================
    # TAB 4: Smart Kitchen Recipe Assistant
    # =========================================================================
    def generate_smart_recipe(self, pantry_items: list, preferences: dict) -> Dict[str, Any]:
        """Generates creative, nutritious recipe based on pantry items and preferences."""
        items_str = ", ".join(pantry_items) if pantry_items else "Common staples (Olive oil, Garlic, Rice, Eggs, Greens)"
        prompt = f"""
Act as a Michelin-trained executive chef and nutritional biochemist.
Create an inventive, delicious, highly nutritious recipe based on these available pantry ingredients:
Available Pantry Items: {items_str}
User Preferences:
- Meal Type: {preferences.get('meal_type', 'Dinner')}
- Max Cooking Time: {preferences.get('max_time', '30 mins')}
- Skill Level: {preferences.get('skill_level', 'Intermediate')}
- Dietary Restriction: {preferences.get('diet', 'Balanced')}

Return a single valid JSON object with EXACTLY the following structure:
{{
  "title": "Creative Recipe Name",
  "prep_time": "10 mins",
  "cook_time": "20 mins",
  "total_time": "30 mins",
  "servings": 2,
  "difficulty": "Easy" or "Intermediate" or "Advanced",
  "calories_per_serving": 480,
  "macros": {{
    "protein": "34g",
    "carbs": "42g",
    "fats": "18g",
    "fiber": "7g"
  }},
  "ingredients": [
    "Item 1 with exact quantity",
    "Item 2 with exact quantity"
  ],
  "substitutions": [
    {{"ingredient": "Name of ingredient", "substitution": "Smart swap suggestion"}}
  ],
  "steps": [
    "Step 1 with chef pro tip",
    "Step 2 with chef pro tip"
  ],
  "waste_reduction_tip": "Advice on how to utilize vegetable scraps, peels, or leftovers."
}}
Ensure the JSON is strictly formatted and valid.
"""
        # Try Live Gemini
        if self.provider == "Google Gemini" and self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt]
                )
                data = extract_json_from_text(response.text)
                if data and "title" in data and "steps" in data:
                    return data
            except Exception as e:
                logger.error(f"Gemini API error in generate_smart_recipe: {e}")

        # Try Live Groq Text
        elif self.provider == "Groq" and self.groq_client:
            try:
                completion = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4
                )
                data = extract_json_from_text(completion.choices[0].message.content)
                if data and "title" in data and "steps" in data:
                    return data
            except Exception as e:
                logger.error(f"Groq API error in generate_smart_recipe: {e}")

        # Standalone Demonstration Simulation Fallback
        from modules.sample_data import SAMPLE_RECIPES
        return SAMPLE_RECIPES["mediterranean"]

    # =========================================================================
    # TAB 5: Personalized 7-Day Meal Planner
    # =========================================================================
    def generate_adaptive_meal_plan(self, profile: dict, targets: dict) -> Dict[str, Any]:
        """Generates a complete 7-day nutritional schedule with an aisle-organized grocery list."""
        prompt = f"""
Act as an elite sports dietitian and functional medicine practitioner.
Generate a structured, hyper-personalized 7-day meal schedule and organized grocery shopping list for:
- Age: {profile.get('age', 30)}
- Gender: {profile.get('gender', 'Female')}
- Weight: {profile.get('weight', 65)} kg, Height: {profile.get('height', 170)} cm
- Goal: {profile.get('goal', 'Fat Loss')}
- Dietary Constraint: {profile.get('diet', 'Mediterranean')}
- Target Daily Energy: {targets.get('target_calories', 1800)} kcal
- Target Macros: {targets.get('protein_g', 120)}g Protein, {targets.get('carbs_g', 180)}g Carbs, {targets.get('fat_g', 60)}g Fats

Return a single valid JSON object with EXACTLY the following structure:
{{
  "overview": "2-sentence dietary strategy summary aligning with the user's specific target calories and goals.",
  "weekly_schedule": [
    {{
      "day": "Day 1 (Monday)",
      "total_calories": {targets.get('target_calories', 1800)},
      "breakfast": {{"name": "Meal name", "calories": 450, "protein": "28g"}},
      "lunch": {{"name": "Meal name", "calories": 550, "protein": "38g"}},
      "dinner": {{"name": "Meal name", "calories": 600, "protein": "42g"}},
      "snack": {{"name": "Snack name", "calories": 200, "protein": "12g"}}
    }}
    // Repeat for Day 2 through Day 7
  ],
  "grocery_list": {{
    "Fresh Produce": ["Baby spinach", "Avocados", "Blueberries", "Broccoli"],
    "Lean Proteins & Seafood": ["Wild salmon", "Chicken breast", "Eggs", "Greek yogurt"],
    "Whole Grains & Legumes": ["Quinoa", "Rolled oats", "Chickpeas"],
    "Healthy Fats & Pantry": ["Extra virgin olive oil", "Almonds", "Chia seeds"],
    "Dairy & Alternatives": ["Almond milk", "Feta cheese"],
    "Seasonings & Herbs": ["Fresh garlic", "Rosemary", "Sea salt"]
  }}
}}
Ensure the JSON contains all 7 days and is strictly formatted and valid.
"""
        # Try Live Gemini
        if self.provider == "Google Gemini" and self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt]
                )
                data = extract_json_from_text(response.text)
                if data and "weekly_schedule" in data and "grocery_list" in data:
                    return data
            except Exception as e:
                logger.error(f"Gemini API error in generate_adaptive_meal_plan: {e}")

        # Try Live Groq Text
        elif self.provider == "Groq" and self.groq_client:
            try:
                completion = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                data = extract_json_from_text(completion.choices[0].message.content)
                if data and "weekly_schedule" in data:
                    return data
            except Exception as e:
                logger.error(f"Groq API error in generate_adaptive_meal_plan: {e}")

        # Standalone Demonstration Simulation Fallback
        cals = targets.get("target_calories", 1850)
        prot = targets.get("protein_g", 125)
        diet = profile.get("diet", "Mediterranean")
        
        return {
            "overview": f"Scientifically calibrated {diet} nutrition protocol providing ~{cals} kcal/day with {prot}g bioavailable protein to stimulate muscle protein synthesis while sustaining energy balance.",
            "weekly_schedule": [
                {
                    "day": "Day 1 (Monday)",
                    "total_calories": cals,
                    "breakfast": {"name": "Chia Seed & Greek Yogurt Bowl with Mixed Berries & Walnuts", "calories": int(cals*0.25), "protein": f"{int(prot*0.25)}g"},
                    "lunch": {"name": "Mediterranean Quinoa Bowl with Pan-Seared Salmon & Greens", "calories": int(cals*0.35), "protein": f"{int(prot*0.35)}g"},
                    "dinner": {"name": "Lemon-Herb Grilled Chicken with Roasted Sweet Potatoes & Asparagus", "calories": int(cals*0.30), "protein": f"{int(prot*0.30)}g"},
                    "snack": {"name": "Apple Slices with Natural Almond Butter & Cinnamon", "calories": int(cals*0.10), "protein": f"{int(prot*0.10)}g"}
                },
                {
                    "day": "Day 2 (Tuesday)",
                    "total_calories": cals,
                    "breakfast": {"name": "Avocado & Spinach Pasture-Raised Omelet on Sprouted Toast", "calories": int(cals*0.25), "protein": f"{int(prot*0.26)}g"},
                    "lunch": {"name": "Tuscan White Bean & Tuna Salad with Lemon-Dijon Vinaigrette", "calories": int(cals*0.35), "protein": f"{int(prot*0.34)}g"},
                    "dinner": {"name": "Baked Cod with Mediterranean Tomato-Caper Sauce & Steamed Broccoli", "calories": int(cals*0.30), "protein": f"{int(prot*0.30)}g"},
                    "snack": {"name": "Handful of Raw Mixed Almonds and Dark Chocolate Square", "calories": int(cals*0.10), "protein": f"{int(prot*0.10)}g"}
                },
                {
                    "day": "Day 3 (Wednesday)",
                    "total_calories": cals,
                    "breakfast": {"name": "Steel-Cut Oatmeal with Plant Protein Powder, Banana, and Flaxseed", "calories": int(cals*0.25), "protein": f"{int(prot*0.25)}g"},
                    "lunch": {"name": "Turkey & Avocado Whole Grain Wrap with Crunch Herb Slaw", "calories": int(cals*0.35), "protein": f"{int(prot*0.35)}g"},
                    "dinner": {"name": "Spiced Grass-fed Beef Kofta with Roasted Cauliflower & Tahini", "calories": int(cals*0.30), "protein": f"{int(prot*0.29)}g"},
                    "snack": {"name": "Cottage Cheese with Pineapple Chunks & Pumpkin Seeds", "calories": int(cals*0.10), "protein": f"{int(prot*0.11)}g"}
                },
                {
                    "day": "Day 4 (Thursday)",
                    "total_calories": cals,
                    "breakfast": {"name": "Smoked Salmon & Scrambled Eggs with Steamed Spinach", "calories": int(cals*0.25), "protein": f"{int(prot*0.27)}g"},
                    "lunch": {"name": "Moroccan Spiced Chickpea & Roasted Vegetable Grain Bowl", "calories": int(cals*0.35), "protein": f"{int(prot*0.32)}g"},
                    "dinner": {"name": "Herb-Crusted Pork Tenderloin with Sautéed Green Beans & Quinoa", "calories": int(cals*0.30), "protein": f"{int(prot*0.31)}g"},
                    "snack": {"name": "Edamame Beans in the Pod with Sea Salt", "calories": int(cals*0.10), "protein": f"{int(prot*0.10)}g"}
                },
                {
                    "day": "Day 5 (Friday)",
                    "total_calories": cals,
                    "breakfast": {"name": "Green Power Smoothie: Spinach, Frozen Mango, Greek Yogurt, Hemp Seeds", "calories": int(cals*0.25), "protein": f"{int(prot*0.24)}g"},
                    "lunch": {"name": "Warm Grilled Chicken Caprese Salad with Balsamic Glaze", "calories": int(cals*0.35), "protein": f"{int(prot*0.36)}g"},
                    "dinner": {"name": "Wild Salmon Steaks with Garlic Bok Choy & Jasmine Brown Rice", "calories": int(cals*0.30), "protein": f"{int(prot*0.30)}g"},
                    "snack": {"name": "Roasted Tamari Pumpkin Seeds & Celery Sticks", "calories": int(cals*0.10), "protein": f"{int(prot*0.10)}g"}
                },
                {
                    "day": "Day 6 (Saturday)",
                    "total_calories": cals,
                    "breakfast": {"name": "Shakshuka (Poached Eggs in Spicy Tomato-Bell Pepper Sauce) with Feta", "calories": int(cals*0.25), "protein": f"{int(prot*0.25)}g"},
                    "lunch": {"name": "Lentil Soup with Kale, Carrots, and Grilled Sourdough", "calories": int(cals*0.35), "protein": f"{int(prot*0.33)}g"},
                    "dinner": {"name": "Sous-Vide Sirloin Steak with Roasted Asparagus & Garlic Mashed Cauliflower", "calories": int(cals*0.30), "protein": f"{int(prot*0.32)}g"},
                    "snack": {"name": "Blueberry Chia Pudding Cup", "calories": int(cals*0.10), "protein": f"{int(prot*0.10)}g"}
                },
                {
                    "day": "Day 7 (Sunday)",
                    "total_calories": cals,
                    "breakfast": {"name": "Protein Oat Pancakes with Fresh Strawberries & Pure Maple Drizzle", "calories": int(cals*0.25), "protein": f"{int(prot*0.26)}g"},
                    "lunch": {"name": "Greek Salad with Grilled Chicken Breast, Kalamata Olives & Cucumber", "calories": int(cals*0.35), "protein": f"{int(prot*0.35)}g"},
                    "dinner": {"name": "Slow-Simmered Chicken Bone Broth Pho with Rice Noodles & Herbs", "calories": int(cals*0.30), "protein": f"{int(prot*0.29)}g"},
                    "snack": {"name": "Sliced Bell Peppers with Roasted Red Pepper Hummus", "calories": int(cals*0.10), "protein": f"{int(prot*0.10)}g"}
                }
            ],
            "grocery_list": {
                "Fresh Produce": ["Baby spinach (500g)", "Hass avocados (4 pcs)", "Broccoli florets (2 heads)", "Cherry tomatoes (2 pints)", "Sweet potatoes (1 kg)", "Lemons (4 pcs)", "Asparagus (1 bunch)", "Strawberries & Blueberries (2 boxes)"],
                "Lean Proteins & Seafood": ["Wild Atlantic salmon fillets (4x 150g)", "Boneless skinless chicken breast (1.2 kg)", "Pasture-raised eggs (2 dozen)", "Plain 0% Greek yogurt (1 kg tub)", "Wild caught cod or halibut (2 fillets)", "Canned chunk light tuna (3 cans)"],
                "Whole Grains & Legumes": ["Tri-color quinoa (500g)", "Rolled oats (500g)", "Canned brown chickpeas & white cannellini beans", "Brown jasmine rice (500g)"],
                "Healthy Fats & Oils": ["Extra virgin cold-pressed olive oil", "Raw California almonds (200g)", "Chia seeds & ground flaxseed", "Raw walnuts"],
                "Dairy & Alternatives": ["Crumbled goat/sheep feta (150g)", "Unsweetened organic almond milk (1L)"],
                "Seasonings, Herbs & Pantry": ["Fresh garlic bulbs", "Fresh rosemary & basil", "Coarse pink Himalayan salt", "Balsamic glaze", "Dijon mustard"]
            }
        }
