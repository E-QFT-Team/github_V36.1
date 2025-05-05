#!/usr/bin/env python3
"""
Extension du framework unifié pour intégrer le calcul canonique de g-2 V36.1.

Ce script étend le framework unifié E-QFT V34.8 pour incorporer
la méthode de calcul canonique V36.1 du g-2 des leptons avec
recouvrement par flux de Berry.
"""

import sys
import numpy as np
import logging
from pathlib import Path

# Ajouter le répertoire du projet au chemin Python
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Importer les modules nécessaires
from src.core.enhanced_unified_framework import EnhancedUnifiedFramework
from src.physics.lepton_g2_canonical_v361 import LeptonG2CanonicalV361

# Configuration du logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UnifiedFrameworkWithV361(EnhancedUnifiedFramework):
    """
    Extension du framework unifié avec calcul canonique V36 et V36.1 du g-2 des leptons.
    """
    
    def __init__(self, **kwargs):
        """
        Initialisation avec paramètres hérités et nouveaux.
        """
        # Initialize parent class
        super().__init__(**kwargs)
        
        # Initialize canonical g-2 calculator
        self.g2_calculator = LeptonG2CanonicalV361(chern_class=self.chern_class)
        
        logger.info("Initialized UnifiedFrameworkWithV361")
    
    def compute_g_minus_2_canonical(self, fermion, use_v361=True):
        """
        Calcule la correction g-2 avec l'approche canonique V36 ou V36.1.
        
        Args:
            fermion: Nom du fermion ("muon", "electron", "tau")
            use_v361: Si True, utilise la formule V36.1 avec facteur Ω
            
        Returns:
            Correction g-2 calculée avec l'approche canonique
        """
        if fermion not in ["muon", "electron", "tau"]:
            logger.warning(f"Canonical g-2 calculation not implemented for {fermion}")
            return 0.0
        
        return self.g2_calculator.predict_g2_correction(fermion, use_v361=use_v361)
    
    def compute_g_minus_2(self, fermion, topological_charge, use_canonical=True, use_v361=True):
        """
        Version étendue de compute_g_minus_2 avec options pour méthodes canoniques.
        
        Args:
            fermion: Nom du fermion ("muon", "electron", "tau")
            topological_charge: Charge topologique
            use_canonical: Utiliser l'approche canonique si True
            use_v361: Si True et use_canonical=True, utilise V36.1 au lieu de V36
            
        Returns:
            Correction g-2 calculée
        """
        if fermion in ["muon", "electron", "tau"] and use_canonical:
            version = "V36.1" if use_v361 else "V36"
            logger.info(f"Using canonical {version} approach for {fermion} g-2 calculation")
            return self.compute_g_minus_2_canonical(fermion, use_v361=use_v361)
        else:
            logger.info(f"Using standard approach for {fermion} g-2 calculation")
            return super().compute_g_minus_2(fermion, topological_charge)
    
    def calculate_anomalous_magnetic_moment(self, 
                                          particle_name,
                                          include_topological_correction=True,
                                          use_canonical=True,
                                          use_v361=True):
        """
        Version étendue de calculate_anomalous_magnetic_moment avec options canoniques.
        
        Args:
            particle_name: Nom du fermion ("muon", "electron", "tau")
            include_topological_correction: Inclure la correction topologique
            use_canonical: Utiliser l'approche canonique si True
            use_v361: Si True et use_canonical=True, utilise V36.1 au lieu de V36
            
        Returns:
            Dictionnaire avec tous les détails de calcul
        """
        # Retrieve base result without modifications to get structure
        result = super().calculate_anomalous_magnetic_moment(
            particle_name=particle_name,
            include_topological_correction=False
        )
        
        # Get topological charges for each fermion
        topological_charges = {
            "electron": 1.0, 
            "muon": 2.0, 
            "tau": 4.0
        }
        
        # Add E-QFT topological correction if requested
        if include_topological_correction:
            result["a_nf"] = self.compute_g_minus_2(
                particle_name, 
                topological_charges[particle_name],
                use_canonical=use_canonical,
                use_v361=use_v361
            )
        else:
            result["a_nf"] = 0.0
        
        # Total prediction
        result["a_total"] = result["a_sm"] + result["a_nf"]
        
        # Calculate discrepancy if experimental value is available
        if result["a_exp"] is not None:
            result["discrepancy"] = result["a_exp"] - result["a_total"]
            
            if result["a_exp_uncertainty"] is not None and result["a_exp_uncertainty"] > 0:
                result["discrepancy_sigma"] = result["discrepancy"] / result["a_exp_uncertainty"]
        
        # Add canonical specific information if used
        if particle_name in ["muon", "electron", "tau"] and use_canonical and include_topological_correction:
            # Get detailed info from the calculator
            calc_results = self.g2_calculator.calculate_significance(
                particle_name, 
                a_lepton_eqft=result["a_nf"],
                use_v361=use_v361
            )
            
            # Add canonical info to result
            result["canonical_info"] = {
                "version": "V36.1" if use_v361 else "V36",
                "phi_lepton": calc_results["phi_lepton"],
                "phi_heavy": calc_results["phi_heavy"],
                "c2": calc_results["c2"],
                "lambda_topo": calc_results["lambda_topo"]
            }
            
            # Add omega factor for V36.1
            if use_v361:
                result["canonical_info"]["omega"] = calc_results["omega"]
                
            # Use the significance from the calculator for consistency
            if "significance" in calc_results and calc_results["significance"] is not None:
                result["discrepancy_sigma"] = calc_results["significance"]
        
        version = "V36.1" if use_canonical and use_v361 else "V36" if use_canonical else "standard"
        logger.info(f"Calculated anomalous magnetic moment for {particle_name} using {version} approach: {result['a_total']:.12e}")
        
        return result
    
    def set_berry_phases(self, phi_e=None, phi_mu=None, phi_tau=None):
        """
        Définit les phases de Berry pour les différents leptons.
        
        Args:
            phi_e: Phase de Berry de l'électron
            phi_mu: Phase de Berry du muon
            phi_tau: Phase de Berry du tau
        """
        self.g2_calculator.set_berry_phases(phi_e=phi_e, phi_mu=phi_mu, phi_tau=phi_tau)
    
    def set_delta_a_nf(self, lepton, value):
        """
        Définit la correction brute E-QFT pour un lepton spécifique.
        
        Args:
            lepton: Type de lepton ("electron", "muon", "tau")
            value: Nouvelle valeur pour delta_a_nf
        """
        self.g2_calculator.set_delta_a_nf(lepton, value)
    
    def print_g2_canonical_report(self, lepton="muon", use_v361=True):
        """
        Affiche un rapport détaillé sur le calcul canonique du g-2 d'un lepton.
        
        Args:
            lepton: Type de lepton ("electron", "muon", "tau")
            use_v361: Si True, utilise la formule V36.1
            
        Returns:
            Rapport formaté
        """
        report = self.g2_calculator.generate_report(lepton=lepton, use_v361=use_v361)
        print(report)
        return report


