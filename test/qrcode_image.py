from MyQR import myqr
import os
version, level, qr_name = myqr.run(
	"Honey, I'm coming !",
    version=4,
    level='Q',
    picture='20170711122040.gif',
    colorized=False,
    contrast=1.5,
    brightness=1.3,
    save_name='201707111302321.gif',
    save_dir=os.getcwd()
	)