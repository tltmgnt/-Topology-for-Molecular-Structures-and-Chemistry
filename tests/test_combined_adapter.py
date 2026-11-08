import unittest
from unittest.mock import patch
from researchos import domain


class CombinedAdapterTests(unittest.TestCase):
    def test_both_scoped_calculations_are_captured(self):
        result=domain.check()
        self.assertTrue(result['passed'])
        self.assertEqual(result['observed']['explicit_graph']['explicit_atom_formula'],'H2O')
        self.assertEqual(result['observed']['ring']['wiener_index'],27)
        self.assertLess(abs(abs(result['observed']['link']['estimate'])-1),.002)

    def test_either_toolkit_failure_blocks_receipt(self):
        with patch.object(domain,'analyze',return_value={'explicit_atom_formula':'wrong','cycle_rank':0}):
            self.assertFalse(domain.check()['passed'])
        with patch.object(domain,'linking_number',return_value={'estimate':0}):
            self.assertFalse(domain.check()['passed'])
