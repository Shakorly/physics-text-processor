from physics_text_processor import RobustPhysicsTextProcessor

def test():
    assert RobustPhysicsTextProcessor().process(" hello ") == "hello"

if __name__ == "__main__":
    test()