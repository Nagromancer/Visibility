from astropy.io import fits
import numpy as np

from path import Path
input_path = Path("/Users/nagro/Documents/median.fits")

hdulist = fits.open(input_path)
data = hdulist[0].data
header = hdulist[0].header

# Add a constant value to the data
data += 100

# save the const added data
output_path = input_path.parent / "const_added.fits"
hdu = fits.PrimaryHDU(data, header=header)
hdu.writeto(output_path, overwrite=True)
print(f"Saved the const added data to {output_path}")