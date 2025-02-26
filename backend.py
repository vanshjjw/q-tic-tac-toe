from qiskit import QuantumCircuit, transpile
from qiskit_aer.primitives import SamplerV2
from qiskit.quantum_info.operators import Operator
import math
import numpy as np


def makeCirc(m, Indexes, superMeasure, measurables, SuperMeasureIndexes, SuperMeasureValue):
    qc = QuantumCircuit(9, 9)
    placeQubits(m, qc)
    EntangleQubits(m, qc)
    measureAll = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    qc.measure(measureAll, measureAll)
    o = simulate(qc)
    o = o[::-1]
    if superMeasure:
        return checkAllMeasures(o, Indexes, measurables, SuperMeasureIndexes, SuperMeasureValue)
    else:
        return (o[Indexes[0]] == o[Indexes[1]]) and (o[Indexes[1]] == o[Indexes[2]])


def placeQubits(m, qc):
    for i in range(0, 3):
        for j in range(0, 3):
            if m[2][i][j] == -1 and m[0][i][j] != -1:
                qc.unitary(makeOperator(m[0][i][j]), [3 * i + j], label=str(m[0][i][j]))


def EntangleQubits(m, qc):
    for i in range(0, 3):
        for j in range(0, 3):
            if 70 <= m[2][i][j] < 80:
                qc.barrier()
                qc.cx(m[2][i][j] - 70, 3 * i + j)
            if 80 <= m[2][i][j] < 90:
                qc.barrier()
                qc.x(3 * i + j)
                qc.cx(m[2][i][j] - 80, 3 * i + j)


def makeOperator(probability):
    angle = math.acos(np.sqrt(probability / 100))
    return Operator([
        [math.cos(angle), math.sin(angle)],
        [-math.sin(angle), math.cos(angle)]
    ])


def checkAllMeasures(o, index, measurables, SuperMeasureIndexes, SuperMeasureValue):
    for m in measurables:
        if (o[m[0]] == o[m[1]]) and (o[m[1]] == o[m[2]]):
            if m[0] in index and m[1] in index and m[2] in index:
                SuperMeasureIndexes = m
                SuperMeasureValue = o[m[0]]
                return True
    return False


def simulate(qc):
    sampler = SamplerV2()
    job = sampler.run([qc], shots=1)
    results = job.result()
    try:
        counts = results[0].data.c.get_counts()
    except AttributeError:
        counts =  results[0].data.meas.get_counts()
    return list(counts.keys())[0]


def QuantumMoveMaker(myBoard, p1, p2):
    qc = QuantumCircuit(3, 1)

    if myBoard[0][p1 // 3][p1 % 3] != -1 and myBoard[0][p2 // 3][p2 % 3] != -1:
        qc.unitary(makeOperator(myBoard[0][p1 // 3][p1 % 3]), 0, label=str(myBoard[0][p1 // 3][p1 % 3]))
        qc.unitary(makeOperator(myBoard[0][p2 // 3][p2 % 3]), 1, label=str(myBoard[0][p2 // 3][p2 % 3]))
        qc.x(2)
        qc.cx(0, 2)
        qc.cx(1, 2)

    elif myBoard[0][p1 // 3][p1 % 3] != -1:
        qc.unitary(makeOperator(myBoard[0][p1 // 3][p1 % 3]), 0, label=str(myBoard[0][p1 // 3][p1 % 3]))
        qc.cx(0, 2)

    elif myBoard[0][p2 // 3][p2 % 3] != -1:
        qc.unitary(makeOperator(myBoard[0][p2 // 3][p2 % 3]), 1, label=str(myBoard[0][p2 // 3][p2 % 3]))
        qc.cx(1, 2)

    qc.measure([2], [0])


    sampler = SamplerV2()
    job = sampler.run([qc], shots=128)
    results = job.result()
    c = results[0].data.c.get_counts()

    if '0' in c.keys():
        zero = c['0']
    else:
        zero = 0
    if '1' in c.keys():
        one = c['1']
    else:
        one = 0
    return zero, one
