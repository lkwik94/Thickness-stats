#!/usr/bin/env python3
"""
Refactored Thickness Analysis Script

This script consolidates the repetitive analysis code from the original notebook
into reusable functions that can analyze multiple CSV columns efficiently.

Author: OpenHands AI Assistant
Date: 2025-08-13
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import os
from typing import Tuple, Dict, List, Any

warnings.filterwarnings('ignore')

# Configuration des graphiques
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def extract_thickness_data(file_path: str, column_index: int, min_columns: int = 2, 
                          is_percentage: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extrait les données de temps et d'épaisseur/pourcentage d'un fichier CSV
    
    Args:
        file_path: Chemin vers le fichier CSV
        column_index: Index de la colonne à extraire (-1 pour la dernière)
        min_columns: Nombre minimum de colonnes requis
        is_percentage: True si c'est un pourcentage (pour le nom des variables)
    
    Returns:
        Tuple contenant (times, values) - arrays numpy des temps et valeurs
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Trouve le début des données (après les lignes %)
    data_start = 0
    for i, line in enumerate(lines):
        if not line.startswith('%') and line.strip():
            data_start = i
            break
    
    times = []
    values = []
    
    for line in lines[data_start:]:
        if line.strip():
            row_values = [x.strip() for x in line.split(',') if x.strip()]
            if len(row_values) >= min_columns:
                try:
                    time_val = float(row_values[0]) / 60  # Temps en minutes
                    data_val = float(row_values[column_index])
                    times.append(time_val)
                    values.append(data_val)
                except ValueError:
                    continue
    
    return np.array(times), np.array(values)


def calculate_statistics(data_avant: np.ndarray, data_apres: np.ndarray, 
                        is_percentage: bool = False) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Calcule les statistiques comparatives pour deux jeux de données
    
    Args:
        data_avant: Données avant optimisation
        data_apres: Données après optimisation
        is_percentage: True si les données sont des pourcentages
    
    Returns:
        Tuple contenant (stats_avant, stats_apres) - dictionnaires des statistiques
    """
    stats_avant = {
        'Moyenne': np.mean(data_avant),
        'Médiane': np.median(data_avant), 
        'Écart-type': np.std(data_avant),
        'Minimum': np.min(data_avant),
        'Maximum': np.max(data_avant),
        'Plage': np.max(data_avant) - np.min(data_avant)
    }
    
    stats_apres = {
        'Moyenne': np.mean(data_apres),
        'Médiane': np.median(data_apres),
        'Écart-type': np.std(data_apres), 
        'Minimum': np.min(data_apres),
        'Maximum': np.max(data_apres),
        'Plage': np.max(data_apres) - np.min(data_apres)
    }
    
    if is_percentage:
        stats_avant['Temps à 100%'] = np.sum(data_avant == 100) / len(data_avant) * 100
        stats_apres['Temps à 100%'] = np.sum(data_apres == 100) / len(data_apres) * 100
    else:
        stats_avant['CV (%)'] = (np.std(data_avant) / np.mean(data_avant)) * 100
        stats_apres['CV (%)'] = (np.std(data_apres) / np.mean(data_apres)) * 100
    
    return stats_avant, stats_apres


def print_statistics(stats_avant: Dict[str, float], stats_apres: Dict[str, float], 
                    title: str, is_percentage: bool = False) -> None:
    """
    Affiche les statistiques comparatives de manière formatée
    
    Args:
        stats_avant: Statistiques avant optimisation
        stats_apres: Statistiques après optimisation
        title: Titre de l'analyse
        is_percentage: True si les données sont des pourcentages
    """
    print(f"\n📊 STATISTIQUES {title}")
    separator_length = max(60, len(title) + 20)
    print("=" * separator_length)
    print(f"{'Métrique':<20} {'Avant':<12} {'Après':<12} {'Différence':<12}")
    print("-" * separator_length)
    
    for metric in stats_avant.keys():
        avant = stats_avant[metric]
        apres = stats_apres[metric]
        diff = apres - avant
        
        if metric == 'CV (%)' or metric == 'Temps à 100%':
            print(f"{metric:<20} {avant:<12.2f} {apres:<12.2f} {diff:<+12.2f}")
        elif is_percentage:
            print(f"{metric:<20} {avant:<12.1f} {apres:<12.1f} {diff:<+12.1f}")
        else:
            print(f"{metric:<20} {avant:<12.3f} {apres:<12.3f} {diff:<+12.3f}")


