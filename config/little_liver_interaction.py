{
    "camera": {
        "source": 0,
        "width": 640,
        "height": 480,
        "grab": 33,
        "clock": 15,
        "fullscreen": false,
	"calibration" : "data/calibration.npz"
    },
    "models": {
        "models_dir": "data/models",
	    "ref_file": "data/reference_for_small_liver.txt",
	    "reference_to_model" : "data/reference_to_model.txt",
        "visible_anatomy" : 1
    },

    "interaction": {
        "keyboard"      : true,
        "footswitch"    : true,
        "maximum delay" : 2.0,
        "mouse"         : true
    },

    "pointerData": {
        "pointer_tag_file": "data/pointer.txt",
        "pointer_tag_to_tip": "data/pointer_tip.txt"
    }


}
