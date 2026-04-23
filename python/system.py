import numpy as np 
from math import sin, cos, pi
from . import signal

class Field(np.matrix):
    '''Class of fields, for example, gravity field, electric field, magnetic field, etc.
    Note that a field is hold by the Screen to register all the forces on one
    time,before the systems update thierselves, they should firstly update 
    the field to register the forces.
    Then the systems can update themselves according to the registered forces.
    TODO: 3D field, and the field can be a function of time.
    '''
    def __init__(self, width, height):
        super().__init__(np.zeros((width, height)))

class Particle:
    '''Class of prticles, basic member of mechanical imitation'''
    def __init__(self,
                 mass, electricity = 0, 
                 position = np.array([0, 0]),
                 velocity = np.array([0, 0]), 
                 acceleration = np.array([0, 0]),
                 color = "black"):
        if self.mass < 0:
            raise ValueError("Mass must be positive")
        self.mass = mass
        self.electricity = electricity
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.color = color

    def update(self, dt, general_field):
        self.position += self.velocity * dt + 0.5 * self.acceleration * dt ** 2
        self.velocity += self.acceleration * dt
        self.acceleration = general_field[self.position[0], self.position[1]] / self.mass
        return None
    
    def collision_event(self, *others, general_field):
        '''This method is related to the implementation of particles' 
        shape, electricity, etc. So it should be overridden by the 
        child class of Particle.
        Parameters:
        others: the other particles that collide with this particle.
        general_field: the field that the particles are in'''
        if type(others) != list[Particle]:
            raise TypeError("Parameter 'others' must be a list of Particle")
        if len(others) == 0:
            raise ValueError("Parameter 'others' must not be empty")
        if type(general_field) != Field:
            raise TypeError("Parameter 'general_field' must be a Field")
        pass

    def not_collision_event(self, *others, general_field):
        '''Some interactions not depend on collision. This method should 
        be specified by the child class of Particle.'''
        if type(others) != list[Particle]:
            raise TypeError("Parameter 'others' must be a list of Particle")
        if len(others) == 0:
            raise ValueError("Parameter 'others' must not be empty")
        if type(general_field) != Field:
            raise TypeError("Parameter 'general_field' must be a Field")
        pass

class System:
    '''Class of prticles, basic member of mechanical imitation.
    While particles' rotation is not taken into account, a system's rotation is 
    very important, hence there are some more complex methods that should be implemented.'''
    def __init__(self, particles):

        if type(particles) != list[Particle]:
            raise TypeError("Particles must be a list")
        # Move those data to the system class to enable Numpy operations
        self.mass = np.array([particle.mass for particle in particles])
        self.electricity = np.array([particle.electricity for particle in particles])
        self.position = np.array([particle.position for particle in particles])
        self.velocity = np.array([particle.velocity for particle in particles])
        self.acceleration = np.array([particle.acceleration for particle in particles])

    def update(self, dt, general_field):
        # Basic translation of the kinematic equations.
        # dt can be a negative number as a reversed time step
        self.position += self.velocity * dt
        self.velocity += self.acceleration * dt
        self.acceleration += general_field[self.position] * dt
        # To the GUI wiget
        return signal.Update()

    def find_centre(self):
        '''Find the centre position, velocity and acceleration of mass of the system'''
        total_mass = np.sum(self.mass)
        pos_centre = np.sum(self.position * self.mass[:, np.newaxis], axis=0) / total_mass
        vel_centre = np.sum(self.velocity * self.mass[:, np.newaxis], axis=0) / total_mass
        acc_centre = np.sum(self.acceleration * self.mass[:, np.newaxis], axis=0) / total_mass
        return pos_centre, vel_centre, acc_centre
    
    def rotate_with_angle(self, angle, reference_point = None):
        '''Rotate the system by a certain angle.
        angle: degree by default.'''
        if reference_point == None:
            raise ValueError("Reference piont can't be void. Try rotate_with_self().")
        angle = angle * pi / 180
        r_mat = np.array([[sin(angle), cos(angle)], [cos(angle), -sin(angle)]])
        pos_c, vel_c, acc_c = self.find_centre()
        self.position = (self.position - pos_c) * r_mat + pos_c
        self.velocity = (self.velocity - vel_c) * r_mat + vel_c
        self.acceleration = (self.acceleration - acc_c) * r_mat + acc_c
        return signal.Update()

    def knetic_energy(self):
        E_k = 0.5 * self.mass * np.sum(self.velocity**2, axis=1)
        return E_k

    def momentum(self):
        p = self.mass * self.velocity
        return p
    
    def moment_interia(self):
        _, _, p_c = self.find_centre()
        r_p = self.position - p_c
        r_p = np.sum(r_p**2, axis=1)# r ^ 2
        I = np.sum(r_p * self.mass)
        return I

