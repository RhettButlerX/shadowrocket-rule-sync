import unittest
from scripts.update_rules import extract_direct

class ExtractTests(unittest.TestCase):
    def test_keeps_only_direct_in_rule_section(self):
        lines = ["[General]", "DOMAIN-SUFFIX,ignored.com,DIRECT", "[Rule]"]
        lines += [f"DOMAIN-SUFFIX,d{i}.example,DIRECT" for i in range(110)]
        lines += ["DOMAIN-SUFFIX,proxy.example,Proxy", "DOMAIN-SUFFIX,blocked.example,REJECT", "[MITM]", "DOMAIN-SUFFIX,late.example,DIRECT"]
        rules = extract_direct("\n".join(lines))
        self.assertEqual(len(rules), 110)
        self.assertIn("DOMAIN-SUFFIX,d1.example", rules)
        self.assertTrue(all(len(x.split(",")) == 2 for x in rules))

    def test_rejects_empty_source(self):
        with self.assertRaises(ValueError):
            extract_direct("[Rule]\nFINAL,Proxy")

if __name__ == "__main__":
    unittest.main()
