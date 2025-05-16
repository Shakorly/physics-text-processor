from physics_text_processor import RobustPhysicsTextProcessor

processor = RobustPhysicsTextProcessor()
text = "   Sample physics text with 10×10⁻³² unicode   "
cleaned = processor.process(text)

print(f"Original: {text!r}")
print(f"Cleaned: {cleaned!r}")