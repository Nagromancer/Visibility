from astroquery.simbad import Simbad
import ssl
import certifi
import contextlib
import sys
import os

# Force Python to use certifi's CA bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = lambda: ssl_context


@contextlib.contextmanager
def suppress_stdout():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

with suppress_stdout():
    from astroquery.gaia import Gaia


def get_bp_mag(target):
    try:
        if "Gaia DR3" not in target:
            # Create a custom Simbad instance
            custom_simbad = Simbad()
            custom_simbad.TIMEOUT = 60
            custom_simbad.add_votable_fields('ids')  # Add extra IDs


            # Query object
            result = custom_simbad.query_object(target)
            ids = str(result['ids']).replace("\n", "").replace("-", "").split("|")

            # get Gaia DR3 ID
            gaia_id = None
            for id in ids:
                if "Gaia DR3" in id:
                    gaia_id = id
                    # remove anything before Gaia DR3
                    gaia_id = gaia_id.split("Gaia DR3")[1].strip()
                    break
        else:
            # If the target is already a Gaia DR3 ID
            gaia_id = target.split("Gaia DR3")[1].strip()

        # Get the bp magnitude from Gaia DR3
        query = f"""
        SELECT source_id, phot_bp_mean_mag
        FROM gaiadr3.gaia_source
        WHERE source_id = {gaia_id}
        """

        with suppress_stdout():
            job = Gaia.launch_job_async(query)
            result = job.get_results()
        bp_mag = result['phot_bp_mean_mag'][0]
        return bp_mag
    except Exception as error:
        return None
