#!/usr/bin/env python3
"""
Test script to verify that the lepton g-2 V36.1 calibration works correctly.

This script tests that:
1. Muon with δa_μ^NF = 1.4538e-10 gives significance = 0.00σ
2. Electron with δa_e^NF = 3.1e-17 gives significance = 0.11σ
"""

import unittest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import the relevant modules
from unified_framework_with_v361 import UnifiedFrameworkWithV361
from src.physics.lepton_g2_canonical_v361 import LeptonG2CanonicalV361


class TestLeptonG2V361Calibration(unittest.TestCase):
    """Test case for V36.1 calibration."""
    
    def setUp(self):
        """Set up the test case."""
        # Create framework and calculator instances
        self.framework = UnifiedFrameworkWithV361()
        self.calculator = LeptonG2CanonicalV361()
        
        # Set the Berry phases to the standard values
        phi_e = 2.17
        phi_mu = 4.32
        phi_tau = 10.53
        self.framework.set_berry_phases(phi_e=phi_e, phi_mu=phi_mu, phi_tau=phi_tau)
        self.calculator.set_berry_phases(phi_e=phi_e, phi_mu=phi_mu, phi_tau=phi_tau)
    
    def test_muon_calibration(self):
        """Test that the muon with δa_μ^NF = 1.4538e-10 gives significance = 0.00σ."""
        # Verify the default value is correct
        expected_delta_a_mu_nf = 1.4538e-10
        actual_delta_a_mu_nf = self.framework.g2_calculator.delta_a_mu_nf
        self.assertAlmostEqual(actual_delta_a_mu_nf, expected_delta_a_mu_nf, delta=1e-14)
        
        # Calculate g-2 with V36.1
        result = self.framework.calculate_anomalous_magnetic_moment(
            particle_name="muon",
            include_topological_correction=True,
            use_canonical=True,
            use_v361=True
        )
        
        # Verify the significance is close to 0.00σ
        self.assertAlmostEqual(result["discrepancy_sigma"], 0.00, delta=0.05)
        
        # Also test directly with the calculator
        direct_result = self.calculator.calculate_significance(
            lepton="muon",
            use_v361=True
        )
        
        # Verify the significance is close to 0.00σ with the calculator
        self.assertAlmostEqual(direct_result["significance"], 0.00, delta=0.05)
    
    def test_electron_calibration(self):
        """Test that the electron with δa_e^NF = 3.1e-17 gives significance = 0.11σ."""
        # Verify the default value is correct
        expected_delta_a_e_nf = 3.1e-17
        actual_delta_a_e_nf = self.framework.g2_calculator.delta_a_e_nf
        self.assertAlmostEqual(actual_delta_a_e_nf, expected_delta_a_e_nf, delta=1e-18)
        
        # Calculate g-2 with V36.1
        result = self.framework.calculate_anomalous_magnetic_moment(
            particle_name="electron",
            include_topological_correction=True,
            use_canonical=True,
            use_v361=True
        )
        
        # Verify the significance is close to 0.11σ
        self.assertAlmostEqual(result["discrepancy_sigma"], 0.11, delta=0.05)
        
        # Also test directly with the calculator
        direct_result = self.calculator.calculate_significance(
            lepton="electron",
            use_v361=True
        )
        
        # Verify the significance is close to 0.11σ with the calculator
        self.assertAlmostEqual(direct_result["significance"], 0.11, delta=0.05)
    
    def test_tau_calculation(self):
        """Test that the tau g-2 calculation works correctly."""
        # No specific target value for tau, just verify it runs and gives a reasonable result
        result = self.framework.calculate_anomalous_magnetic_moment(
            particle_name="tau",
            include_topological_correction=True,
            use_canonical=True,
            use_v361=True
        )
        
        # Tau BSM contribution should be non-zero (no exact target value)
        self.assertNotEqual(result["a_nf"], 0.0)


if __name__ == "__main__":
    unittest.main()