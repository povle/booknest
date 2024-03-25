import pandas as pd
import numpy as np
from async_lru import alru_cache
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from app.models import User, Book, Rating
from beanie import Link


@alru_cache(maxsize=None)
async def get_index_and_csr_matrix_and_model():
    dataset = await Rating.find_all().to_list()
    dataset = pd.DataFrame([rating.model_dump() for rating in dataset])
    dataset['rating'] -= 3
    matrix = dataset.pivot_table(index='isbn', columns='user_id', values='rating')
    matrix = matrix.fillna(0)
    c_matrix = csr_matrix(matrix.values)
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(c_matrix)
    return matrix.index, c_matrix, model


async def get_recommendations(user: User, k: int = 10) -> list:
    index, matrix, model = await get_index_and_csr_matrix_and_model()
    avg_embedding = np.zeros((matrix.shape[1],))
    await user.fetch_link(User.favorites)
    favorites = [x for x in user.favorites if not isinstance(x, Link)]
    if len(favorites) == 0:
        return await Book.find_all(limit=k).to_list()
    for book in favorites:
        if not book.original_isbn:
            continue
        i = index.get_loc(book.original_isbn)
        avg_embedding += matrix[i].toarray()[0]
    avg_embedding /= len(favorites)
    distances, indices = model.kneighbors(avg_embedding.reshape(1, -1), n_neighbors=k + 1)
    recommendations = []
    for i in range(k + 1):
        isbn = index[indices[0][i]]
        book = await Book.find_one(Book.original_isbn==isbn)
        if book is not None and book not in favorites:
            recommendations.append(book)
    return recommendations
