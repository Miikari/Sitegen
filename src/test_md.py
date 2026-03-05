import unittest

from markdown_blocks import block_to_block_type, BlockType

class TestTextNode(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(
            BlockType.HEADING, 
            block_to_block_type("# Hei"),
            )
        self.assertEqual(
            BlockType.HEADING, 
            block_to_block_type("###### Hei"),
            )
        self.assertEqual(
            BlockType.PARAGRAPH, 
            block_to_block_type("#Hei"),
            )
        self.assertEqual(
            BlockType.PARAGRAPH, 
            block_to_block_type("####### Hei"),
            )
    def test_code(self):
        self.assertEqual(
            BlockType.CODE, 
            block_to_block_type("```\n Hei ```"),
            )
        self.assertEqual(
            BlockType.PARAGRAPH, 
            block_to_block_type("``` Hei ``"),
            )
        self.assertEqual(
            BlockType.PARAGRAPH, 
            block_to_block_type("`` Hei ``"),
            )
    def test_quote(self):    
        self.assertEqual(
            BlockType.QUOTE, 
            block_to_block_type("> Hei"),
            )
        self.assertEqual(
            BlockType.QUOTE, 
            block_to_block_type(">Hei"),
            )
        self.assertEqual(
            BlockType.QUOTE, 
            block_to_block_type(">Hei\n>Moi\n>Terve"),
            )
        self.assertEqual(
            BlockType.PARAGRAPH, 
            block_to_block_type(">Hei\n>Moi\nTerve"),
            )
        self.assertEqual(
            BlockType.PARAGRAPH, 
            block_to_block_type(">Hei\n>Moi\n- Terve"),
            )
        
    def test_unordered(self):
        self.assertEqual(
            BlockType.UNORDERED,
            block_to_block_type("- Hei"),
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("-Hei"),
        )
        self.assertEqual(
            BlockType.UNORDERED,
            block_to_block_type("- Hei\n- Moi\n- Terve"),
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("- Hei\n - Moi\n -Terve"),
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("- Hei\n -  Moi\n - Terve"),
        )
    def test_ordered(self):
        self.assertEqual(
            BlockType.ORDERED,
            block_to_block_type("1. Hei"),
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("1.Hei"),
        )
        self.assertEqual(
            BlockType.ORDERED,
            block_to_block_type("1. Hei \n2. Moi\n3. Terve"),
        )   
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("1. Hei \n2. Moi\n3.Terve"),
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("1. Hei \n3. Moi\n4. Terve"),
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("Hei \n2. Moi\n3. Terve"),
        )
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("1. Hei \n2. Moi\nTerve"),
        ) 
    

if __name__ == "__main__":
    unittest.main()