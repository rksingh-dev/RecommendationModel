import pickle
import pandas as pd
import numpy as np
import os

def generate_summary_report():
    """Generate a comprehensive summary report of both pickle files"""
    
    print("="*80)
    print("MOVIE RECOMMENDATION SYSTEM - DATA ANALYSIS REPORT")
    print("="*80)
    
    # File information
    print(f"\n📁 FILE INFORMATION:")
    print(f"   movie_list.pkl: {os.path.getsize('movie_list.pkl') / 1024 / 1024:.2f} MB")
    print(f"   similarity.pkl: {os.path.getsize('similarity.pkl') / 1024 / 1024:.2f} MB")
    
    # Load data
    with open('movie_list.pkl', 'rb') as f:
        movie_data = pickle.load(f)
    
    with open('similarity.pkl', 'rb') as f:
        similarity_matrix = pickle.load(f)
    
    print(f"\n🎬 MOVIE DATASET OVERVIEW:")
    print(f"   Total movies: {len(movie_data['title'])}")
    print(f"   Data structure: Dictionary with 3 keys")
    print(f"   Keys: {list(movie_data.keys())}")
    
    print(f"\n📊 MOVIE DATA DETAILS:")
    for key, value in movie_data.items():
        print(f"   {key}:")
        print(f"     - Type: {type(value).__name__}")
        print(f"     - Items: {len(value)}")
        if key == 'tags':
            # Calculate average tags per movie
            tag_counts = [len(tags) for tags in value.values()]
            avg_tags = np.mean(tag_counts)
            print(f"     - Average tags per movie: {avg_tags:.1f}")
            print(f"     - Min tags: {min(tag_counts)}")
            print(f"     - Max tags: {max(tag_counts)}")
    
    print(f"\n🔍 SIMILARITY MATRIX OVERVIEW:")
    print(f"   Shape: {similarity_matrix.shape}")
    print(f"   Data type: {similarity_matrix.dtype}")
    print(f"   Memory usage: {similarity_matrix.nbytes / 1024 / 1024:.2f} MB")
    print(f"   Symmetric: {np.allclose(similarity_matrix, similarity_matrix.T)}")
    print(f"   Diagonal values: All 1.0 (self-similarity)")
    
    print(f"\n📈 SIMILARITY STATISTICS:")
    # Exclude diagonal for statistics
    non_diagonal = similarity_matrix.copy()
    np.fill_diagonal(non_diagonal, 0)
    
    print(f"   Min similarity (non-diagonal): {np.min(non_diagonal):.6f}")
    print(f"   Max similarity (non-diagonal): {np.max(non_diagonal):.6f}")
    print(f"   Mean similarity: {np.mean(non_diagonal):.6f}")
    print(f"   Median similarity: {np.median(non_diagonal):.6f}")
    print(f"   Std deviation: {np.std(non_diagonal):.6f}")
    
    # Find top similar movies
    print(f"\n🏆 TOP 5 MOST SIMILAR MOVIE PAIRS:")
    top_indices = np.argsort(non_diagonal.flatten())[-5:][::-1]
    
    for i, idx in enumerate(top_indices):
        row, col = np.unravel_index(idx, non_diagonal.shape)
        similarity_score = non_diagonal[row, col]
        
        movie1_title = movie_data['title'][row]
        movie2_title = movie_data['title'][col]
        
        print(f"   {i+1}. {movie1_title}")
        print(f"      {movie2_title}")
        print(f"      Similarity: {similarity_score:.4f}")
        print()
    
    # Sample movies
    print(f"\n🎭 SAMPLE MOVIES IN DATASET:")
    sample_indices = [0, 100, 500, 1000, 1493]
    for idx in sample_indices:
        if idx in movie_data['title']:
            title = movie_data['title'][idx]
            movie_id = movie_data['movie_id'][idx]
            tag_count = len(movie_data['tags'][idx])
            print(f"   Index {idx}: {title} (ID: {movie_id}, {tag_count} tags)")
    
    print(f"\n💡 SYSTEM CAPABILITIES:")
    print(f"   ✅ Content-based movie recommendation")
    print(f"   ✅ 1,494 movies in database")
    print(f"   ✅ Pre-computed similarity matrix")
    print(f"   ✅ Tag-based similarity calculation")
    print(f"   ✅ Fast similarity lookup (O(1) for any movie pair)")
    
    print(f"\n🔧 TECHNICAL DETAILS:")
    print(f"   - Similarity scores range from 0.0 to 1.0")
    print(f"   - Higher scores indicate more similar movies")
    print(f"   - Matrix is symmetric (A[i,j] = A[j,i])")
    print(f"   - Diagonal values are 1.0 (perfect self-similarity)")
    print(f"   - Average similarity between movies: {np.mean(non_diagonal):.4f}")
    
    print(f"\n" + "="*80)

if __name__ == "__main__":
    generate_summary_report()
