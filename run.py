import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from autoencoders import *
from fais import *
from kmeans import *
from knn import *
from nn import *
from rf import *
from svm import *
from vecctors import *
from dataprep import *

def get_vectors(file_path, need, weights):
    player_stats_dict = prepare_data(file_path)
    player_stats_dict = clean_data(player_stats_dict)
    player_distances = calculate_distance(player_stats_dict, need)
    player_similarities = calculate_cosine_similarity(player_stats_dict, need)
    player_manhattan_distances = calculate_manhattan_distance(player_stats_dict, need)
    player_weighted_distances = calculate_weighted_distance(player_stats_dict, need, weights)
    return player_distances, player_similarities, player_manhattan_distances, player_weighted_distances

def get_svm(file_path, need):
    df = prepare_data_svm(file_path)
    model, scaler, player_names, X = train_svm(df)
    return find_nearest_players(model, scaler, player_names, X, need, top_n=3)

def get_rf(file_path, need):
    df = prepare_data_rf(file_path)
    model, scaler, player_names, X = train_random_forest(df)
    return find_nearest_players(model, scaler, player_names, X, need, top_n=3)

def get_nn(file_path, need):
    df = prepare_data_nn(file_path)
    model, scaler, player_names, X = train_neural_network(df)
    return find_nearest_players_nn(model, scaler, player_names, X, need, top_n=3)

def get_kmeans(file_path, need):
    df = prepare_data_kmeans(file_path)
    kmeans, scaler, player_names, X = train_kmeans(df, n_clusters=5)
    return find_nearest_players_kmeans(kmeans, scaler, player_names, X, need, top_n=3)

def get_fais(file_path, need):
    df = prepare_data_fais(file_path)
    index, scaler, player_names, X_scaled = train_faiss(df)
    return find_nearest_players_fais(index, scaler, player_names, X_scaled, need, top_n=3)

def get_autoencoders(file_path, need):
    df = prepare_data_autoencoders(file_path)
    encoder, scaler, player_names, X_scaled = train_autoencoder(df, encoding_dim=16, epochs=100, batch_size=8)
    return find_nearest_players_autoencoders(encoder, scaler, player_names, X_scaled, need, top_n=3)

def get_knn(file_path, need):
    df = prepare_data_knn(file_path)
    model, scaler, player_names, X = train_knn(df)
    return find_nearest_players_knn(model, scaler, player_names, X, need, top_n=3)

def get_lists(file_path, need, weights):
    autoencoder = get_autoencoders(file_path, need)
    fais = get_fais(file_path, need)
    kmeans = get_kmeans(file_path, need)
    knn = get_knn(file_path, need)
    nn = get_nn(file_path, need)
    rf = get_rf(file_path, need)
    svm = get_svm(file_path, need)
    
    player_distances, player_similarities, player_manhattan_distances, player_weighted_distances = get_vectors(file_path, need, weights)
    
    vectors_euc = get_nearest_players(player_distances, 3)
    vectors_cos = get_most_similar_players(player_similarities, 3)
    vectors_man = get_nearest_players(player_manhattan_distances, 3)
    vectors_weuc = get_nearest_players(player_weighted_distances, 3)
    
    # Combine all lists into one
    all_players = [autoencoder, fais, kmeans, knn, nn, rf, svm, vectors_euc, vectors_cos, vectors_man, vectors_weuc]
    return all_players

def find_intersection(*lists):
    return set(lists[0]).intersection(*lists[1:])

def get_plot(file_path, need, weights):
    all_players = get_lists(file_path, need, weights)
    
    # Flatten the list of lists
    all_players_flat = [player for sublist in all_players for player in sublist]
    player_counts = Counter(all_players_flat)
    
    plt.figure(figsize=(12, 6))
    plt.bar(player_counts.keys(), player_counts.values())
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Players')
    plt.ylabel('Count')
    plt.title('Number of Times Each Player Was Selected')
    plt.show()
    
    # Find intersection
    common_players = find_intersection(*all_players)
    print("Players common in all methods:", common_players)

if __name__ == "__main__":
    file_path = "2025_scc_5a_nba_player_data_2023.xlsx"
    need = np.array([1, 300, 50, 120, 0.45, 40, 100, 0.4, 10, 20, 0.5, 0.55, 5, 10, 0.8, 5, 30, 40, 20, 10, 5, 5, 20, 100])
    weights = np.array([1, 0.5, 0.8, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1.5, 1, 1, 2, 1, 1, 1, 1.2, 1.2, 1.5, 1, 0.8])
    get_plot(file_path, need, weights)
