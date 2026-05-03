import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class PremiumFlowTests(unittest.TestCase):
    def test_premium_modules_import(self):
        from handlers import payment, pitch, questions  # noqa: F401

    def test_services_keyboard_has_four_options(self):
        from handlers.pitch import PITCH_MAIN, _services_keyboard

        keyboard = _services_keyboard()
        button_texts = [
            button.text
            for row in keyboard.inline_keyboard
            for button in row
        ]

        self.assertIn("Decode Your Future", PITCH_MAIN)
        self.assertEqual(len(button_texts), 4)
        self.assertIn("🅰️ Vedic Basic — ₹499", button_texts)
        self.assertIn("🅱️ Vedic Premium — ₹1100", button_texts)
        self.assertIn("🅲 Numerology Basic — ₹399", button_texts)
        self.assertIn("🅳 Numerology Premium — ₹1100", button_texts)


if __name__ == "__main__":
    unittest.main()
