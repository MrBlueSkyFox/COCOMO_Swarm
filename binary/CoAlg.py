from binary.pop import Pop, np
import copy
from metrix import MD
import random


class COCOMO():
    def __init__(self, max, min, n, pop, generations):
        ar_pop = []
        for i in range(0, pop):
            ar_pop.append(Pop(max=max, min=min, n=n))
        self.pop_array = np.array(ar_pop)
        self.generations = generations

    def breeding(self, array_pop):
        array_copy = copy.deepcopy(array_pop)
        couples = []
        offsprings = []
        for s in array_pop:
            offsprings.append(self.breed_one(array_pop))

        for i in range(0, int(len(array_copy) / 2)):
            # couple = [self.choseOne(array_copy), self.choseOne(array_copy)]
            #   couples.append(couple)
            a = offsprings.pop()
            k = random.randint(0, len(offsprings) - 1)
            b = offsprings.pop(k)
            couples.append([a, b])

        return couples

    def breed_one(self, species):
        sum_fit_func = 0
        min_fit_func = float("inf")
        for s in species:
            if s.fit_func() < min_fit_func:
                min_fit_func = s.fit_func()
        for s in species:
            sum_fit_func = sum_fit_func + s.fit_func() - min_fit_func
        rnd = random.random() * sum_fit_func
        csum = 0
        for s in species:
            csum = csum + s.fit_func() - min_fit_func
            if csum >= rnd:
                return copy.deepcopy(s)

    def choseOne(self, array):
        max = sum([
            MD(c.vector) for c in array
        ])
        select_prob = [MD(c.vector) / max for c in array]
        return array[np.random.choice(len(array), p=select_prob)]

    def crossover(self, spec1, spec2, pop_len, chance_of_crossover=0.9):
        k = random.randint(0, pop_len - 1)
        a = copy.deepcopy(spec1)
        b = copy.deepcopy(spec2)
        s = random.random()
        if s <= chance_of_crossover:
            vector1 = [
                (a.to_int(a.vector[0]) & (~(1 << k))) | (spec2.to_int(spec2.vector[0]) & (1 << k)),
                (a.to_int(a.vector[1]) & (~(1 << k))) | (spec2.to_int(spec2.vector[1]) & (1 << k))
            ]
            vector2 = [
                (b.to_int(b.vector[0]) & (~(1 << k))) | (spec1.to_int(spec1.vector[0]) & (1 << k)),
                (b.to_int(b.vector[1]) & (~(1 << k))) | (spec1.to_int(spec1.vector[1]) & (1 << k))
            ]
            # now they are in binary view
            vector1 = [a.from_int(vector1[0]), a.from_int(vector1[1])]
            vector2 = [b.from_int(vector2[0]), b.from_int(vector2[1])]
            a.vector = vector1
            b.vector = vector2
            if (a.vector[0] > a.max or a.vector[1] > a.max or
                    a.vector[0] < a.min or a.vector[1] < a.min):
                a = copy.deepcopy(spec1)
            if (b.vector[0] > b.max or b.vector[1] > b.max or
                    b.vector[0] < b.min or b.vector[1] < b.min):
                b = copy.deepcopy(spec2)
        return [a, b]

    def mutate(self, pop, pop_len, chance_of_mutation=0.1):
        k = random.randint(0, pop_len - 1)
        work_pop = copy.deepcopy(pop)
        if random.random() <= chance_of_mutation:
            work_pop.vector = [
                work_pop.to_int(work_pop.vector[0]) ^ (1 << k),
                work_pop.to_int(work_pop.vector[1]) ^ (1 << k),
            ]
            work_pop.vector = [
                work_pop.from_int(work_pop.vector[0]),
                work_pop.from_int(work_pop.vector[1])
            ]
            if (work_pop.vector[0] > work_pop.max or work_pop.vector[0] < work_pop.min
                    or work_pop.vector[1] > work_pop.max or work_pop.vector[1] < work_pop.min):
                work_pop = copy.deepcopy(pop)
        return work_pop

    def start(self):

        pop_l = len(self.pop_array)
        for s in self.pop_array:
            print(s)
        for gen in range(self.generations):
            couples = self.breeding(self.pop_array)
            ext_array = []
            for couple in couples:
                ext_array.extend(self.crossover(couple[0], couple[1], pop_l))
            mutated_array = []
            for pop in ext_array:
                mutatant = self.mutate(pop, pop_l)
                mutated_array.append(mutatant)
            for mut in mutated_array:
                mut.calc_fit()
            self.pop_array = np.array(mutated_array)
        print('----')
        print(self.pop_array[1])


# def start(self):
# Создать из массива популяции пары по 2 с помощью рулетки
# breed берет всю популяцию и отдают пары
# pair
s = COCOMO(10, 0, 16, 150, 20)
s.start()