def main():
    """Main function to demonstrate the extended framework."""
    # Créer une instance du framework étendu
    framework = UnifiedFrameworkWithV361()
    
    print("\n=== Test des implémentations canoniques V36 et V36.1 pour g-2 ===\n")
    
    # Définir les phases de Berry optimales
    framework.set_berry_phases(phi_e=2.17, phi_mu=4.32, phi_tau=10.53)
    
    # ===== Tests pour le Muon =====
    print("=== MUON ===")
    
    # Calculer g-2 avec l'approche standard
    result_standard = framework.calculate_anomalous_magnetic_moment(
        particle_name="muon",
        include_topological_correction=True,
        use_canonical=False
    )
    
    # Calculer g-2 avec l'approche canonique V36
    result_v36 = framework.calculate_anomalous_magnetic_moment(
        particle_name="muon",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=False
    )
    
    # Calculer g-2 avec l'approche canonique V36.1
    result_v361 = framework.calculate_anomalous_magnetic_moment(
        particle_name="muon",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=True
    )
    
    print("\nComparaison pour le muon:")
    print(f"Standard E-QFT : {result_standard['a_nf']:.6e}, σ = {result_standard['discrepancy_sigma']:.2f}")
    print(f"Canonique V36  : {result_v36['a_nf']:.6e}, σ = {result_v36['discrepancy_sigma']:.2f}")
    print(f"Canonique V36.1: {result_v361['a_nf']:.6e}, σ = {result_v361['discrepancy_sigma']:.2f}")
    
    # Afficher le rapport détaillé pour V36.1
    framework.print_g2_canonical_report("muon", use_v361=True)
    
    # ===== Tests pour l'Électron =====
    print("\n=== ÉLECTRON ===")
    
    # Ajuster delta_a_e_nf pour obtenir ~0.11σ avec V36.1
    framework.set_delta_a_nf("electron", 4.0e-18)
    
    # Calculer g-2 avec l'approche canonique V36
    result_e_v36 = framework.calculate_anomalous_magnetic_moment(
        particle_name="electron",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=False
    )
    
    # Calculer g-2 avec l'approche canonique V36.1
    result_e_v361 = framework.calculate_anomalous_magnetic_moment(
        particle_name="electron",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=True
    )
    
    print("\nComparaison pour l'électron:")
    print(f"Canonique V36  : {result_e_v36['a_nf']:.6e}, σ = {result_e_v36['discrepancy_sigma']:.2f}")
    print(f"Canonique V36.1: {result_e_v361['a_nf']:.6e}, σ = {result_e_v361['discrepancy_sigma']:.2f}")
    
    # Afficher le rapport détaillé pour V36.1
    framework.print_g2_canonical_report("electron", use_v361=True)
    
    # ===== Tests pour le Tau =====
    print("\n=== TAU ===")
    
    # Calculer g-2 avec l'approche canonique V36
    result_tau_v36 = framework.calculate_anomalous_magnetic_moment(
        particle_name="tau",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=False
    )
    
    # Calculer g-2 avec l'approche canonique V36.1
    result_tau_v361 = framework.calculate_anomalous_magnetic_moment(
        particle_name="tau",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=True
    )
    
    print("\nComparaison pour le tau:")
    print(f"Canonique V36  : {result_tau_v36['a_nf']:.6e}")
    print(f"Canonique V36.1: {result_tau_v361['a_nf']:.6e}")
    print(f"Ratio V36.1/V36: {result_tau_v361['a_nf']/result_tau_v36['a_nf']:.4f}")
    
    # Afficher le rapport détaillé pour V36.1
    framework.print_g2_canonical_report("tau", use_v361=True)
    
    # Rapport de validation des valeurs cibles
    print("\n=== VALIDATION DES VALEURS CIBLES ===")
    
    # Vérification pour le muon
    c2_mu_tau_v36 = result_v36['canonical_info']['c2']
    c2_mu_tau_v361 = result_v361['canonical_info']['c2']
    
    omega_mu = result_v361['canonical_info']['omega']
    omega_theoretical = 1.0 - 4.32/(4.0*np.pi)
    
    target_c2_v361 = 2.0 * 4.32 * 10.53 * (1.0 - 4.32/(4.0*np.pi))
    
    print("\nMuon - Vérification des valeurs:")
    print(f"c₂(μ,τ) V36     : {c2_mu_tau_v36:.2f} (attendu: ~90.98)")
    print(f"Ω(μ)            : {omega_mu:.6f} (théorique: {omega_theoretical:.6f})")
    print(f"c₂(μ,τ) V36.1   : {c2_mu_tau_v361:.2f} (attendu: ~75.29)")
    print(f"Valeur cible    : {target_c2_v361:.2f}")
    
    # Vérification pour l'électron
    c2_e_mu_v36 = result_e_v36['canonical_info']['c2']
    c2_e_mu_v361 = result_e_v361['canonical_info']['c2']
    
    omega_e = result_e_v361['canonical_info']['omega']
    omega_e_theoretical = 1.0 - 2.17/(4.0*np.pi)
    
    target_c2_e_v361 = 2.0 * 2.17 * 4.32 * (1.0 - 2.17/(4.0*np.pi))
    
    print("\nÉlectron - Vérification des valeurs:")
    print(f"c₂(e,μ) V36     : {c2_e_mu_v36:.2f} (attendu: ~18.75)")
    print(f"Ω(e)            : {omega_e:.6f} (théorique: {omega_e_theoretical:.6f})")
    print(f"c₂(e,μ) V36.1   : {c2_e_mu_v361:.2f} (attendu: ~15.50)")
    print(f"Valeur cible    : {target_c2_e_v361:.2f}")
    
    # Vérification optionnelle pour c₂(e,τ)
    c2_e_tau = 2.0 * 2.17 * 10.53 * (1.0 - 2.17/(4.0*np.pi))
    print(f"c₂(e,τ) V36.1   : {c2_e_tau:.2f} (attendu: ~37.8)")


if __name__ == "__main__":
    main()