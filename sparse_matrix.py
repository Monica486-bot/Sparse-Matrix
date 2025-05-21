class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        if matrixFilePath:
            self.load_matrix(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols
            self.elements = {}

    def load_matrix(self, matrixFilePath):
        try:
            with open(matrixFilePath, 'r') as f:
                self.numRows = int(f.readline().split('=')[1].strip())
                self.numCols = int(f.readline().split('=')[1].strip())
                self.elements = {}
                for line in f:
                    line = line.strip()
                    if line:
                        row, col, val = map(int, line.strip('()').split(','))
                        self.setElement(row, col, val)
        except ValueError:
            raise ValueError("Input file has wrong format")

    def getElement(self, currRow, currCol):
        return self.elements.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.elements[(currRow, currCol)] = value
        elif (currRow, currCol) in self.elements:
            del self.elements[(currRow, currCol)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices must have the same dimensions")
        result = SparseMatrix(self.numRows, self.numCols)
        for (r, c), v in self.elements.items():
            result.setElement(r, c, v + other.getElement(r, c))
        for (r, c), v in other.elements.items():
            if (r, c) not in self.elements:
                result.setElement(r, c, v)
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices must have the same dimensions")
        result = SparseMatrix(self.numRows, self.numCols)
        for (r, c), v in self.elements.items():
            result.setElement(r, c, v - other.getElement(r, c))
        for (r, c), v in other.elements.items():
            if (r, c) not in self.elements:
                result.setElement(r, c, -v)
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")
        result = SparseMatrix(self.numRows, other.numCols)
        for (r1, c1), v1 in self.elements.items():
            for c2 in range(other.numCols):
                result.setElement(r1, c2, result.getElement(r1, c2) + v1 * other.getElement(c1, c2))
        return result

    def save_to_file(self, filePath):
        with open(filePath, 'w') as f:
            f.write(f"rows={self.numRows}\n")
            f.write(f"cols={self.numCols}\n")
            for (r, c), v in self.elements.items():
                f.write(f"({r}, {c}, {v})\n")

def user_interface():
    operation = input("Choose operation: add, subtract, multiply: ").strip().lower()
    if operation not in ['add', 'subtract', 'multiply']:
        raise ValueError("Invalid operation")
    matrix1 = SparseMatrix('input_files/sample-03')
    matrix2 = SparseMatrix('input_files/sample-03')
    if operation == 'add':
        result = matrix1.add(matrix2)
    elif operation == 'subtract':
        result = matrix1.subtract(matrix2)
    elif operation == 'multiply':
        result = matrix1.multiply(matrix2)
    result.save_to_file('result_matrix.txt')

user_interface()

