from __future__ import division
from __future__ import print_function
from builtins import zip
import argparse
from pickle import FALSE, FLOAT
import numpy as np

#from utils._alpha_variance import run_alpha_variance
#from utils._jackknife_variance import run_jackknife_variance
from nested_sampling import compute_heat_capacity, get_energies, compute_log_dos

def main():   
    parser = argparse.ArgumentParser(description="load energy intervals and compute cv", 
                                     epilog="if more than one file name is given the energies from all runs will be combined and sorted."
                                     "  the number of replicas MUST be the sum of the replicas used from all runs (you need to input this number!)")
    parser.add_argument("K", type=float, help="number of replicas")
    parser.add_argument("fname", nargs="+", type=str, help="filenames with energies")
    parser.add_argument("-P", type=int, help="number of cores for parallel run", default=1)
    parser.add_argument("--Tmin", type=float,help="set minimum temperature for Cv evaluation (default=0.01)",default=0.01)
    parser.add_argument("--Tmax", type=float,help="set maximum temperature for Cv evaluation (default=0.5)",default=0.5)
    parser.add_argument("--nT", type=int,help="set number of temperature in the interval Tmin-Tmax at which Cv is evaluated (default=500)",default=500)
    parser.add_argument("--ndof", type=int, help="number of degrees of freedom (default=0)", default=4)
    parser.add_argument("--live", action="store_true", help="use live replica energies (default=False)",default=False)
    parser.add_argument("-o", type=str, default="cv", help="change the prefix of the output files")
    args = parser.parse_args()
    print(args.fname)
    print(args)

    
    print("started get_energies...")
    energies = get_energies(args.fname)
    print("energies size", np.size(energies))
    
    print("parallel nprocessors", args.P)
    print("replicas", args.K)
    K = int(args.K)
    if len(args.fname) < 2:
        assert not args.live,"cannot use live replica under any circumstances if they have not been saved, you need to add a data file with the live replicas energies"

    
    # do the computation
    T, Cv, U, U2 = compute_heat_capacity(energies, K, npar=args.P, 
                                         ndof=args.ndof, Tmin=args.Tmin, Tmax=args.Tmax, 
                                         nT=args.nT, live_replicas=args.live)

    # compute density of states
    dos_log = compute_log_dos(energies, args.P, K, args.live)

    import matplotlib.pyplot as plt
    plt.plot(energies, dos_log)
    plt.xlabel('E')
    plt.ylabel('log g(E)')
    plt.title('Log g(E)')
    plt.savefig('dos.'  + 'pdf')
    plt.show()


    
    # print to cv.dat 
    with open(args.o+".dat", "w") as fout:
        fout.write("#T Cv <E> <E^2>\n")
        for vals in zip(T, Cv, U, U2):
            fout.write("%.16g %.16g %.16g %.16g\n" % vals)
    
    # make a plot and save it
    import matplotlib
    matplotlib.use('PDF')
    import pylab as pl
    pl.plot(T, Cv)
    pl.xlabel("T")
    pl.ylabel("Cv")
    pl.savefig(args.o+".pdf")
        
    
if __name__ == "__main__":
    main()
