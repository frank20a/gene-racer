import numpy as np
from copy import deepcopy
import json, os


sigmoid = lambda x: 1 / (1 + np.exp(-x/100))
relu = lambda x: np.maximum(0, x)


class Brain:
    def __init__(self, name: str, inputs: int, inner_layers: int, inner_dims: list, outputs: int):
        self.i = inputs
        self.n = inner_layers
        self.ds = inner_dims
        self.o = outputs
        self.name = name
        
        self.weights = []
        self.biases = []
        self.init_weights()
        self.init_biases()

    def init_weights(self):
        self.weights = [np.random.uniform(-1, 1, (self.i, self.ds[0]))]
        for i in range(self.n - 1):
            self.weights.append(np.random.uniform(-1, 1, (self.ds[i], self.ds[i+1])))
        self.weights.append(np.random.uniform(-1, 1, (self.ds[-1], self.o)))

    def init_biases(self):
        for i in range(self.n):
            self.biases.append(np.random.uniform(-1, 1, (self.ds[i], )))
        self.biases.append(np.random.uniform(-1, 1, (self.o, )))

    def calculate(self, inputs: np.ndarray) -> np.ndarray:
        if inputs.shape[0] != self.i:
            raise ValueError('Inputs must be of shape ({},)'.format(self.i))
        
        res = np.matmul(inputs, self.weights[0]) + self.biases[0]
        for i in range(self.n - 1):
            res = relu(np.matmul(res, self.weights[i+1]) + self.biases[i+1])
            
        return sigmoid(np.matmul(res, self.weights[-1]) + self.biases[-1])

    def mutate(self, mutation_rate: float):
        for w in self.weights:
            for i in range(w.shape[0]):
                for j in range(w.shape[1]):
                    if np.random.random() < mutation_rate:
                        w[i, j] = np.random.uniform(-1, 1)
    
        for b in self.biases:
            for i in range(b.shape[0]):
                if np.random.random() < mutation_rate:
                    b[i] = np.random.uniform(-1, 1)

    def crossover(self, other: 'Brain', keep_rate: float = 0.5) -> 'Brain':
        if self.i != other.i or self.n != other.n or self.o != other.o:
            raise ValueError('Brains must be of same shape')
        
        child = Brain(self.i, self.n, self.ds, self.o)
        for i in range(self.n):
            for j in range(self.ds[i]):
                if np.random.random() < keep_rate:
                    child.weights[i][j] = self.weights[i][j]
                else:
                    child.weights[i][j] = other.weights[i][j]
        
        return child

    def copy(self) -> 'Brain':
        res = Brain(self.name, self.i, self.n, self.ds, self.o)
        res.weights = deepcopy(self.weights)
        res.biases = deepcopy(self.biases)
        return res

    def copy_mutated(self, mutation_rate: float) -> 'Brain':
        res = self.copy()
        res.mutate(mutation_rate)
        return res
    
    def save(self, filename: str = None):
        if filename is None:
            filename = f'brain_{self.name}'
        
        with open(os.path.join(os.environ['GAME_DIR'], f'/bin/{filename}.json'), 'w') as f:
            json.dump({'i': self.i, 'n': self.n, 'ds': self.ds, 'o': self.o, 'weights': self.weights, 'biases': self.biases}, f)
            
    def load(self, filename: str):
        with open(os.path.join(os.environ['GAME_DIR'], f'/bin/{filename}.json'), 'r') as f:
            data = json.load(f)
            self.i = data['i']
            self.n = data['n']
            self.ds = data['ds']
            self.o = data['o']
            self.weights = np.array(data['weights'], dtype=np.float64)
            self.biases = np.array(data['biases'], dtype=np.float64)