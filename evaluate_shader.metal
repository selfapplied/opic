#include <metal_stdlib>
using namespace metal;

// Evaluation shader - complete evaluation pipeline in Metal
// Buffer layout:
// buffer(0): constants [map_size, num_queries, k] as uint
// buffer(1): query_embeddings [num_queries * 768] as float
// buffer(2): map_embeddings [map_size * 768] as float
// buffer(3): predictions [num_queries] as uint (output)
// buffer(4): similarities [num_queries] as float (output)

// Cosine similarity between two vectors
float cosine_similarity(device float* vec1, device float* vec2, uint dim) {
    float dot = 0.0;
    float norm1 = 0.0;
    float norm2 = 0.0;
    for(uint i = 0; i < dim; i++) {
        dot += vec1[i] * vec2[i];
        norm1 += vec1[i] * vec1[i];
        norm2 += vec2[i] * vec2[i];
    }
    return dot / (sqrt(norm1) * sqrt(norm2));
}

// Main evaluation kernel - computes predictions for all queries
kernel void evaluate_kernel(
    constant uint* constants [[buffer(0)]],      // [map_size, num_queries, k]
    device float* query_embeddings [[buffer(1)]], // [num_queries * 768]
    device float* map_embeddings [[buffer(2)]],   // [map_size * 768]
    device uint* predictions [[buffer(3)]],       // [num_queries] output
    device float* similarities [[buffer(4)]],    // [num_queries] output
    uint id [[thread_position_in_grid]]
) {
    uint map_size = constants[0];
    uint num_queries = constants[1];
    uint k = constants[2];
    
    if(id >= num_queries) {
        return;
    }
    
    // Get query embedding (query_indices tells us which embedding from map to use as query)
    // For now, use the query embedding directly (we'll match it in the map)
    device float* query = &query_embeddings[id * 768];
    
    // Find k-nearest neighbors
    float max_sims[5] = {-1.0, -1.0, -1.0, -1.0, -1.0};
    uint max_indices[5] = {0, 0, 0, 0, 0};
    
    // Compute similarities with all embeddings in map
    for(uint i = 0; i < map_size; i++) {
        device float* embedding = &map_embeddings[i * 768];
        float sim = cosine_similarity(query, embedding, 768);
        
        // Insert into top-k (simple insertion sort)
        for(uint j = 0; j < k; j++) {
            if(sim > max_sims[j]) {
                // Shift down
                for(uint m = k - 1; m > j; m--) {
                    max_sims[m] = max_sims[m-1];
                    max_indices[m] = max_indices[m-1];
                }
                max_sims[j] = sim;
                max_indices[j] = i;
                break;
            }
        }
    }
    
    // Select best prediction (first in k-nearest)
    predictions[id] = max_indices[0];
    similarities[id] = max_sims[0];
}

