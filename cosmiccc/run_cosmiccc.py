#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

import argparse
import astroscrappy
import glob
from astropy.io import fits
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Script for running cosmiccc")
    # group = argparser.add_mutually_exclusive_group(required=True)
    parser.add_argument("file", type=str, help="Spectral input file")
    parser.add_argument("-s", "--sigclip", default=5, help="Sigma clipping value")
    parser.add_argument(
        "-f", "--sigfrac", default=0.01, help="Sigma clipping fraction",
    )
    parser.add_argument("-o", "--objlim", default=15, help="Object limit")
    parser.add_argument("-n", "--niter", default=10, help="Number of iterations")
    return parser.parse_args()


def main(args):
    fitsfile = fits.open(args.file)
    print(
        "Removing cosmics from file: ", args.file,
    )
    crmask, clean_arr = astroscrappy.detect_cosmics(
        fitsfile[0].data,
        sigclip=args.sigclip,
        sigfrac=args.sigfrac,
        objlim=args.objlim,
        cleantype="medmask",
        niter=args.niter,
        sepmed=True,
        verbose=True,
    )
    fitsfile[0].data = clean_arr
    fitsfile.writeto(args.file + "_cosmiccced.fits", output_verify="fix")
