# Checking RNN accuracy and F1 score from the provided files
rnn_accuracy_f1 = {
    "Rooms 1, 5, 8": (1.00, 1.00),  # From the results discussion in the provided documents
    "Rooms 1, 3, 6, 8": (0.99, 0.99),
    "Strongest 3 RSSIs": (0.18, 0.18),
    "Strongest 5 RSSIs": (0.36, 0.36),
}

# Displaying the data
import pandas as pd
import ace_tools as tools

rnn_df = pd.DataFrame.from_dict(rnn_accuracy_f1, orient='index', columns=['Accuracy', 'F1 Score'])
tools.display_dataframe_to_user(name="RNN Accuracy and F1 Score", dataframe=rnn_df)
