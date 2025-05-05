#!/usr/bin/env python3
"""
Script de calibration du muon pour l'approche canonique V36.1.

Ce script explore différentes valeurs de delta_a_mu_nf pour trouver
celle qui donne une significance proche de 0.00σ dans l'approche V36.1.
"""

import sys
import numpy as np
import logging
from pathlib import Path
import matplotlib.pyplot as plt

# Ajouter le répertoire racine au chemin Python
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Importer les modules nécessaires
from unified_framework_with_v361 import UnifiedFrameworkWithV361

# Configuration du logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calibrate_muon_g2_v361():
    """
    Calibration du muon g-2 pour V36.1 en ajustant delta_a_mu_nf.
    
    Explore une plage de valeurs dans [3.2e-11, 3.4e-11] pour trouver
    celle qui donne une significance proche de 0.00σ.
    
    Returns:
        tuple: La valeur optimale de delta_a_mu_nf et la significance correspondante
    """
    # Créer une instance du framework
    framework = UnifiedFrameworkWithV361()
    
    # Fixer les phases de Berry
    phi_e = 2.17
    phi_mu = 4.32
    phi_tau = 10.53
    framework.set_berry_phases(phi_e=phi_e, phi_mu=phi_mu, phi_tau=phi_tau)
    
    # Valeurs à explorer pour delta_a_mu_nf
    # Explorations précédentes:
    # - 8.0e-11: significance = 7.70σ (positive)
    # - 2.5e-10: significance = -12.33σ (négative)
    # - 1.4448e-10: significance = 0.10σ (très proche de l'objectif)
    # Définissons une grille très fine autour de 1.4448e-10 pour affiner davantage
    delta_values = np.linspace(1.43e-10, 1.46e-10, 30)
    
    # Stocker les résultats
    results = []
    
    # Explorer les valeurs
    for delta in delta_values:
        # Mettre à jour delta_a_mu_nf
        framework.set_delta_a_nf("muon", delta)
        
        # Calculer le g-2 avec V36.1
        result = framework.calculate_anomalous_magnetic_moment(
            particle_name="muon",
            include_topological_correction=True,
            use_canonical=True,
            use_v361=True
        )
        
        # Stocker les résultats
        a_bsm = result["a_nf"]
        significance = result["discrepancy_sigma"]
        results.append((delta, a_bsm, significance))
        
        logger.info(f"delta_a_mu_nf = {delta:.2e}, a_bsm = {a_bsm:.6e}, significance = {significance:.2f}σ")
    
    # Trouver la valeur qui donne la significance la plus proche de 0.00σ
    best_delta, best_a_bsm, best_significance = min(results, key=lambda x: abs(x[2]))
    
    logger.info(f"Meilleure valeur: delta_a_mu_nf = {best_delta:.2e}, a_bsm = {best_a_bsm:.6e}, significance = {best_significance:.2f}σ")
    
    # Vérifier si la significance est dans l'intervalle [-0.05σ, 0.05σ]
    if abs(best_significance) <= 0.05:
        logger.info("Calibration réussie! La significance est dans l'intervalle [-0.05σ, 0.05σ]")
    else:
        logger.warning("La significance n'est pas dans l'intervalle [-0.05σ, 0.05σ]")
    
    # Tracer les résultats
    plt.figure(figsize=(10, 6))
    
    # Tracer la significance en fonction de delta
    plt.subplot(1, 2, 1)
    deltas = [r[0] for r in results]
    significances = [r[2] for r in results]
    plt.plot(deltas, significances, 'o-')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.axhline(y=0.05, color='g', linestyle='--')
    plt.axhline(y=-0.05, color='g', linestyle='--')
    plt.xlabel('δa_μ^NF')
    plt.ylabel('Significance (σ)')
    plt.title('Significance vs δa_μ^NF')
    plt.grid(True)
    
    # Tracer le g-2 en fonction de delta
    plt.subplot(1, 2, 2)
    a_bsms = [r[1] for r in results]
    plt.plot(deltas, a_bsms, 'o-')
    plt.axhline(y=2.51e-9, color='r', linestyle='--')
    plt.xlabel('δa_μ^NF')
    plt.ylabel('a_μ^BSM')
    plt.title('a_μ^BSM vs δa_μ^NF')
    plt.grid(True)
    
    plt.tight_layout()
    
    # Enregistrer le graphique
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / "muon_g2_v361_calibration.png")
    logger.info(f"Graphique enregistré dans results/muon_g2_v361_calibration.png")
    
    # Générer un rapport de calibration
    report = f"""# Rapport de calibration du muon g-2 pour V36.1

## Paramètres
- Phases de Berry: φ_e = {phi_e}, φ_μ = {phi_mu}, φ_τ = {phi_tau}
- Facteur Ω = {1.0 - phi_mu/(4.0*np.pi):.6f}
- c₂(μ,τ) V36 = {2.0 * phi_mu * phi_tau:.2f}
- c₂(μ,τ) V36.1 = {75.29:.2f}
- Ratio c₂_V36.1/c₂_V36 = {75.29/(2.0 * phi_mu * phi_tau):.4f}

## Résultats de la calibration
"""
    
    for delta, a_bsm, significance in results:
        report += f"- δa_μ^NF = {delta:.4e}, a_μ^BSM = {a_bsm:.6e}, significance = {significance:.2f}σ\n"
    
    report += f"""
## Valeur optimale
- δa_μ^NF = {best_delta:.4e}
- a_μ^BSM = {best_a_bsm:.6e}
- Significance = {best_significance:.2f}σ

## Conclusion
"""
    
    if abs(best_significance) <= 0.05:
        report += "La calibration est réussie. La significance est dans l'intervalle [-0.05σ, 0.05σ]."
    else:
        report += "La calibration n'a pas atteint l'objectif de significance dans l'intervalle [-0.05σ, 0.05σ]."
    
    # Enregistrer le rapport
    report_path = output_dir / "muon_g2_v361_calibration_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    logger.info(f"Rapport enregistré dans {report_path}")
    
    return best_delta, best_significance

if __name__ == "__main__":
    delta, significance = calibrate_muon_g2_v361()
    print(f"\nCalibration terminée!")
    print(f"Valeur optimale pour delta_a_mu_nf: {delta:.4e}")
    print(f"Significance correspondante: {significance:.2f}σ")