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
	"type" : "sksaruco", /*alternatively sksndi*/
	/* The tracker configuration follows the same format as
	   the tracker in use with the exceptions listed below. 
	   Note that the name of the rigid bodies should be the same
	   as in the model list, by default reference and pointer.
	   Exceptions for sksaruco
	   BARD allows source as synonym of video source, if no source 
	   or video source is set this defaults to the same value used 
	   for the camera configuration. */
	"source" : 0,
	/* BARD allows us to use calibration directory in line with the 
	   camera settings. If not calibration parameters are set
	   this defaults to the same as in the camera settings */
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
    },
	
    "models": {
        "models_dir": "data/models",
	"port handle": 'reference',
        "reference_to_model": "data/reference_to_model.txt",
        "visible_anatomy": 1
    },
    "pointer": {
	"port handle": 'pointer',
        "pointer_tag_to_tip": "data/pointer_tip.txt"
    },
    "interaction": {
        "keyboard": true,
        "footswitch": true,
        "maximum delay": 2.0,
        "mouse": true
    }
}
