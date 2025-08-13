#!/usr/bin/env python3
"""
Demonstration of the refactored thickness analysis

This script shows how the refactored code eliminates repetition
and provides a clean, maintainable solution.
"""

import os
import sys
from thickness_analysis import analyze_thickness_data, create_summary_analysis

def demo_single_analysis():
    """
    Demonstrates how to run a single analysis with the refactored code
    """
    print("🔍 DÉMONSTRATION - ANALYSE UNIQUE")
    print("=" * 50)
    
    # Configuration des fichiers
    csv_file_1 = './CSV/2-apres/thickness_ENG.csv'
    csv_file_2 = './CSV/10-restart apres modif recette a la main/thickness.csv'
    
    # Vérification des fichiers
    if not os.path.exists(csv_file_1) or not os.path.exists(csv_file_2):
        print("❌ Fichiers CSV non trouvés pour la démonstration")
        return
    
    # Analyse d'un seul capteur (exemple: Capteur 1)
    print("\n📊 Analyse du Capteur 1 uniquement:")
    result = analyze_thickness_data(
        csv_file_1=csv_file_1,
        csv_file_2=csv_file_2,
        column_index=1,  # 2ème colonne
        min_columns=2,
        title='TRSF_ThicknessBottles[1] (Capteur 1)',
        ylabel='TRSF_ThicknessBottles[1]',
        is_percentage=False
    )
    
    print(f"\n✅ Analyse terminée pour {result['title']}")
    print(f"   - Moyenne avant: {result['stats_avant']['Moyenne']:.3f}")
    print(f"   - Moyenne après: {result['stats_apres']['Moyenne']:.3f}")
    print(f"   - Différence: {result['stats_apres']['Moyenne'] - result['stats_avant']['Moyenne']:+.3f}")

def demo_multiple_analyses():
    """
    Demonstrates how to run multiple analyses efficiently
    """
    print("\n\n🔍 DÉMONSTRATION - ANALYSES MULTIPLES")
    print("=" * 50)
    
    # Configuration des fichiers
    csv_file_1 = './CSV/2-apres/thickness_ENG.csv'
    csv_file_2 = './CSV/10-restart apres modif recette a la main/thickness.csv'
    
    # Vérification des fichiers
    if not os.path.exists(csv_file_1) or not os.path.exists(csv_file_2):
        print("❌ Fichiers CSV non trouvés pour la démonstration")
        return
    
    # Configuration pour toutes les analyses
    analyses_config = [
        {
            'column_index': -1,  # Dernière colonne
            'min_columns': 12,
            'title': 'TRSF_ThicknessBottlePerc',
            'ylabel': 'Pourcentage de bouteilles lues (%)',
            'is_percentage': True
        },
        {
            'column_index': 1,  # 2ème colonne
            'min_columns': 2,
            'title': 'TRSF_ThicknessBottles[1] (Capteur 1)',
            'ylabel': 'TRSF_ThicknessBottles[1]',
            'is_percentage': False
        },
        {
            'column_index': 3,  # 4ème colonne
            'min_columns': 4,
            'title': 'TRSF_ThicknessBottles[2] (Capteur 2)',
            'ylabel': 'TRSF_ThicknessBottles[2]',
            'is_percentage': False
        },
        {
            'column_index': 5,  # 6ème colonne
            'min_columns': 6,
            'title': 'TRSF_ThicknessBottles[3] (Capteur 3)',
            'ylabel': 'TRSF_ThicknessBottles[3]',
            'is_percentage': False
        }
    ]
    
    print("📊 Exécution de toutes les analyses avec une seule boucle:")
    
    results = []
    for i, config in enumerate(analyses_config, 1):
        print(f"\n   {i}/4: {config['title']}")
        
        # Une seule fonction fait tout le travail !
        result = analyze_thickness_data(
            csv_file_1=csv_file_1,
            csv_file_2=csv_file_2,
            **config  # Unpacking de la configuration
        )
        
        results.append(result)
        print(f"   ✅ Terminé - Δ moyenne: {result['stats_apres']['Moyenne'] - result['stats_avant']['Moyenne']:+.2f}")
    
    # Analyse résumée
    print(f"\n📈 Création du résumé comparatif...")
    summary = create_summary_analysis(csv_file_1, csv_file_2, analyses_config)
    
    print(f"\n🎉 {len(results)} analyses terminées avec succès!")
    return results, summary

def show_code_comparison():
    """
    Shows the difference between old and new approach
    """
    print("\n\n📝 COMPARAISON DE CODE")
    print("=" * 50)
    
    print("❌ ANCIEN CODE (répétitif):")
    print("""
    # Pour chaque capteur, il fallait:
    def extract_thickness_sensor1(file_path):
        # ... 20+ lignes de code identique
        thickness_val = float(values[1])  # Seule différence: index
        # ... reste identique
    
    def extract_thickness_sensor2(file_path):
        # ... 20+ lignes de code identique  
        thickness_val = float(values[3])  # Seule différence: index
        # ... reste identique
    
    # + 2 autres fonctions similaires
    # + 4 blocs d'analyse identiques de 50+ lignes chacun
    # = ~400 lignes de code répétitif !
    """)
    
    print("\n✅ NOUVEAU CODE (générique):")
    print("""
    # Une seule fonction générique:
    def extract_thickness_data(file_path, column_index, min_columns):
        # ... logique réutilisable
        thickness_val = float(values[column_index])  # Paramétrable !
        # ... 
    
    def analyze_thickness_data(csv_file_1, csv_file_2, column_index, ...):
        # Une fonction qui fait tout !
        
    # Usage simple:
    for config in analyses_config:
        analyze_thickness_data(**config)
    
    # = ~200 lignes de code réutilisable + configuration
    # = 50% de réduction de code !
    """)

def main():
    """
    Main demonstration function
    """
    print("🚀 DÉMONSTRATION DU CODE REFACTORISÉ")
    print("=" * 60)
    print("Ce script montre comment le code répétitif a été éliminé")
    print("et remplacé par des fonctions génériques réutilisables.")
    print("=" * 60)
    
    # Démonstration du code
    show_code_comparison()
    
    # Démonstration d'une analyse unique
    demo_single_analysis()
    
    # Démonstration d'analyses multiples
    demo_multiple_analyses()
    
    print("\n\n🎯 AVANTAGES DU CODE REFACTORISÉ:")
    print("=" * 50)
    print("✅ Réduction de ~50% du code")
    print("✅ Élimination de la duplication")
    print("✅ Maintenance plus facile")
    print("✅ Ajout de nouvelles analyses simplifié")
    print("✅ Moins d'erreurs potentielles")
    print("✅ Code plus lisible et organisé")
    print("✅ Fonctions réutilisables")
    print("✅ Configuration centralisée")

if __name__ == "__main__":
    main()