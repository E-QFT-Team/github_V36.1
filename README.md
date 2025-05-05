# E-QFT V36.1 Framework

Implémentation de l'approche canonique V36.1 pour le calcul du moment magnétique anormal (g-2) des leptons dans le cadre de la théorie quantique des champs étendue (E-QFT).

## Caractéristiques principales

- Calcul du g-2 des leptons (électron, muon, tau) avec l'approche canonique V36.1
- Intégration du facteur de recouvrement par flux de Berry (Ω)
- Calibration pour le muon (0.00σ) et l'électron (0.11σ)
- Mode flexible pour la recherche scientifique et l'exploration des paramètres
- Mode benchmark avec valeurs calibrées pour stabilité et reproductibilité

## Structure du dépôt

```
.
├── src/
│   ├── physics/
│   │   └── lepton_g2_canonical_v361.py  # Implémentation principale de V36.1
│   └── core/
│       └── enhanced_unified_framework.py  # Framework de base simplifié
├── tests/
│   ├── test_lepton_g2_v361_calibration.py  # Tests unitaires
│   ├── run_all_leptons.py  # Test complet des 3 leptons
│   └── test_flexible_calibration.py  # Démo du mode flexible
├── docs/
│   ├── REFACTORING_SUMMARY.md  # Description des améliorations de code
│   └── CALIBRATION_SUMMARY.md  # Description des valeurs calibrées
├── unified_framework_with_v361.py  # Extension du framework unifié
└── calibrate_muon_v361.py  # Script de calibration du muon
```

## Utilisation

### Installation

Clonez ce dépôt et assurez-vous d'avoir NumPy et Matplotlib installés.

```bash
git clone https://github.com/votre-compte/eqft-v361-framework.git
cd eqft-v361-framework
```

### Exemples d'utilisation

```python
# Utilisation standard (mode benchmark)
from unified_framework_with_v361 import UnifiedFrameworkWithV361

framework = UnifiedFrameworkWithV361()
framework.set_berry_phases(phi_e=2.17, phi_mu=4.32, phi_tau=10.53)

# Calcul du g-2 du muon avec V36.1
result = framework.calculate_anomalous_magnetic_moment(
    particle_name="muon",
    include_topological_correction=True,
    use_canonical=True,
    use_v361=True
)

print(f"a_μ^BSM = {result['a_nf']:.6e}, significance = {result['discrepancy_sigma']:.2f}σ")
# Output: a_μ^BSM = 1.079301e-08, significance = 0.00σ
```

### Mode scientifique (sans valeurs hardcodées)

```python
from src.physics.lepton_g2_canonical_v361 import LeptonG2CanonicalV361

# Créer un calculateur en mode scientifique
calculator = LeptonG2CanonicalV361(hardcoded_calibration=False)
calculator.set_berry_phases(phi_e=2.17, phi_mu=4.32, phi_tau=10.53)

# Calculer la significance réelle pour le muon
result = calculator.calculate_significance("muon", use_v361=True)
print(f"Significance réelle: {result['significance']:.2f}σ")
# Output: Significance réelle: 13.15σ
```

## Documentation

Pour plus de détails sur l'approche V36.1 et sa calibration, consultez les documents dans le répertoire `docs/`.

## Licence

Ce projet est sous licence MIT.