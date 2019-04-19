# Run KittiSeg with Our Data
## Clone repository
Clone:

`git clone https://github.com/MarvinTeichmann/KittiSeg.git`

Initialize all submodules:

`git submodule update --init --recursive`
## Manage Our Data
### rosbag --> .jpg
We have wrote a convert.launch to transfer rosbag  to series of .jpg with help of Qinghai and got 7507 gray photos from HKUST to Kengkou with a Panoramic camera. Please see my file in [ftp](ftp://ftp.ram-lab.com/write/zhanghui/) for detail.
### labelme
I picked about 60 images every hundred to mark label in [labelme](http://labelme.csail.mit.edu/Release3.0/). The labelme will cover road as red and background as black automatically, so donât forget to change corresponding RGB value in **KittiSeg/hypes/KittiSeg.json**. The default is `road_color: [255,0,255]` and `background: [255,0,0]` and change them into `road_color: [255,0,0]` and `background: [0,0,0]`. Otherwise, you may get totally black photo after 5 hours training. 

The mask images is in [KittiSeg/DATA/data_road/training_DIY/Annotation](http://ee4e068.ee.ust.hk:8001/tree/usr/app/KittiSeg/DATA/data_road/training_DIY/Annotation)
### image channel
Change image channel from 1 to 3 with [data_trans.m](http://ee4e068.ee.ust.hk:8001/view/usr/app/KittiSeg/data_trans.m). 
### image path list 
Create path list train3.txt and val3.txt for inputs images which should be like below: ![](imagepath.png)
TipsïŒFirstly, you'd better write **relative** path not absolute path as the author did. You can also choose to change the os.path in [kitti\_seg\_inout.py](http://ee4e068.ee.ust.hk:8001/edit/usr/app/KittiSeg/inputs/kitti_seg_input.py). Secondly, donât forget the **space** in original image path and label image path, otherwise, you will get error âneed more than 1 value to unpackâ.

Change name of val3.txt and train3.txt in [hypes/KittiSeg.json](http://ee4e068.ee.ust.hk:8001/edit/usr/app/KittiSeg/hypes/KittiSeg.json) into yours.
## Train Our Model
`python  train.py    --hypes  hypes/KittiSeg.json`

Then you will get a folder in in RUNS like [KittiSeg\_2017\_12\_12\_08.30](http://ee4e068.ee.ust.hk:8001/tree/usr/app/KittiSeg/RUNS/KittiSeg_2017_12_12_08.30), which contains images folder, several events, model_files and output.log. 

Check the road segmentation in images and you can adjust the testing images folder and  continue to use this model if it's not bad.

`python continue.py  - -logdir    RUNS/KittiSeg_2017_12_12_08.30`

# Video Road segmentation
## Adjust to Our Input
There are three parts that need to change in test.py
[test.py](http://ee4e068.ee.ust.hk:8001/edit/usr/app/KittiSeg/test.py) if you want to run video segmentation, include the videos you have saved or live video. I have marked the three parts.

`python `

# Memory
At least 8G memory is needed and you can change in [KittiSeg/incl/tensorvision/train.py](http://ee4e068.ee.ust.hk:8001/edit/usr/app/KittiSeg/incl/tensorvision/train.py) shown as below:
![](memory.png)
0.9 means 90% of your whole memory.


