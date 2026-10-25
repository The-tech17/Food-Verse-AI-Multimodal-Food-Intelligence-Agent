"""
Food Verse AI - Sample Data & Presets
Provides rich, realistic sample inputs and datasets for instant 1-click evaluation.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "samples")

def get_sample_image(sample_key: str):
    """
    Retrieves the PIL image for the requested sample key,
    or generates a clean aesthetic placeholder card if the file is missing.
    """
    file_map = {
        "salmon_bowl": "salmon_bowl.jpg",
        "spoiled_fruit": "spoiled_fruit.jpg",
        "kitchen_hygiene": "kitchen_hygiene.jpg"
    }
    
    filename = file_map.get(sample_key)
    if filename:
        full_path = os.path.join(ASSETS_SAMPLE_DIR, filename)
        if os.path.exists(full_path):
            try:
                with Image.open(full_path) as img:
                    return img.copy()
            except Exception:
                pass
                
    # Fallback synthetic badge image
    img = Image.new("RGB", (600, 600), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 580, 580], outline=(16, 185, 129), width=4)
    # Simple label
    draw.text((100, 280), f"FoodVerse Sample: {sample_key.replace('_', ' ').title()}", fill=(248, 250, 252))
    draw.text((100, 320), "Multimodal Vision Analysis Ready", fill=(148, 163, 184))
    return img

SAMPLE_DISHES = {
    "salmon_bowl": {
        "title": "Mediterranean Grilled Salmon & Quinoa Bowl",
        "image_key": "salmon_bowl",
        "cuisine": "Mediterranean / Healthy Contemporary",
        "portion_size": "420g (Single Serving)",
        "calories": 585,
        "protein": 42.5,
        "carbs": 48.0,
        "fats": 22.0,
        "fiber": 8.5,
        "sugar": 4.2,
        "sodium": 480,
        "health_score": 94,
        "health_rating": "Superfood Tier (A+)",
        "ingredients": [
            {"name": "Wild Atlantic Salmon Fillet (Pan-seared)", "weight": "170g", "calories": 280},
            {"name": "Tri-Color Quinoa (Cooked)", "weight": "120g", "calories": 145},
            {"name": "Hass Avocado (Fresh slices)", "weight": "50g", "calories": 80},
            {"name": "Steamed Tenderstem Broccoli", "weight": "80g", "calories": 28},
            {"name": "Heirloom Cherry Tomatoes & Herbs", "weight": "40g", "calories": 15},
            {"name": "Toasted Sesame & Citrus Glaze", "weight": "15g", "calories": 37}
        ],
        "allergens": [
            {"allergen": "Fish", "severity": "High", "source": "Wild Atlantic Salmon"},
            {"allergen": "Sesame", "severity": "Medium", "source": "Sesame seeds & dressing"}
        ],
        "dietary_tags": ["High-Protein", "Heart-Healthy Omega-3", "Low-GI", "Dairy-Free", "Clean Fuel"],
        "science_notes": "Optimal 1:1.1 protein-to-carb ratio with anti-inflammatory EPA/DHA omega-3 fatty acids and 8.5g prebiotic soluble fiber for steady glycemic control."
    },
    "cheeseburger": {
        "title": "Artisan Double Smash Cheeseburger & Seasoned Fries",
        "image_key": "salmon_bowl", # fallback or custom
        "cuisine": "American Gourmet",
        "portion_size": "560g (Single Serving)",
        "calories": 1140,
        "protein": 52.0,
        "carbs": 94.0,
        "fats": 62.0,
        "fiber": 4.0,
        "sugar": 14.5,
        "sodium": 1680,
        "health_score": 46,
        "health_rating": "High Calorie / Indulgence (C)",
        "ingredients": [
            {"name": "Grass-fed Beef Patties (80/20 double smash)", "weight": "220g", "calories": 540},
            {"name": "Brioche Bun (Toasted with butter)", "weight": "85g", "calories": 230},
            {"name": "Aged Cheddar Slices", "weight": "40g", "calories": 160},
            {"name": "Crispy Skin-on French Fries", "weight": "160g", "calories": 360},
            {"name": "House Secret Aioli Sauce", "weight": "30g", "calories": 140}
        ],
        "allergens": [
            {"allergen": "Gluten / Wheat", "severity": "High", "source": "Brioche bun"},
            {"allergen": "Dairy", "severity": "High", "source": "Aged cheddar & butter"},
            {"allergen": "Eggs", "severity": "Medium", "source": "Aioli sauce"}
        ],
        "dietary_tags": ["High-Protein", "High-Sodium", "High-Saturated-Fat", "Elevated Glycemic Load"],
        "science_notes": "Caloric density of 2.03 kcal/g with 1680mg sodium (73% of daily FDA threshold). Saturated fatty acids comprise 44% of total fat content."
    },
    "vegan_buddha": {
        "title": "Rainbow Vegan Tahini Buddha Bowl",
        "image_key": "salmon_bowl",
        "cuisine": "Plant-Based Fusion",
        "portion_size": "450g (Single Serving)",
        "calories": 490,
        "protein": 21.0,
        "carbs": 64.0,
        "fats": 18.0,
        "fiber": 14.2,
        "sugar": 7.0,
        "sodium": 320,
        "health_score": 96,
        "health_rating": "Nutritional Powerhouse (A+)",
        "ingredients": [
            {"name": "Crispy Roasted Chickpeas", "weight": "110g", "calories": 160},
            {"name": "Steamed Brown Jasmine Rice", "weight": "100g", "calories": 130},
            {"name": "Purple Cabbage & Grated Carrots", "weight": "90g", "calories": 35},
            {"name": "Marinated Edamame Beans", "weight": "60g", "calories": 75},
            {"name": "Lemon-Garlic Tahini Dressing", "weight": "30g", "calories": 90}
        ],
        "allergens": [
            {"allergen": "Sesame", "severity": "Medium", "source": "Tahini paste"},
            {"allergen": "Soy", "severity": "Medium", "source": "Edamame"}
        ],
        "dietary_tags": ["100% Vegan", "Ultra High-Fiber", "Antioxidant Rich", "Cholesterol-Free", "Gut-Health"],
        "science_notes": "Contains 14.2g dietary fiber (51% RDA) promoting microbiome diversity and short-chain fatty acid (SCFA) production. Abundant anthocyanins from purple cabbage."
    }
}

SAMPLE_FRESHNESS = {
    "spoiled_fruit": {
        "item_name": "Fresh Strawberries & Avocado Half",
        "image_key": "spoiled_fruit",
        "category": "Perishable Fresh Produce",
        "freshness_stage": "Spoiled",
        "freshness_stage_enum": "Spoiled",
        "freshness_score": 18,
        "color_code": "red",
        "texture_analysis": "Severe breakdown of cellular structure; mushy collapsing parenchyma with water-soaked spots.",
        "discoloration_index": "82% oxidation; dark brown necrotic enzymatic browning across avocado flesh and strawberry calyx.",
        "wrinkling_turgor": "Significant loss of turgor pressure (skin flaccid, shriveled epidermis).",
        "mold_detection": "POSITIVE (High fungal density) - Visible grey-white mycelium tufts of Botrytis cinerea (grey mold) on strawberries and fungal hyphae in avocado cavity.",
        "food_safety_verdict": "Discard Immediately - High Health Risk",
        "safety_badge": "DISCARD IMMEDIATELY",
        "remaining_shelf_life": "0 Hours (Expired / Bio-hazard)",
        "actionable_advice": [
            "Do NOT cut off the moldy sections and eat the rest; mycotoxins (e.g. patulin) penetrate deep into soft, high-moisture fruits.",
            "Seal in a compostable bag immediately to prevent airborne fungal spores from contaminating adjacent produce in your refrigerator.",
            "Wash and sanitize the wooden cutting board with a chlorine bleach dilution or food-grade sanitizer before reuse."
        ],
        "preservation_tips": [
            "Store fresh berries unwashed in a breathable container lined with paper towels at 0-2°C (32-35°F).",
            "Store cut avocado tightly wrapped in plastic film with the pit intact or submerged in water inside an airtight container.",
            "Maintain refrigerator humidity at 85-90% for leafy greens and 65-75% for berries."
        ]
    },
    "fresh_apple": {
        "item_name": "Organic Honeycrisp Apple",
        "image_key": "salmon_bowl",
        "category": "Pome Fruit",
        "freshness_stage": "Fresh",
        "freshness_stage_enum": "Fresh",
        "freshness_score": 96,
        "color_code": "green",
        "texture_analysis": "Firm, crisp cell walls with intact cellular turgidity and no soft depressions.",
        "discoloration_index": "3% natural blush variance; zero oxidation or bruising.",
        "wrinkling_turgor": "100% skin turgor; taut epicuticular wax cuticle intact.",
        "mold_detection": "NEGATIVE (0% mycelium spores detected).",
        "food_safety_verdict": "Safe to Consume (Fresh Crisp State)",
        "safety_badge": "SAFE TO CONSUME",
        "remaining_shelf_life": "14-21 Days (Refrigerated) / 5-7 Days (Room Temp)",
        "actionable_advice": [
            "Rinse under cold running water for 30 seconds before eating to remove natural dust and surface microbes.",
            "Optimal for raw consumption, salads, or cold-pressed juicing."
        ],
        "preservation_tips": [
            "Keep stored at 1-3°C (34-37°F) with high relative humidity.",
            "Keep separate from ethylene-sensitive vegetables as apples emit ethylene gas."
        ]
    },
    "ripe_banana": {
        "item_name": "Cavendish Banana (Sugar Speckled)",
        "image_key": "salmon_bowl",
        "category": "Tropical Fruit",
        "freshness_stage": "Moderately Fresh",
        "freshness_stage_enum": "Moderately Fresh",
        "freshness_score": 72,
        "color_code": "amber",
        "texture_analysis": "Slight softening of mesocarp pulp; skin yielding slightly to gentle pressure.",
        "discoloration_index": "35% surface covered with characteristic brown sugar freckles (senescent spotting).",
        "wrinkling_turgor": "Minor skin thinning and slight neck dehydration; internal fruit remains protected.",
        "mold_detection": "NEGATIVE (No fungal mycelium or crown rot present).",
        "food_safety_verdict": "Safe to Consume - Consume Within 24-48 Hours",
        "safety_badge": "CONSUME WITHIN 24-48H",
        "remaining_shelf_life": "1-2 Days at Room Temp / 4-5 Days in Refrigerator",
        "actionable_advice": [
            "Ideal for immediate raw consumption (peak sweetness, highest simple sugar content).",
            "Perfect candidate for banana bread, smoothies, or freezing in slices for nice-cream."
        ],
        "preservation_tips": [
            "Peel and freeze in airtight silicone bags for future baking.",
            "Wrap the crown stems in plastic wrap to retard ethylene release."
        ]
    }
}

SAMPLE_KITCHEN = {
    "kitchen_hygiene": {
        "title": "Main Restaurant Kitchen Line Inspection",
        "image_key": "kitchen_hygiene",
        "compliance_score": 88,
        "compliance_grade": "Grade B+ (Compliant with Minor Corrective Actions)",
        "hygiene_status": "Operational - Corrective Actions Required",
        "indicators": {
            "chef_hat_hairnet": {"status": "Compliant", "details": "All active food handlers wearing bouffant hairnets and beard restraints."},
            "glove_usage": {"status": "Partial Compliance", "details": "Plating chef wearing nitrile food-safe gloves; sauté cook handling pans bare-handed (permitted for hot cooking, but handwash protocol required before ready-to-eat contact)."},
            "sanitization_state": {"status": "Good", "details": "Stainless steel counters wiped clean; sanitizing spray bucket stationed at station end."},
            "cross_contamination": {"status": "Minor Hazard Detected", "details": "Cutting board shows knife left on edge; poultry prep station is 3 feet from ready-to-eat salad prep without splash barrier."}
        },
        "violations": [
            {
                "code": "HACCP-CCP-2",
                "severity": "Major",
                "issue": "Raw Protein Proximity to Plating Area",
                "observation": "Raw beef tenderloin prep station located directly adjacent to cold garnish line without physical sneeze guard or barrier.",
                "action": "Relocate raw meat preparation to dedicated red-coded board station at least 6 feet away."
            },
            {
                "code": "FDA-FC-3-304",
                "severity": "Minor",
                "issue": "Towel Resting on Cutting Surface",
                "observation": "Damp wiping cloth resting directly on food preparation surface instead of chemical sanitizing bucket (200ppm quaternary ammonium).",
                "action": "Store wiping cloths submerged in sanitizer bucket tested with chlorine/quat test strips."
            },
            {
                "code": "FDA-FC-2-402",
                "severity": "Pass",
                "issue": "Hair Restraints Compliance",
                "observation": "100% compliance with hairnet protocol across all 4 visible kitchen personnel.",
                "action": "Maintain current standard."
            }
        ],
        "summary": "Commercial kitchen displays strong general sanitation and rigorous hair restraint adherence. Immediate remediation required for raw protein station zoning and wiping cloth storage to meet FDA 2022 Food Code standards."
    }
}

SAMPLE_PANTRY_PRESETS = {
    "Mediterranean Wellness": [
        "Salmon Fillet", "Quinoa", "Avocado", "Extra Virgin Olive Oil", 
        "Garlic", "Lemon", "Baby Spinach", "Cherry Tomatoes", "Feta Cheese"
    ],
    "High-Protein Muscle Prep": [
        "Chicken Breast", "Eggs", "Greek Yogurt", "Rolled Oats", 
        "Broccoli", "Sweet Potato", "Natural Peanut Butter", "Olive Oil"
    ],
    "Pantry Cleanout (Student Budget)": [
        "Canned Chickpeas", "Pasta", "Canned Tuna", "Crushed Tomatoes", 
        "Yellow Onion", "Garlic", "Olive Oil", "Chili Flakes", "Parmesan"
    ],
    "Plant-Powered Vegan": [
        "Extra Firm Tofu", "Brown Rice", "Shelled Edamame", "Bell Peppers", 
        "Sesame Oil", "Low-Sodium Soy Sauce", "Ginger", "Sesame Seeds"
    ]
}

SAMPLE_RECIPES = {
    "mediterranean": {
        "title": "20-Minute Pan-Crisped Salmon with Warm Lemon-Spinach Quinoa",
        "prep_time": "8 mins",
        "cook_time": "12 mins",
        "total_time": "20 mins",
        "servings": 2,
        "difficulty": "Easy",
        "calories_per_serving": 490,
        "macros": {"protein": "38g", "carbs": "32g", "fats": "22g", "fiber": "6g"},
        "ingredients": [
            "2 fresh salmon fillets (approx 150g each)",
            "1 cup cooked tri-color quinoa",
            "2 cups fresh baby spinach",
            "1 cup halved cherry tomatoes",
            "2 cloves garlic (minced)",
            "1 tbsp extra virgin olive oil",
            "1/2 lemon (juiced & zested)",
            "30g crumbled feta cheese (optional garnish)"
        ],
        "substitutions": [
            {"ingredient": "Salmon Fillet", "substitution": "Firm tofu slices, chicken breast cutlets, or canned chickpeas"},
            {"ingredient": "Quinoa", "substitution": "Brown rice, farro, couscous, or cauliflower rice for low-carb"},
            {"ingredient": "Feta Cheese", "substitution": "Nutritional yeast flakes or kalamata olives (dairy-free)"}
        ],
        "steps": [
            "Pat salmon fillets dry with a paper towel and season both sides with sea salt, cracked black pepper, and lemon zest.",
            "Heat 1 tbsp extra virgin olive oil in a non-stick skillet over medium-high heat until shimmering.",
            "Place salmon skin-side down. Sear undisturbed for 4-5 minutes until skin is crispy and golden, then flip and cook 3 minutes more.",
            "In the final 2 minutes, push salmon to one side and add minced garlic, cherry tomatoes, and baby spinach. Sauté until wilted.",
            "Toss warm quinoa with lemon juice and pan juices. Plate quinoa topped with salmon, blistered tomatoes, and feta crumble."
        ],
        "waste_reduction_tip": "Keep the lemon rinds for vinegar cleaning infusion or zest into freezer bags for future marinade brightness."
    }
}
