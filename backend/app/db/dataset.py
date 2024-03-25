import pandas as pd
from app.models import Book, Rating
from pathlib import Path


def load_datasets():
    dataset_path = Path('/app/datasets')
    # if file "loaded.txt" exists in the dataset folder, it contains the list of files that have been loaded
    # if it doesn't exist we create it
    # then we load the files that haven't been loaded yet

    if not dataset_path.joinpath('loaded.txt').exists():
        dataset_path.joinpath('loaded.txt').touch()

    with open(dataset_path.joinpath('loaded.txt'), 'r') as f:
        loaded_files = f.read().splitlines()

    books = []
    for file in (dataset_path / 'books').iterdir():
        if file.is_file() and file.suffix == '.csv' and file.name not in loaded_files:
            data = pd.read_csv(file)
            data['year'] = data['year'].fillna(0).astype(int)

            for _, row in data.iterrows():
                book = Book(
                    title=str(row['title']) or '-',
                    author=str(row['author']) or '-',
                    description=str(row['description']) or '-',
                    short_description=str(row['short_description']) or '-',
                    year=row['year'] or 0,
                    cover=str(row['cover']) or '',
                    original_title=str(row['original_title']) or '',
                    original_isbn=str(row['original_isbn']) or '',
                    rating=5,
                    genre='-'
                )
                books.append(book)
            loaded_files.append(file.name)
            print(f'Loaded {file.name}')

    ratings = []
    for file in (dataset_path / 'ratings').iterdir():
        if file.is_file() and file.suffix == '.csv' and file.name not in loaded_files:
            data = pd.read_csv(file)
            for _, row in data.iterrows():
                rating = Rating(
                    user_id=str(row['User-ID']),
                    isbn=str(row['ISBN']),
                    rating=str(row['Book-Rating'])
                )
                ratings.append(rating)
            loaded_files.append(file.name)
            print(f'Loaded {file.name}')

    with open(dataset_path.joinpath('loaded.txt'), 'w') as f:
        f.write('\n'.join(loaded_files))

    return books, ratings
