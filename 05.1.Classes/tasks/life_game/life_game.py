import typing as tp


class LifeGame(object):
    def __init__(self, initial_board: tp.Any) -> tp.Any:
        self.board = initial_board
        self.rows = len(initial_board)
        self.cols = len(initial_board[0])

    def get_next_generation(self) -> tp.Any:
        new_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self._get_neighbors(i, j)
                fish_neighbors = neighbors.count(2)
                shrimp_neighbors = neighbors.count(3)

                if self.board[i][j] == 0:
                    if fish_neighbors == 3:
                        new_board[i][j] = 2

                    elif shrimp_neighbors == 3:
                        new_board[i][j] = 3

                elif self.board[i][j] == 2:

                    if fish_neighbors < 2 or fish_neighbors > 3:
                        new_board[i][j] = 0
                    else:
                        new_board[i][j] = 2

                elif self.board[i][j] == 3:
                    if shrimp_neighbors < 2 or shrimp_neighbors > 3:
                        new_board[i][j] = 0
                    else:
                        new_board[i][j] = 3
                else:
                    new_board[i][j] = 1

        self.board = new_board
        return new_board

    def _get_neighbors(self, i: tp.Any, j: tp.Any) -> tp.Any:
        neighbors = []
        neighbor_indices = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                            (i, j - 1), (i, j + 1),
                            (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]

        for ni, nj in neighbor_indices:
            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                neighbors.append(self.board[ni][nj])

        return neighbors
