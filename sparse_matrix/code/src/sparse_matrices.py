#!/usr/bin/python3

class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=0, numCols=0):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}  # {(row, col): value}

        if matrixFilePath:
            self.load_matrix(matrixFilePath)

    def load_matrix(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
                self.numRows = int(lines[0].split('=')[1])
                self.numCols = int(lines[1].split('=')[1])

                for line in lines[2:]:
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")

                    parts = line.strip('()').split(',')
                    if len(parts) != 3:
                        raise ValueError("Input file has wrong format")

                    row, col, value = map(int, parts)
                    self.elements[(row, col)] = value
        except (ValueError, IndexError):
            raise ValueError("Input file has wrong format")

    def get_element(self, row, col):
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def __str__(self):
        result = []
        for (row, col), value in sorted(self.elements.items()):
            result.append(f"({row}, {col}, {value})")
        return "\n".join(result)


def additionOfMatrices(mat1, mat2):
    if mat1.numRows != mat2.numRows or mat1.numCols != mat2.numCols:
        raise ValueError("Matrix dimensions do not match for addition")

    result = SparseMatrix(numRows=mat1.numRows, numCols=mat1.numCols)

    all_keys = set(mat1.elements.keys()).union(mat2.elements.keys())
    for key in all_keys:
        val = mat1.get_element(*key) + mat2.get_element(*key)
        result.set_element(key[0], key[1], val)

    return result


def subtractionOfSparseMatrices(mat1, mat2):
    if mat1.numRows != mat2.numRows or mat1.numCols != mat2.numCols:
        raise ValueError("Matrix dimensions do not match for subtraction")

    result = SparseMatrix(numRows=mat1.numRows, numCols=mat1.numCols)

    all_keys = set(mat1.elements.keys()).union(mat2.elements.keys())
    for key in all_keys:
        val = mat1.get_element(*key) - mat2.get_element(*key)
        result.set_element(key[0], key[1], val)

    return result


def MultiplicationOfMatrices(mat1, mat2):
    if mat1.numCols != mat2.numRows:
        raise ValueError("Matrix dimensions do not match for multiplication")

    result = SparseMatrix(numRows=mat1.numRows, numCols=mat2.numCols)

    for (i, k), val1 in mat1.elements.items():
        for j in range(mat2.numCols):
            val2 = mat2.get_element(k, j)
            if val2 != 0:
                current = result.get_element(i, j)
                result.set_element(i, j, current + val1 * val2)

    return result


def main():
    try:
        # Correct file paths relative to script
        matrixOnePath = "../../sample_inputs/easy_sample_03_1.txt"
        matrixTwoPath = "../../sample_inputs/easy_sample_03_2.txt"

        mat1 = SparseMatrix(matrixOnePath)
        mat2 = SparseMatrix(matrixTwoPath)

        print("Select matrix operation:")
        print("1) Add\n2) Subtract\n3) Multiply")
        choice = input("Enter 1, 2, or 3: ").strip()

        if choice == '1':
            result = additionOfMatrices(mat1, mat2)
        elif choice == '2':
            result = subtractionOfSparseMatrices(mat1, mat2)
        elif choice == '3':
            result = MultiplicationOfMatrices(mat1, mat2)
        else:
            print("❌ Invalid option selected.")
            return

        print("✅ Result:")
        print(result)

    except FileNotFoundError:
        print("❌ Matrix file not found.")
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()

