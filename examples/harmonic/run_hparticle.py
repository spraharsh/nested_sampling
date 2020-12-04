from builtins import range
import argparse

from nested_sampling import NestedSampling, MonteCarloWalker, Harmonic, run_nested_sampling, Replica
from nested_sampling.utils.cv_trapezoidal import compute_cv_c

def main():
    parser = argparse.ArgumentParser(description="do nested sampling on a p[article in a n-dimensional Harmonic well")
    parser.add_argument("-K", "--nreplicas", type=float, help="number of replicas", default=1e1)
    parser.add_argument("-A", "--ndof", type=int, help="number of degrees of freedom", default=3)
    parser.add_argument("-P", "--nproc", type=int, help="number of processors", default=1)
    parser.add_argument("-N", "--nsteps", type=int, help="number of MC steps per NS iteration", default=int(1e3))
    parser.add_argument("--stepsize", type=float, help="stepsize, adapted between NS iterations", default=20)
    parser.add_argument("--etol", type=float, help="energy tolerance: the calculation terminates when the energy difference \
                                                    between Emax and Emin is less than etol", default=0.1)
    parser.add_argument("-q", action="store_true", help="turn off verbose printing of information at every step")
    args = parser.parse_args()
    ndof = args.ndof
    nproc = args.nproc
    nsteps = int(args.nsteps)-8
    nreplicas = int(args.nreplicas)
    stepsize = args.stepsize
    etol = args.etol
    
    #construct potential (cost function)
    potential = Harmonic(ndof)
    
    #construct Monte Carlo walker
    mc_runner = MonteCarloWalker(potential, mciter=nsteps)

    #initialise replicas (initial uniformly samples set of configurations)
    replicas = []
    for _ in range(nreplicas):
        x = potential.get_random_configuration()
        print(x)
        print(potential.get_energy(x))
        replicas.append(Replica(x, potential.get_energy(x)))
    
    #construct Nested Sampling object
    ns = NestedSampling(replicas, mc_runner, stepsize=stepsize, nproc=nproc, max_stepsize=10, verbose=not args.q)
    
    #run Nested Sampling (NS), output:
    ## label.energies (one for each iteration) 
    ## label.replicas_final (live replica energies when NS terminates)
    run_nested_sampling(ns, label="run_hparticle", etol=etol)

if __name__ == "__main__":
    main()