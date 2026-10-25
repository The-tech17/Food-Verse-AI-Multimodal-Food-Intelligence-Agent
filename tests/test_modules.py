"""
Food Verse AI - Test Suite
Verifies computational accuracy, data structures, and module stability.
"""

import unittest
from PIL import Image
from modules.sample_data import get_sample_image, SAMPLE_DISHES, SAMPLE_FRESHNESS, SAMPLE_KITCHEN, SAMPLE_RECIPES
from modules.meal_planner import calculate_bmr_and_tdee
from modules.ai_engine import FoodVerseAIEngine, extract_json_from_text

class TestFoodVerseAI(unittest.TestCase):

    def test_sample_image_loader(self):
        """Verifies that sample images load properly or fall back cleanly."""
        img = get_sample_image("salmon_bowl")
        self.assertIsNotNone(img)
        self.assertIsInstance(img, Image.Image)
        
        img_mold = get_sample_image("spoiled_fruit")
        self.assertIsNotNone(img_mold)

        img_kitchen = get_sample_image("kitchen_hygiene")
        self.assertIsNotNone(img_kitchen)

    def test_bmr_calculation_male(self):
        """
        Mifflin-St Jeor test for Male:
        Age 30, Male, 80kg, 180cm
        BMR = 10(80) + 6.25(180) - 5(30) + 5
            = 800 + 1125 - 150 + 5 = 1780 kcal
        """
        res = calculate_bmr_and_tdee(
            age=30,
            gender="Male",
            weight_kg=80.0,
            height_cm=180.0,
            activity="Moderately Active (Exercise 3-5 days/week)", # 1.55
            goal="Maintenance (Sustain Energy Balance)",
            diet="Mediterranean"
        )
        self.assertEqual(res["bmr"], 1780)
        # TDEE = 1780 * 1.55 = 2759
        self.assertEqual(res["tdee"], 2759)
        self.assertEqual(res["target_calories"], 2759)

    def test_bmr_calculation_female(self):
        """
        Mifflin-St Jeor test for Female:
        Age 28, Female, 60kg, 165cm
        BMR = 10(60) + 6.25(165) - 5(28) - 161
            = 600 + 1031.25 - 140 - 161 = 1330.25 -> 1330
        """
        res = calculate_bmr_and_tdee(
            age=28,
            gender="Female",
            weight_kg=60.0,
            height_cm=165.0,
            activity="Sedentary (Little or no exercise)", # 1.2
            goal="Fat Loss (Moderate -300 kcal)",
            diet="High Protein"
        )
        self.assertEqual(res["bmr"], 1330)
        # TDEE = 1330 * 1.2 = 1596
        self.assertEqual(res["tdee"], 1596)
        # Target = 1596 - 300 = 1296
        self.assertEqual(res["target_calories"], 1296)

    def test_json_extractor(self):
        """Tests JSON parser with markdown code blocks and whitespace."""
        text1 = '```json\n{"dish": "Salmon Bowl", "score": 95}\n```'
        parsed1 = extract_json_from_text(text1)
        self.assertEqual(parsed1.get("dish"), "Salmon Bowl")
        self.assertEqual(parsed1.get("score"), 95)

        text2 = 'Some model chatter before {"status": "ok"} and after'
        parsed2 = extract_json_from_text(text2)
        self.assertEqual(parsed2.get("status"), "ok")

    def test_demo_ai_engine(self):
        """Verifies that the Demo AI engine produces complete schemas for all 5 tabs."""
        engine = FoodVerseAIEngine(provider="Demo")
        dummy_img = Image.new("RGB", (100, 100), color=(16, 185, 129))
        
        # Tab 1
        nutr = engine.analyze_nutrition(dummy_img)
        self.assertIn("calories", nutr)
        self.assertIn("protein", nutr)
        self.assertIn("health_score", nutr)

        # Tab 2
        fresh = engine.analyze_freshness(dummy_img)
        self.assertIn("freshness_stage", fresh)
        self.assertIn("freshness_score", fresh)

        # Tab 3
        hyg = engine.analyze_kitchen_hygiene(dummy_img)
        self.assertIn("compliance_score", hyg)
        self.assertIn("indicators", hyg)

        # Tab 4
        rec = engine.generate_smart_recipe(["Chicken", "Rice"], {})
        self.assertIn("title", rec)
        self.assertIn("steps", rec)

        # Tab 5
        plan = engine.generate_adaptive_meal_plan({"age": 30}, {"target_calories": 2000})
        self.assertIn("weekly_schedule", plan)
        self.assertIn("grocery_list", plan)
        self.assertEqual(len(plan["weekly_schedule"]), 7)

if __name__ == "__main__":
    unittest.main()
