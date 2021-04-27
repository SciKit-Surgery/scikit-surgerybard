/*
This is an example configuration file for SciKit-SurgeryBARD post
v0.1.0. It is not valid json, to use it you can first need to remove
comments with something like https://pypi.org/project/JSON_minify/
*/

/*
BARD configuration is divided into 5 optional dictionaries
camera, tracker, models, pointer, and interaction.
*/

{
    /* Camera dictionary defines the parameters for the video source
    that forms the back ground of the augmented reality */
    "camera": {
	/* source defines an opencv video soure, integer or filename,
	defaults to 0 */
        "source": 0, 
	/* window size defines the size of the video image to use. If 
	not set this delegates to 
	sksurgeryimage.acquire.video_source.TimestampedVideoSource
	which set's them to cv2.CAP_PROP_FRAME_WIDTH and 
	cv2.CAP_PROP_FRAME_HEIGHT which will depend on the source you're 
	using. Take care that the window size matches the image size
	used during camera calibration */
        "window size": [640, 480],
	/* calibration directory containing an .intrinsics.txt 
	and a .distortion.txt file. This will be ignored if you 
	use the -d command line argument*/
        "calibration directory": "data/calibration/matts_mbp_640_x_480"
    },
    "tracker" : {
	"type" : "sksaruco",
	/* BARD allows source as synomym of video source*/
	"source" : 0,
	"calibration directory": "data/calibration/matts_mbp_640_x_480",
	rigid_bodies : [ {
		'name' : 'reference',
                'filename' : "data/reference_for_small_liver.txt"
                'aruco dictionary' : 'DICT_ARUCO_ORIGINAL'
		},
		{
			'name' : 'pointer',
			'filename' : 'data/pointer.txt',
                	'aruco dictionary' : 'DICT_ARUCO_ORIGINAL',
		}]
    }


	
	
	
	"video source" : 0,
	"calibraion" : "somefile.txt",
	"camera projection" : some matrix,
	"camera distortion" : a distortion vector




    "models": {
        "models_dir": "data/models",
        "ref_file": "data/reference_for_small_liver.txt",
        "reference_to_model": "data/reference_to_model.txt",
        "visible_anatomy": 1
    },
    "interaction": {
        "keyboard": true,
        "footswitch": true,
        "maximum delay": 2.0,
        "mouse": true
    },
    "pointerData": {
        "pointer_tag_file": "data/pointer.txt",
        "pointer_tag_to_tip": "data/pointer_tip.txt"
    }
}
