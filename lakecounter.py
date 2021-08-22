"""
 Author:      Jiawen Liu
 Question:    Count of Lakes
 Description: Given a matrix where 0 represents water and 1 represents land, count the
              number of lakes in it. A lake is surrounded by lands and is formed by connecting adjacent
              water horizontally or vertically or diagonally.
 Assumption:  The matrix is assumed to be a 2d list with integer 0s and 1s.
 Solution:    Executing this file will print out the sample matrix used and the total number of lakes found.
"""

def count_lakes(matrix):
    """
    This method  solves question Count of Lakes.
    """
    if not matrix or len(matrix) == 0:
        print("Invalid matrix")
        return 0
    num_lakes = 0
    num_row = len(matrix)
    num_col = len(matrix[0])
    for i in range(0, num_row):
        for j in range(0, num_col):
            if matrix[i][j] == 0:
                # If a water cell is found, convert all water cells connected to this cell to land
                # So that one lake is disappeared from the matrix and it will not be traversed again
                # Increase the number of lakes found by 1
                check_adjacent_water(i,j, num_row, num_col, matrix)
                num_lakes += 1
    return num_lakes

def check_adjacent_water(i, j, num_row, num_col, matrix):
    """
        If the given position(i,j) in matrix is water, convert itself and all its adjacent water to land.
            :param i Row index
            :param j Column index
    """
    # Do nothing on current cell if it is out of bound in any dimension or it is land
    if i >= num_row or i < 0:
        return
    elif j >= num_col or j < 0:
        return
    elif matrix[i][j] == 1:
        return
    else:
    # Convert current cell to land and recursively call this method on all its adjacent cells
    # So all water cells connected to current cell will be converted to land eventually
        matrix[i][j] = 1
        check_adjacent_water(i - 1, j - 1, num_row, num_col, matrix)
        check_adjacent_water(i - 1, j, num_row, num_col, matrix)
        check_adjacent_water(i, j - 1, num_row, num_col, matrix)
        check_adjacent_water(i + 1, j + 1, num_row, num_col, matrix)
        check_adjacent_water(i + 1, j, num_row, num_col, matrix)
        check_adjacent_water(i, j + 1, num_row, num_col, matrix)
        check_adjacent_water(i + 1, j - 1, num_row, num_col, matrix)
        check_adjacent_water(i - 1, j + 1, num_row, num_col, matrix)

def main():
    matrix = [[1,0,1,0,0,0,1],
              [0,0,1,0,1,0,1],
              [1,1,1,1,0,0,1],
              [1,0,0,1,0,1,0],
              [1,1,1,1,0,0,0],
              [0,1,0,1,0,0,1],
              [0,0,0,0,0,1,1],
              [0,0,0,1,0,0,1],
              [1,0,1,0,1,0,0],
              [1,1,1,1,0,0,0]]
    print("Count the lakes within this matrix:")
    for row in matrix:
        print(row)
    num_lakes = count_lakes(matrix)
    print(f"There are total of {num_lakes} lakes in the matrix.")

main()






