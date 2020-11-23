"""
Mixed Gaussian Porential
"""
import numpy as np
from nested_sampling.utils.rotations import vector_random_uniform_hypersphere



class MixedGausssian(object):
    """
    potential of the form sum_i a_i (-exp(-b_i(x-x_i)^2)). Here a_i is thed depth of the
    gaussian minimum, b_i the sharpness and x_i the coordinates. ndim is the dimension of the
    problem i.e length of x_i
        

    Parameters
    ----------
    minimum_coords_list: ndarray[len, ndim]
        x_i
    minimum_depths_list: ndarray[len]
        a_i positive array
    minimum_sharpness_list: ndarray[len]
        b_i positive array
    ndim: int
        dimension of the problem
    """
    def __init__(self, minimum_coords_list, minimum_depths_list, minimum_sharpness_list, ndim):

        # make sure inputs make sense
        assert(len(minimum_coords_list) == len(minimum_depths_list))
        assert(len(minimum_coords_list) == len(minimum_sharpness_list))
        assert(np.all(minimum_sharpness_list>0))
        assert(np.all(minimum_depths_list>0))
        
        self.length = len(minimum_coords_list)
        self.minimum_coords_list = np.array(minimum_coords_list)
        self.minimum_depths_list = np.array(minimum_depths_list)
        self.minimum_sharpness_list = np.array(minimum_sharpness_list)
        self.ndim = ndim
        
        assert(minimum_coords_list.shape[1] ==ndim)

    def get_energy(self, x):
        """
        Parameters
        ----------
        self: type
        x: ndarray[len, ndim]
            coordinates
        """
        
        x_shifted = x- self.minimum_coords_list
        x_shifted_2 = np.einsum('ij,ij->i', x_shifted, x_shifted)
        # - a_i (exp(-b_i*(x_shifted^2)))
        return -(self.minimum_depths_list*np.exp(-(self.minimum_sharpness_list*x_shifted_2)))

    def get_random_configuration(self, radius=1.):
        """
        """
        x = vector_random_uniform_hypersphere(self.ndim*self.length) * radius
        return x.reshape(x, (self.ndim, self.length))
        

        

    



class Harmonic(object):
    def __init__(self, ndim):
        """
        Parameters
        ----------

        ndim: int
        dimensions of numpy array
        """
        self.ndim = ndim
    
    def get_energy(self, x):
        """
        Parameters
        ----------
        x: numpy array
        coordinates
        """
        assert len(x) == self.ndim
        return 0.5 * x.dot(x)
    
    def get_random_configuration(self, radius=10.):
        """ return a random vector sampled uniformly from within a hypersphere of dimensions self.ndim"""
        x = vector_random_uniform_hypersphere(self.ndim) * radius
        return x