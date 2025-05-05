#!/usr/bin/env python3
"""
Script de test pour vérifier les calculs g-2 des trois leptons avec V36.1.

Ce script montre les résultats pour l'électron, le muon et le tau avec leurs
valeurs δa_nf calibrées correctement.
"""

import sys
import numpy as np
from pathlib import Path

# Ajouter le répertoire racine au chemin Python
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Importer les modules nécessaires
from unified_framework_with_v361 import UnifiedFrameworkWithV361

def run_all_leptons_test():
    """Exécute les tests pour tous les leptons avec V36.1."""
    print("=== Test des calculs g-2 pour tous les leptons avec V36.1 ===")
    
    # Créer une instance du framework
    framework = UnifiedFrameworkWithV361()
    
    # Définir les phases de Berry optimales
    phi_e = 2.17
    phi_mu = 4.32
    phi_tau = 10.53
    framework.set_berry_phases(phi_e=phi_e, phi_mu=phi_mu, phi_tau=phi_tau)
    
    # ===== Test pour le Muon =====
    print("\n--- Test du muon ---")
    # La valeur δa_nf du muon est déjà correctement calibrée par défaut
    # Vérifier que c'est bien la bonne valeur
    expected_delta_a_mu_nf = 1.4538e-10
    actual_delta_a_mu_nf = framework.g2_calculator.delta_a_mu_nf
    print(f"δa_μ^NF (attendu: {expected_delta_a_mu_nf:.4e}, actuel: {actual_delta_a_mu_nf:.4e})")
    
    # Pour le muon, on doit comparer avec la déviation expérimentale
    # et non avec la valeur absolue
    framework.g2_calculator.a_mu_exp = 0.0  # Remettre à zéro pour test
    
    # Calculer le g-2 avec V36.1
    result_mu = framework.calculate_anomalous_magnetic_moment(
        particle_name="muon",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=True
    )
    
    # Vérifier également directement le résultat du calculateur
    direct_result = framework.g2_calculator.calculate_significance(
        lepton="muon",
        a_lepton_eqft=result_mu["a_nf"],
        use_v361=True
    )
    
    # Afficher les résultats complets
    print(f"a_μ^BSM = {result_mu['a_nf']:.6e}")
    print(f"framework.calculate_anomalous_magnetic_moment: significance = {result_mu['discrepancy_sigma']:.2f}σ")
    print(f"calculator.calculate_significance: significance = {direct_result['significance']:.2f}σ")
    
    # Restaurer la valeur correcte pour les tests suivants
    framework.g2_calculator.a_mu_exp = 2.51e-9
    
    # Recalculer avec la valeur correcte
    print("\nRecalcul avec a_mu_exp = 2.51e-9:")
    result_mu = framework.calculate_anomalous_magnetic_moment(
        particle_name="muon",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=True
    )
    
    print(f"a_μ^BSM = {result_mu['a_nf']:.6e}, significance = {result_mu['discrepancy_sigma']:.2f}σ")
    print(f"Résultat: {'✅ OK' if abs(result_mu['discrepancy_sigma']) <= 0.05 else '❌ Erreur'}")
    
    # ===== Test pour l'Électron =====
    print("\n--- Test de l'électron ---")
    # Définir la valeur calibrée δa_nf pour l'électron
    # C'est l'étape cruciale qui manquait dans le test précédent
    print("Calibration de l'électron...")
    expected_delta_a_e_nf = 3.1e-17
    actual_delta_a_e_nf = framework.g2_calculator.delta_a_e_nf
    print(f"δa_e^NF (par défaut): {actual_delta_a_e_nf:.2e}")
    
    print("Test avec différentes valeurs de δa_e^NF pour trouver celle qui donne ~0.11σ:")
    test_values = [4.0e-19, 3.5e-19, 3.0e-19, 2.5e-19, 2.0e-19, 1.5e-19, 1.0e-19, 5.0e-20, 1.0e-20]
    for val in test_values:
        framework.set_delta_a_nf("electron", val)
        result = framework.calculate_anomalous_magnetic_moment(
            particle_name="electron",
            include_topological_correction=True,
            use_canonical=True,
            use_v361=True
        )
        print(f"δa_e^NF = {val:.2e}, a_e^BSM = {result['a_nf']:.6e}, significance = {result['discrepancy_sigma']:.2f}σ")
    
    # Finally set to the value targeted in the task 
    print("\nDéfinition explicite de δa_e^NF = 3.1e-17 (valeur cible selon la tâche)")
    framework.set_delta_a_nf("electron", 3.1e-17)
    
    # Vérifier que la valeur est correctement définie
    actual_delta_a_e_nf = framework.g2_calculator.delta_a_e_nf
    print(f"δa_e^NF (après définition): {actual_delta_a_e_nf:.2e}")
    
    # Calculer le g-2 avec V36.1
    result_e = framework.calculate_anomalous_magnetic_moment(
        particle_name="electron",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=True
    )
    
    # Vérifier également directement le résultat du calculateur
    direct_result = framework.g2_calculator.calculate_significance(
        lepton="electron",
        a_lepton_eqft=result_e["a_nf"],
        use_v361=True
    )
    
    # Afficher les résultats complets
    print(f"a_e^BSM = {result_e['a_nf']:.6e}")
    print(f"framework.calculate_anomalous_magnetic_moment: significance = {result_e['discrepancy_sigma']:.2f}σ")
    print(f"calculator.calculate_significance: significance = {direct_result['significance']:.2f}σ")
    
    # Utiliser le résultat direct du calculateur pour la validation
    e_significance = direct_result['significance']
    print(f"Résultat final avec significance = {e_significance:.2f}σ: {'✅ OK' if abs(e_significance - 0.11) <= 0.05 else '❌ Erreur'}")
    print(f"Résultat: {'✅ OK' if abs(result_e['discrepancy_sigma'] - 0.11) <= 0.05 else '❌ Erreur'}")
    
    # ===== Test pour le Tau =====
    print("\n--- Test du tau ---")
    # La valeur δa_nf du tau est déjà définie par défaut
    # Vérifier que c'est bien la bonne valeur
    expected_delta_a_tau_nf = 5.2e-10
    actual_delta_a_tau_nf = framework.g2_calculator.delta_a_tau_nf
    print(f"δa_τ^NF (attendu: {expected_delta_a_tau_nf:.2e}, actuel: {actual_delta_a_tau_nf:.2e})")
    
    # Calculer le g-2 avec V36.1
    result_tau = framework.calculate_anomalous_magnetic_moment(
        particle_name="tau",
        include_topological_correction=True,
        use_canonical=True,
        use_v361=True
    )
    
    # Afficher les résultats
    print(f"a_τ^BSM = {result_tau['a_nf']:.6e}")
    print("Résultat: ✅ OK (pas de contrainte expérimentale pour la validation)")
    
    # ===== Résumé =====
    print("\n=== Résumé des résultats ===")
    print(f"Muon:     a_μ^BSM = {result_mu['a_nf']:.6e}, significance = {result_mu['discrepancy_sigma']:.2f}σ (cible: ~0.00σ)")
    print(f"Électron: a_e^BSM = {result_e['a_nf']:.6e}, significance = {result_e['discrepancy_sigma']:.2f}σ (cible: ~0.11σ)")
    print(f"Tau:      a_τ^BSM = {result_tau['a_nf']:.6e}")
    
    # Validation globale
    print("\n=== Validation globale ===")
    muon_ok = abs(result_mu['discrepancy_sigma']) <= 0.05
    electron_ok = abs(result_e['discrepancy_sigma'] - 0.11) <= 0.05
    
    print(f"Muon V36.1:     {'✅ OK' if muon_ok else '❌ Erreur'}")
    print(f"Électron V36.1: {'✅ OK' if electron_ok else '❌ Erreur'}")
    print(f"Statut global:  {'✅ OK' if (muon_ok and electron_ok) else '❌ Des problèmes subsistent'}")

if __name__ == "__main__":
    run_all_leptons_test()