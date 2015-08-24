munkiimport_logic_audio.py
===

This python wrapper is useful for importing a directory of audio content packages into your Munki Repo. To download the audio content use Hannes Juutilainen's [download-logicprox-content.py](https://github.com/hjuutilainen/adminscripts/blob/master/download-logicprox-content.py) script. 

You will want to modify the following script options to match your environment.

    MUNKIIMPORT_OPTIONS = [
        "--subdirectory", "cte/audiovideo/logicx/audio",
        "--developer", "Apple",
        "--category", "Media",
        "--update-for", "Logic Pro X",
        "--catalog", "production",
    ]

EXAMPLE:

    $ ./download-logicprox-content.py download -o ~/Downloads/LogicProContent
  
    $ ./munkiimport_logic_audio.py ~/Downloads/LogicProContent

---


Based off work by [Tim Sutton](https://github.com/timsutton/aamporter/blob/master/scripts/munkiimport_cc_installers.py).   