def create_comparative_plots(times_avant: np.ndarray, data_avant: np.ndarray, 
                           times_apres: np.ndarray, data_apres: np.ndarray, 
                           title: str, ylabel: str, is_percentage: bool = False) -> None:
    """
    Crée les graphiques comparatifs pour deux jeux de données
    
    Args:
        times_avant: Temps avant optimisation
        data_avant: Données avant optimisation
        times_apres: Temps après optimisation
        data_apres: Données après optimisation
        title: Titre principal des graphiques
        ylabel: Label de l'axe Y
        is_percentage: True si les données sont des pourcentages
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
    
    # 1. Évolution temporelle
    ax1.plot(times_avant, data_avant, 'r-', label='Avant optimisation', linewidth=1.5, alpha=0.8)
    ax1.plot(times_apres, data_apres, 'g-', label='Après optimisation', linewidth=1.5, alpha=0.8)
    
    if is_percentage:
        ax1.axhline(y=100, color='blue', linestyle='--', alpha=0.6, label='Optimal (100%)')
        ax1.axhline(y=75, color='red', linestyle='--', alpha=0.6, label='Critical (75%)')
        ax1.set_ylim(0, 105)
    
    ax1.set_title(f'Évolution {title}', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Temps (minutes)')
    ax1.set_ylabel(ylabel)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Histogrammes comparatifs
    if is_percentage:
        bins = np.linspace(0, 100, 21)
    else:
        bins = 30
    
    ax2.hist(data_avant, bins=bins, alpha=0.6, color='red', label='Avant', density=True)
    ax2.hist(data_apres, bins=bins, alpha=0.6, color='green', label='Après', density=True)
    ax2.axvline(np.mean(data_avant), color='red', linestyle='--', linewidth=2)
    ax2.axvline(np.mean(data_apres), color='green', linestyle='--', linewidth=2)
    ax2.set_title(f'Distribution {title}', fontweight='bold', fontsize=12)
    ax2.set_xlabel(ylabel)
    ax2.set_ylabel('Densité')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Box plots
    box_data = [data_avant, data_apres]
    bp = ax3.boxplot(box_data, labels=['Avant', 'Après'], patch_artist=True, showmeans=True)
    bp['boxes'][0].set_facecolor('red')
    bp['boxes'][1].set_facecolor('green')
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_alpha(0.7)
    ax3.set_title(f'Box Plot {title}', fontweight='bold', fontsize=12)
    ax3.set_ylabel(ylabel)
    ax3.grid(True, alpha=0.3)
    
    # 4. Graphique de corrélation/dispersion
    if len(data_avant) == len(data_apres):
        ax4.scatter(data_avant, data_apres, alpha=0.6, s=20)
        # Ligne de référence y=x
        min_val = min(np.min(data_avant), np.min(data_apres))
        max_val = max(np.max(data_avant), np.max(data_apres))
        ax4.plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.8, label='y=x')
        ax4.set_xlabel('Avant optimisation')
        ax4.set_ylabel('Après optimisation')
        ax4.set_title('Corrélation Avant vs Après', fontweight='bold', fontsize=12)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
    else:
        # Si les longueurs sont différentes, afficher un graphique de moyennes mobiles
        window = min(100, len(data_avant) // 10)
        if window > 1:
            rolling_avant = np.convolve(data_avant, np.ones(window)/window, mode='valid')
            rolling_apres = np.convolve(data_apres, np.ones(window)/window, mode='valid')
            ax4.plot(rolling_avant, 'r-', label=f'Moyenne mobile Avant (fenêtre={window})', alpha=0.8)
            ax4.plot(rolling_apres, 'g-', label=f'Moyenne mobile Après (fenêtre={window})', alpha=0.8)
        else:
            ax4.axhline(np.mean(data_avant), color='red', label='Moyenne Avant', linewidth=2)
            ax4.axhline(np.mean(data_apres), color='green', label='Moyenne Après', linewidth=2)
        
        ax4.set_title('Moyennes mobiles', fontweight='bold', fontsize=12)
        ax4.set_xlabel('Index')
        ax4.set_ylabel(ylabel)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
    
    plt.suptitle(f'ANALYSE COMPARATIVE - {title}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def analyze_thickness_data(csv_file_1: str, csv_file_2: str, column_index: int, 
                          min_columns: int, title: str, ylabel: str, 
                          is_percentage: bool = False) -> Dict[str, Any]:
    """
    Fonction principale pour analyser les données d'épaisseur/pourcentage
    
    Args:
        csv_file_1: Chemin vers le premier fichier CSV
        csv_file_2: Chemin vers le deuxième fichier CSV
        column_index: Index de la colonne à analyser (-1 pour la dernière)
        min_columns: Nombre minimum de colonnes requis
        title: Titre de l'analyse
        ylabel: Label de l'axe Y pour les graphiques
        is_percentage: True si les données sont des pourcentages
    
    Returns:
        Dictionnaire contenant les résultats de l'analyse
    """
    print(f"\n📂 Chargement des données {title}...")
    
    # Extraction des données
    times_avant, data_avant = extract_thickness_data(csv_file_1, column_index, min_columns, is_percentage)
    times_apres, data_apres = extract_thickness_data(csv_file_2, column_index, min_columns, is_percentage)
    
    print(f"✅ Avant: {len(data_avant)} points sur {times_avant.max():.1f} min")
    print(f"✅ Après: {len(data_apres)} points sur {times_apres.max():.1f} min")
    
    # Calcul des statistiques
    stats_avant, stats_apres = calculate_statistics(data_avant, data_apres, is_percentage)
    
    # Affichage des statistiques
    print_statistics(stats_avant, stats_apres, title, is_percentage)
    
    # Création des graphiques
    print(f"\n📈 Création des graphiques pour {title}...")
    create_comparative_plots(times_avant, data_avant, times_apres, data_apres, title, ylabel, is_percentage)
    
    return {
        'title': title,
        'stats_avant': stats_avant,
        'stats_apres': stats_apres,
        'data_avant': data_avant,
        'data_apres': data_apres,
        'times_avant': times_avant,
        'times_apres': times_apres
    }


def create_summary_analysis(csv_file_1: str, csv_file_2: str, analyses_config: List[Dict]) -> List[Dict]:
    """
    Crée une analyse résumée de toutes les métriques
    
    Args:
        csv_file_1: Chemin vers le premier fichier CSV
        csv_file_2: Chemin vers le deuxième fichier CSV
        analyses_config: Configuration des analyses à effectuer
    
    Returns:
        Liste des résultats résumés
    """
    print("\n📊 RÉSUMÉ COMPARATIF DE TOUTES LES MÉTRIQUES")
    print("=" * 80)
    
    summary_data = []
    
    for config in analyses_config:
        # Extraction des données
        times_avant, data_avant = extract_thickness_data(
            csv_file_1, config['column_index'], config['min_columns'], config['is_percentage']
        )
        times_apres, data_apres = extract_thickness_data(
            csv_file_2, config['column_index'], config['min_columns'], config['is_percentage']
        )
        
        # Calcul des statistiques
        stats_avant, stats_apres = calculate_statistics(data_avant, data_apres, config['is_percentage'])
        
        # Détermination de l'amélioration
        if config['is_percentage']:
            improvement = 'Amélioration' if stats_apres['Moyenne'] > stats_avant['Moyenne'] else 'Dégradation'
        else:
            improvement = 'Amélioration' if stats_apres['Écart-type'] < stats_avant['Écart-type'] else 'Dégradation'
        
        # Stockage des résultats
        summary_data.append({
            'metric': config['title'],
            'mean_before': stats_avant['Moyenne'],
            'mean_after': stats_apres['Moyenne'],
            'mean_diff': stats_apres['Moyenne'] - stats_avant['Moyenne'],
            'std_before': stats_avant['Écart-type'],
            'std_after': stats_apres['Écart-type'],
            'std_diff': stats_apres['Écart-type'] - stats_avant['Écart-type'],
            'improvement': improvement
        })
    
    # Affichage du tableau résumé
    print(f"{'Métrique':<35} {'Moy. Avant':<12} {'Moy. Après':<12} {'Δ Moyenne':<12} {'Évolution':<12}")
    print("-" * 80)
    
    for data in summary_data:
        print(f"{data['metric']:<35} {data['mean_before']:<12.2f} {data['mean_after']:<12.2f} "
              f"{data['mean_diff']:<+12.2f} {data['improvement']:<12}")
    
    # Graphique résumé
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Graphique des moyennes
    metrics = [data['metric'].replace('TRSF_ThicknessBottles', 'Capteur').replace('[', '').replace(']', '') for data in summary_data]
    means_before = [data['mean_before'] for data in summary_data]
    means_after = [data['mean_after'] for data in summary_data]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    ax1.bar(x - width/2, means_before, width, label='Avant', color='red', alpha=0.7)
    ax1.bar(x + width/2, means_after, width, label='Après', color='green', alpha=0.7)
    ax1.set_xlabel('Métriques')
    ax1.set_ylabel('Valeurs moyennes')
    ax1.set_title('Comparaison des moyennes par métrique')
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Graphique des écarts-types
    stds_before = [data['std_before'] for data in summary_data]
    stds_after = [data['std_after'] for data in summary_data]
    
    ax2.bar(x - width/2, stds_before, width, label='Avant', color='red', alpha=0.7)
    ax2.bar(x + width/2, stds_after, width, label='Après', color='green', alpha=0.7)
    ax2.set_xlabel('Métriques')
    ax2.set_ylabel('Écarts-types')
    ax2.set_title('Comparaison de la variabilité par métrique')
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return summary_data


def main():
    """
    Fonction principale pour exécuter toutes les analyses
    """
    # Configuration des fichiers
    csv_file_1 = './CSV/2-apres/thickness_ENG.csv'
    csv_file_2 = './CSV/10-restart apres modif recette a la main/thickness.csv'
    
    print("🚀 ANALYSE COMPARATIVE DES DONNÉES D'ÉPAISSEUR")
    print("=" * 80)
    print(f"📁 Fichier 1 (avant): {csv_file_1}")
    print(f"📁 Fichier 2 (après): {csv_file_2}")
    
    # Vérification que les fichiers existent
    if not os.path.exists(csv_file_1):
        print(f"❌ {csv_file_1} non trouvé")
        return
    if not os.path.exists(csv_file_2):
        print(f"❌ {csv_file_2} non trouvé")
        return
    
    print("✅ Tous les fichiers sont disponibles")
    
    # Configuration des analyses à effectuer
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
    
    # Exécution de toutes les analyses
    print("\n🔍 Début de l'analyse comparative des 4 métriques...")
    print("=" * 80)
    
    results = []
    for i, config in enumerate(analyses_config, 1):
        print(f"\n🔍 ANALYSE {i}/4: {config['title']}")
        print("=" * 80)
        
        result = analyze_thickness_data(
            csv_file_1=csv_file_1,
            csv_file_2=csv_file_2,
            column_index=config['column_index'],
            min_columns=config['min_columns'],
            title=config['title'],
            ylabel=config['ylabel'],
            is_percentage=config['is_percentage']
        )
        
        results.append(result)
        print(f"\n✅ Analyse {i}/4 terminée")
        print("-" * 80)
    
    # Analyse résumée
    summary_results = create_summary_analysis(csv_file_1, csv_file_2, analyses_config)
    
    print("\n🎉 Toutes les analyses sont terminées!")
    print("=" * 80)
    
    return results, summary_results


if __name__ == "__main__":
    results, summary = main()