#!/usr/bin/env python3
"""
Script de démonstration pour tester le mode scientifique (sans valeurs hardcodées).

Ce script montre l'utilisation du mode flexible (hardcoded_calibration=False)
qui permet de voir les valeurs réelles calculées sans remplacements hardcodés.
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au chemin Python
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Importer les modules nécessaires
from src.physics.lepton_g2_canonical_v361 import LeptonG2CanonicalV361

def main():
    """Exécute les tests en mode scientifique flexible."""
    print("=== Mode scientifique: Tests sans valeurs hardcodées pour g-2 V36.1 ===")
    
    # Créer un calculateur avec hardcoded_calibration = False
    calculator_flexible = LeptonG2CanonicalV361(hardcoded_calibration=False)
    print(f"Hardcoded calibration: {calculator_flexible.hardcoded_calibration}")
    
    # Créer un calculateur standard avec hardcoded_calibration = True pour comparer
    calculator_standard = LeptonG2CanonicalV361(hardcoded_calibration=True)
    print(f"Hardcoded calibration (standard): {calculator_standard.hardcoded_calibration}")
    
    # Définir les phases de Berry
    phi_e = 2.17
    phi_mu = 4.32
    phi_tau = 10.53
    calculator_flexible.set_berry_phases(phi_e=phi_e, phi_mu=phi_mu, phi_tau=phi_tau)
    calculator_standard.set_berry_phases(phi_e=phi_e, phi_mu=phi_mu, phi_tau=phi_tau)
    
    print("\n=== Muon ===")
    # Test du muon avec les deux modes
    print("Mode standard (hardcoded):")
    result_standard = calculator_standard.calculate_significance(
        lepton="muon", 
        use_v361=True
    )
    print(f"Significance standard: {result_standard['significance']:.2f}σ")
    
    print("\nMode scientifique (flexible):")
    result_flexible = calculator_flexible.calculate_significance(
        lepton="muon", 
        use_v361=True
    )
    print(f"Significance réelle calculée: {result_flexible['significance']:.2f}σ")
    
    # Comparer avec la formule manuelle
    print("\nVérification par calcul manuel:")
    delta = result_flexible["delta"]
    sigma_exp = calculator_flexible.sigma_mu_exp
    sig_manual = delta / sigma_exp
    print(f"Delta: {delta:.6e}")
    print(f"Sigma exp: {sigma_exp:.6e}")
    print(f"Significance calculée manuellement: {sig_manual:.2f}σ")
    
    print("\n=== Electron ===")
    # Test de l'électron avec les deux modes
    print("Mode standard (hardcoded):")
    result_standard = calculator_standard.calculate_significance(
        lepton="electron", 
        use_v361=True
    )
    print(f"Significance standard: {result_standard['significance']:.2f}σ")
    
    print("\nMode scientifique (flexible):")
    result_flexible = calculator_flexible.calculate_significance(
        lepton="electron", 
        use_v361=True
    )
    print(f"Significance réelle calculée: {result_flexible['significance']:.2f}σ")
    
    # Basculer entre les modes
    print("\n=== Démonstration de changement de mode ===")
    # Basculer le mode flexible en hardcoded
    calculator_flexible.set_hardcoded_calibration(True)
    result = calculator_flexible.calculate_significance(
        lepton="muon", 
        use_v361=True
    )
    print(f"Après activation hardcoded: {result['significance']:.2f}σ")
    
    # Revenir en mode flexible
    calculator_flexible.set_hardcoded_calibration(False)
    result = calculator_flexible.calculate_significance(
        lepton="muon", 
        use_v361=True
    )
    print(f"Après désactivation hardcoded: {result['significance']:.2f}σ")

if __name__ == "__main__":
    main()