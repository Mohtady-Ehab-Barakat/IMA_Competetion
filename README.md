# IMA Competition Repository

This repository contains materials and code related to the 2025 IMA Student Case Competition, focusing on analyzing NBA player data.

## Repository Contents

- **Datasets and Documentation**:
  - `2025_scc_5a_nba_player_data_2023.xlsx`: NBA player data for the year 2023.
  - `2025_scc_5b_nba_player_data_dictionary.xlsx`: Data dictionary corresponding to the player data.
  - `SCC_Appendix A.pdf` and `SCC_Appendix B[1].pdf`: Additional appendices providing further context and information.
  - `2025-IMA-Student-Case-Competition.pdf`: Official document outlining the case competition details.

- **Python Scripts**:
  - `dataprep.py`: Script for data preprocessing tasks.
  - `autoencoders.py`: Implementation of autoencoder models for data analysis.
  - `kmeans.py`: Script for performing K-Means clustering on the dataset.
  - `knn.py`: Implementation of the K-Nearest Neighbors algorithm.
  - `nn.py`: Neural network models for predictive analysis.
  - `rf.py`: Random Forest algorithm implementation.
  - `svm.py`: Support Vector Machine model for classification tasks.
  - `run.py`: Main script to execute various analyses and models.

- **Data Outputs**:
  - `player_stats_all.xlsx`: Processed player statistics.
  - `player_stats_normalized.xlsx`: Normalized version of player statistics.
  - `overall_average_impact.csv`: Data summarizing overall average impact metrics.
  - `team_impact_analysis.csv`: Analysis results pertaining to team impacts.

- **Visualizations**:
  - `Figure_2.png` and `Figure_3.png`: Graphical representations of data insights.

- **Configuration and Environment**:
  - `requirements.txt`: Lists the Python dependencies required to run the scripts in this repository.
  - `.gitignore`: Specifies files and directories to be ignored by Git.

## Getting Started

To set up the environment and run the analyses:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mohtady-Ehab-Barakat/IMA_Competetion.git
   ```

2. **Install Dependencies**:
   Navigate to the repository directory and install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Analyses**:
   Execute the `run.py` script to perform the analyses:
   ```bash
   python run.py
   ```

   Ensure that all necessary data files are present in the repository directory before running the script.

## Notes

- The scripts are designed to analyze NBA player data as part of the 2025 IMA Student Case Competition.
- For detailed information on the data and the context of the competition, refer to the provided PDFs: `2025-IMA-Student-Case-Competition.pdf`, `SCC_Appendix A.pdf`, and `SCC_Appendix B[1].pdf`.
- The repository includes various machine learning models and data processing scripts to facilitate comprehensive analysis.

## License

This project is licensed under the MIT License. For more details, refer to the `LICENSE` file in the repository.

## Acknowledgments

Special thanks to the IMA for organizing the Student Case Competition and providing the datasets.
