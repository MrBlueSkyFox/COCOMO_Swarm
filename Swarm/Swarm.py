import time

from Swarm.Particle import Particle, np


class Swarm():
    def __init__(self, min_x, max_x, n, population, W=0.6, c1=2, c2=2, generations=100, strategy_choice=1):
        self.particles = []
        [self.particles.append(Particle(n, max_x, min_x)) for i in range(0, population)]
        self.best_global_value = np.math.inf
        self.g_best_global = np.array([0, 0])

        self.const = {
            'generations': generations,
            'population': population,
            'n': n,
            'W': W,
            'c1': c1,
            'c2': c2,
            'max_x': max_x,
            'min_x': min_x,
            'strategy': strategy_choice,
            'starting_value': self.particles
        }

    def __str__(self):
        ans = 'For ' + str(self.const['n']) + ' parametrs\n'
        for i in range(0, self.const['n']):
            ans += 'x' + str(i) + '= ' + str(self.g_best_global[i]) + ' '
        ans += '\nThe Best Function value ' + str(self.best_global_value)
        return ans

    def __repr__(self):
        ans = ''
        for i in range(0, self.const['n']):
            ans += 'x' + str(i) + '= ' + str(self.g_best_global[i]) + ' '
        # print(ans)
        return ans

    def fitness(self, list_of_x: np.ndarray):
        # value = [x ** 2 for x in list_of_x]
        value = 0.0
        for i in range(0, len(list_of_x)):
            value += list_of_x[i] ** 2
        return value

    def find_best_particle(self):
        for particle in self.particles:
            new_boid = self.fitness(particle.positions)
            if new_boid < self.best_global_value:
                self.best_global_value = new_boid
                self.g_best_global = particle.positions

    def update_particles(self):
        for particle in self.particles:
            particle.p_best_global_value = self.best_global_value

    def move_particles(self):
        if self.const['strategy'] == 1:
            for particle in self.particles:
                new_speed = (self.const['W'] * particle.speed) + (self.const['c1'] * np.random.random()) * (
                        particle.p_best_local - particle.positions) + (self.const['c2'] * np.random.random()) * (
                                    self.g_best_global - particle.positions)
                particle.speed = new_speed
                particle.move()
        else:
            for particle in self.particles:
                new_speed = self.const['c1'] * np.random.random() * (particle.p_best_local - particle.positions) + \
                            self.const['c2'] * np.random.random() * (self.g_best_global - particle.positions)
                particle.speed += new_speed
                particle.move()

    def start(self):
        start_time = time.time()
        for i in range(0, self.const['generations'] + 1):
            self.find_best_particle()  # Find gloval maximum
            self.update_particles()  # update  Particles of global max
            self.move_particles()  # move in the demision
            if i % 100 == 0 or i + 1 == self.const['generations']:
                print('Generation ' + str(i) + ' Best global value ' + str(
                    self.best_global_value), ' required time --%s seconds--' % (time.time() - start_time))
                # print(start_time)
        # self.__repr__()
