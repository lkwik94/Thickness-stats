# Thickness Analysis Tool

A Python tool for analyzing thickness data from CSV files, comparing "before" and "after" optimization results across multiple sensors.

## 🚀 Quick Start

### Option 1: Jupyter Notebook (Recommended)
```bash
# Open the refactored notebook
jupyter notebook Analyse_traces_refactored.ipynb
```

### Option 2: Python Script
```bash
# Run the complete analysis
python thickness_analysis.py
```

## 📁 File Structure

```
├── Analyse_traces_refactored.ipynb    # Main analysis notebook (NEW)
├── thickness_analysis.py             # Standalone Python script (NEW)
├── demo_refactored_analysis.py       # Demonstration script (NEW)
├── Analyse traces.ipynb               # Original notebook (LEGACY)
└── CSV/                               # Data directory
    ├── 2-apres/
    │   └── thickness_ENG.csv          # "After" data file
    └── 10-restart apres modif recette a la main/
        └── thickness.csv              # "Before" data file
```

## ⚙️ Configuration

### Changing CSV File Paths

**In Jupyter Notebook** (`Analyse_traces_refactored.ipynb`):
```python
# Edit these paths in the notebook
csv_file_1 = './CSV/2-apres/thickness_ENG.csv'           # "Before" file
csv_file_2 = './CSV/10-restart apres modif recette a la main/thickness.csv'  # "After" file
```

**In Python Script** (`thickness_analysis.py`):
```python
# Edit the main() function around line 386
def main():
    # Configuration des fichiers
    csv_file_1 = './CSV/2-apres/thickness_ENG.csv'       # "Before" file
    csv_file_2 = './CSV/10-restart apres modif recette a la main/thickness.csv'  # "After" file
```
