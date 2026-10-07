import unittest
from reliability import agreement,counts
class AgreementTests(unittest.TestCase):
 def test_perfect_variable(self):
  r=agreement([5,0,0,5]);self.assertEqual(r['agreement'],1);self.assertEqual(r['kappa'],1)
 def test_independent_balanced(self):self.assertEqual(agreement([5,5,5,5])['kappa'],0)
 def test_constant(self):self.assertIsNone(agreement([0,0,0,10])['kappa'])
 def test_opposite(self):self.assertEqual(agreement([0,5,5,0])['kappa'],-1)
 def test_known_marginals(self):
  r=agreement([20,5,10,65]);self.assertAlmostEqual(r['agreement'],.85);self.assertAlmostEqual(r['kappa'],.625)
 def test_counts(self):self.assertEqual(counts([(1,1),(1,0),(0,1),(0,0)]),[1,1,1,1])
if __name__=='__main__':unittest.main()
