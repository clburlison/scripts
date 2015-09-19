munkiimport_logic_audio.py
===

This python wrapper is useful for importing a directory of audio content packages into your Munki Repo. To download the audio content use Hannes Juutilainen's [download-logicprox-content.py](https://github.com/hjuutilainen/adminscripts/blob/master/download-logicprox-content.py) script. 

You will want to modify the following script options to match your environment.

    LOGICNAME = 'Logic Pro X' # This is the `name` of Logic in your repo.
    
    MUNKIIMPORT_OPTIONS = [
        "--subdirectory", "cte/audiovideo/logicx/audio",    
        "--developer", "Apple",
        "--category", "Media",
        "--catalog", "production",
        "--icon", "audio.png",
    ]


EXAMPLE:

    $ ./download-logicprox-content.py download -o ~/Downloads/LogicProContent

    $ ./munkiimport_logic_audio.py ~/Downloads/LogicProContent

---

#Updated for Logic 10.2.0
**September 18th, 2015**

This script has been updated to support Logic Pro 10.2.0. This release included many additional audio libraries for the added Alchemy Plugin. The updated script from Hannes will now download audio content to a "__Downloaded Items" directory and create hard links to Apple's categories. 

The biggest issues this script solves is importing all 357 packages in an automated fashion. The install size is a big factor on laptops with smaller SSDs. For example (_not exact_):

* Logic Pro X - 1.42 GB
* Essental Content - 2.68 GB
* Base Audio Content - 35.32 GB
* Alchemy Content - 13 GB

Not all laptops I manage need all 50 GBs of content. Some can get away with just Logic plus the essental content. However, I needed a solution that was flexible. 

See the included demo ``munki_repo`` for examples.

---

Based off work by Tim Sutton[munkiimport_cc_installers](https://github.com/timsutton/aamporter/blob/master/scripts/munkiimport_cc_installers.py) AND [aamporter.py](https://github.com/timsutton/aamporter/blob/master/aamporter.py).   