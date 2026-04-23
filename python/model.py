"""Usual mechanical models are implemented in this file, such as string, bar, ball, etc.
This file hopefully can simplify the simulation."""

from .signal import Update
from .system import System, Particle, Field
import numpy as np

DT = 0.02

class RigidBody(System):
    """A rigid body is a system that do not have motion between its particles.
    This is quite a common model in life and in theory. Rigid bodies' motion
    is determined by the motion of its center of mass, and the rotation around the
    center of mass. There we rewrite the update method to make it more efficient."""
    def __init__(self, particles):
        super().__init__(particles)
        self.pos_c, self.vel_c, self.acc_c = self.find_centre()

    def update(self, dt: float, general_field: Field)-> None:
        # Centre translation
        self._translation(dt)
        # Centre rotation
        self._rotation(dt)
        # Accelerate update
        self.acc_c = np.sum(general_field[self.position] / self.mass[:, np.newaxis], axis=0) 
        pass

    def _translation(self, dt: float) -> None:
        self.pos_c += self.vel_c * dt
        self.vel_c += self.acc_c * dt

    def _rotation(self, dt: float) -> None:
        """
        NOTE: Up to now this library only supports 2D imitation,
        positive direction of omega and other quantity defined with
        cross product is defined pointing into the screen.
        more complex rotation methods should be implemented when 3D
        imitation is supported.
        Rotate the system according to the angular velocity of the system."""
        r_pos = self.position[0] - self.pos_c
        length = np.linalg.norm(r_pos)
        _ = r_pos / length * (r_pos * self.velocity[0].T) / length
        v_t = self.velocity[0] - _
        omega = np.sqrt(v_t * v_t) / np.sqrt(r_pos * r_pos)
        # Not easy direction check...
        if r_pos[0]*v_t[1] - r_pos[1]*v_t[0] < 0:
            omega *= -1
        angle = omega * dt
        self.rotate_with_angle(angle, self.pos_c)
    
    # Override
    def momentum(self):
        return np.sum(super().momentum(), axis=0)

class Bar(System):
    def __init__(self, particles, has_mass = False, uniform_distribution = True):
        """Parameters:
        particles: a list of 2 particles that form the bar.
        has_mass: whether the bar's mass matters. If False, the bar will not
        take mass into account when calculating the acceleration.
        uniform_distribution: whether the mass and electricity of the bar are
        uniformly distributed."""
        if len(particles) != 2:
            raise ValueError("A bar must have exactly 2 particles")
        super().__init__(particles)
